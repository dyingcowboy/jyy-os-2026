package main

import (
	"fmt"
	"math/rand"
	"time"
)

const THREADS = 1_000_000
const COUNT = 10_000_000

func T_worker(name int, ch chan<- string, done <-chan struct{}) {
	i := 0
	for {
		i++
		select {
		case ch <- fmt.Sprintf("[%d] i = %d", name, i):
		case <-done:
			return
		}
	}
}

func main() {
	channels := make([]chan string, THREADS)
	done := make(chan struct{})

	for i := range THREADS {
		channels[i] = make(chan string, 1)
		go T_worker(i, channels[i], done)
	}

	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	for count := 0; count < COUNT; count++ {
		idx := r.Intn(THREADS)
		res := <-channels[idx]
		fmt.Println(res)
	}
	close(done)
}
