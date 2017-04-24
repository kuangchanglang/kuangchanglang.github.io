package main

import (
	"flag"
	"fmt"
	"strconv"
	"sync"
)

const num = 30

var count = 2

func fib(n int) int {
	if n <= 0 {
		return 0
	}
	if n < 2 {
		return 1
	}
	return fib(n-1) + fib(n-2)
}

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
			fmt.Println(fib(num))
			wg.Done()
		}()
	}
	wg.Wait()
}
