---
layout: post
title:  "热重启golang服务器(graceful restart golang http server)"
date: 2017-4-27 14:58:37
categories: golang 
---

服务端代码经常需要升级，对于线上系统的升级常用的做法是，通过前端的负载均衡（如nginx）来保证升级时至少有一个服务可用，依次（灰度）升级。  
而另一种更方便的方法是在应用上做热重启，直接升级应用而不停服务。  

# 原理
热重启的原理非常简单，但是涉及到一些系统调用以及父子进程之间文件句柄的传递等等细节比较多。  
处理过程分为以下几个步骤：  
1. 监听信号（USR2）
2. 收到信号时fork子进程（使用相同的启动命令），将服务监听的socket文件描述符传递给子进程
3. 子进程监听父进程的socket，这个时候父进程和子进程都可以接收请求
4. 子进程启动成功之后，父进程停止接收新的连接，等待旧连接处理完成（或超时）
5. 父进程退出，升级完成

# 细节
* 父进程将socket文件描述符传递给子进程可以通过命令行，或者环境变量等
* 子进程启动时使用和父进程一样的命令行，对于golang来说用更新的可执行程序覆盖旧程序 
* server.Shutdown()优雅关闭方法是go1.8的新特性
* server.Serve(l)方法在Shutdown时立即返回，Shutdown方法则阻塞至context完成，所以Shutdown的方法要写在主goroutine中

# 代码
``` golang
package main

import (
    "context"
    "errors"
    "flag"
    "log"
    "net"
    "net/http"
    "os"
    "os/exec"
    "os/signal"
    "syscall"
    "time"
)

var (
    server   *http.Server
    listener net.Listener
    graceful = flag.Bool("graceful", false, "listen on fd open 3 (internal use only)")
)

func handler(w http.ResponseWriter, r *http.Request) {
    time.Sleep(20 * time.Second)
    w.Write([]byte("hello world233333!!!!"))
}

func main() {
    flag.Parse()

    http.HandleFunc("/hello", handler)
    server = &http.Server{Addr: ":9999"}

    var err error
    if *graceful {
        log.Print("main: Listening to existing file descriptor 3.")
        // cmd.ExtraFiles: If non-nil, entry i becomes file descriptor 3+i.
        // when we put socket FD at the first entry, it will always be 3(0+3)
        f := os.NewFile(3, "")
        listener, err = net.FileListener(f)
    } else {
        log.Print("main: Listening on a new file descriptor.")
        listener, err = net.Listen("tcp", server.Addr)
    }

    if err != nil {
        log.Fatalf("listener error: %v", err)
    }

    go func() {
        // server.Shutdown() stops Serve() immediately, thus server.Serve() should not be in main goroutine
        err = server.Serve(listener)
        log.Printf("server.Serve err: %v\n", err)
    }()
    signalHandler()
    log.Printf("signal end")
}

func reload() error {
    tl, ok := listener.(*net.TCPListener)
    if !ok {
        return errors.New("listener is not tcp listener")
    }

    f, err := tl.File()
    if err != nil {
        return err
    }

    args := []string{"-graceful"}
    cmd := exec.Command(os.Args[0], args...)
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    // put socket FD at the first entry
    cmd.ExtraFiles = []*os.File{f}
    return cmd.Start()
}

func signalHandler() {
    ch := make(chan os.Signal, 1)
    signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM, syscall.SIGUSR2)
    for {
        sig := <-ch
        log.Printf("signal: %v", sig)

        // timeout context for shutdown
        ctx, _ := context.WithTimeout(context.Background(), 20*time.Second)
        switch sig {
        case syscall.SIGINT, syscall.SIGTERM:
            // stop
            log.Printf("stop")
            signal.Stop(ch)
            server.Shutdown(ctx)
            log.Printf("graceful shutdown")
            return
        case syscall.SIGUSR2:
            // reload
            log.Printf("reload")
            err := reload()
            if err != nil {
                log.Fatalf("graceful restart error: %v", err)
            }
            server.Shutdown(ctx)
            log.Printf("graceful reload")
            return
        }
    }
}

```

# systemd & supervisor
父进程退出之后，子进程会挂到1号进程上面。这种情况下使用systemd和supervisord等管理程序会显示进程处于failed的状态。解决这个问题有两个方法：
- 使用pidfile，每次进程重启更新一下pidfile，让进程管理者通过这个文件感知到mainpid的变更。
- 起一个master来管理服务进程，每次热重启master拉起一个新的进程，把旧的kill掉。这时master的pid没有变化，对于进程管理者来说进程处于正常的状态。[一个简洁的实现](https://github.com/kuangchanglang/graceful)


# References
- [graceful](https://github.com/kuangchanglang/graceful)
- [Graceful Restart in Golang](https://grisha.org/blog/2014/06/03/graceful-restart-in-golang/)  
- [facebookgo/grace](https://github.com/facebookgo/grace)
- [endless](https://github.com/fvbock/endless)
- [overseer](https://github.com/jpillora/overseer)
