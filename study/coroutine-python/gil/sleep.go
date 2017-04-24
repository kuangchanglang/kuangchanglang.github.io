package main

import (
	"flag"
	"strconv"
	"sync"
	"time"
)

var count = 2

func main() {
	flag.Parse()
	args := flag.Args()
	if len(args) > 0 {
		count, _ = strconv.Atoi(args[0])
	}

	var wg sync.WaitGroup
	for i := 0; i < count; i++ {
		wg.Add(1)
		go func() {
			time.Sleep(3 * time.Second)
			wg.Done()
		}()
	}
	wg.Wait()
}
