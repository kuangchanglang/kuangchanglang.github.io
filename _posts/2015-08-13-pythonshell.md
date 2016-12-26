---
layout: post
title:  "python执行shell（管道传输数据）"
date: 2015-8-13 22:05:24 
categories: jekyll update
---
这个问题搞了大半天，傻逼了。   
  
#背景
需求是这样的，分析日志，找到最新一条包含xxx的数据（xxx由用户输入）。  

#cat和tac  
日志最新的内容在最后面。简单地，   
``grep "xxx" logfile | tail -n 1``  
或   
``cat logfile | grep "xxx" | tail -n 1``  

然而，日志文件总共5千多万行，每次操作用时5s左右（第一次10秒，后面稳定在5s，系统缓存屌屌的）。  
改进一下，使用tac（cat的妹妹）：  
``tac logfile | grep "xxx" -m 1``  
tac从尾部开始读，将内容写到管道中。grep -m操作表示匹配到几次停止。  

##时间对比
对于全文件扫描，cat需要5s，tac需要15s。  因此，有以下两种情况：  
1.搜索的内容在文件比较前面或者不存在，tac比较慢
2.搜索的内容在文件的比较后面，实用cat再grep时间保持恒定5s左右，实用tac再grep毫秒级。
所以看应用场景了，如果用户搜索的内容基本都是匹配的，tac效率高很多。

##why？
啰嗦一点，一个从头部遍历，一个从尾部遍历。时间效率差在哪里？就是寻道时间啦。文件操作主要耗时在于两个时间：seek time（寻道时间），transfer time（传输到内存的时间）。对于cat，从文件头开始，每次读取一块固定（缓存）大小的内容，读完了继续读，磁臂刚好停在下面要读的位置。而对于tac，得先找文件末尾，每次后退缓存大小的位置，读一个缓存大小的内容，完了再寻道回去。  
用top命令观察cat和tac执行过程时使用的内容，整个执行过程占用的内容保持不变，98.5M，应该差不多就是其缓存大小。

#管道
管道用于进程间通信，linux中其实是个文件。简单理解就是一个进程往管道里面写内容，一个进程从管道里面读内容。  
``tac logfile | grep "xxx" -m 1``   
tac和grep分别在两个进程中执行，并且是同时进行的（不是先tac完了grep才开始）。所以当grep找到内容时便进程执行结束，关闭读管道，tac会收到SIGPIPE 信号，tac这时也停止。所以说如果搜索内容在文件末尾处这种方法会非常快。  

#python信号坑
前面都很顺利，坑在python。  
因为这个功能要对外提供服务，总不能用shell来完成。写了个python的http服务，调用shell。  
python调用shell的方法也是有点多：  
*     os.system()  
*     subprocess.call()  
*     subprocess.Popen()  
*     os.popen()  
*     commands.getstatusoutput()  
  
system()和call()不能得到shell的返回结果。poen()和getstatusouput()不知是单进程执行还是什么原因，调用上面的方法大概15s，也就是全文件扫描的时间。  
最后在官方文档找到的方法是用Popen()，可以获取结果，并且可以通过管道达到并行的效果：

```python

 proc1 = subprocess.Popen(['tac', filename], stdout=subprocess.PIPE, preexec_fn = lambda: signal(SIGPIPE, SIG_DFL))
 proc2 = subprocess.Popen(['grep', '-m', '1', "url.*sauth.*%s" % channel], stdin=proc1.stdout, stdout=subprocess.PIPE)
                           proc1.stdout.close() # allow p1 to receive a SIGPIPE if p2 exists.
 content, err = proc2.communicate()
```

一开始没有加preexec_fn = lambda: signal(SIGPIPE, SIG_DFL)这个参数，后果就是grep是可以很快拿到结果，但是tac还没有结束，仍在坚持往前读文件。等他执行完了会报一个tac: write error。因为grep进程已经结束了，管道已经关了。  
`` proc1.stdout.close() # allow p1 to receive a SIGPIPE if p2 exists. ``  
这一行也然并卵，最后在stackoverflow上找到答案。python解释器将管道错误已异常形式抛出，将SIGPIPE信号的处理方式改为SIG_IGN（忽略），而tac进程是由python fork出来的，继承其信号，收到SIG_PIPE并没有退出程序，还在猛跑。    
  
 preexec_fn = lambda: signal(SIGPIPE, SIG_DFL)，这一行在进程开始时执行，将SIGPIPE信号的处理方式设为系统默认（default），这样他收到信号就可以正常退出了。  

就这样吧，下班回家。  
  
还试过python从尾部往前读文件再用正则匹配，巨慢。python io有这么慢吗？

References：  
https://docs.python.org/2/library/subprocess.html  
http://stackoverflow.com/questions/10479825/python-subprocess-call-broken-pipe  

