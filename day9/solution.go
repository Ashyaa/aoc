package day9

import (
	"container/list"
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
	"time"
)

var input = "./input.txt"

const maxuint64 = ^uint64(0)
const minuint64 = uint64(0)

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}

// Min of a queue
func Min(queue *list.List) uint64 {
	min := queue.Front().Value.(uint64)
	for e := queue.Front().Next(); e != nil; e = e.Next() {
		if e.Value.(uint64) < min {
			min = e.Value.(uint64)
		}
	}
	return min
}

// Max of a queue
func Max(queue *list.List) uint64 {
	max := queue.Front().Value.(uint64)
	for e := queue.Front().Next(); e != nil; e = e.Next() {
		if e.Value.(uint64) > max {
			max = e.Value.(uint64)
		}
	}
	return max
}

// ReadInput retrieves the content of the input file
func ReadInput() (res []uint64) {
	data, _ := ioutil.ReadFile(input)
	for _, line := range strings.Split(strings.TrimRight(string(data), "\n"), "\n") {
		n, _ := strconv.ParseUint(line, 10, 64)
		res = append(res, n)
	}
	return
}

func isValid(n uint64, numbers []uint64) bool {
	set := make(map[uint64]bool)
	for _, k := range numbers {
		set[k] = true
	}
	for _, k := range numbers {
		if _, ok := set[n-k]; n != 2*k && ok {
			return true
		}
	}
	return false
}

// Step1 solves step 1
func Step1(numbers []uint64) uint64 {
	defer timeTrack(time.Now(), "Step 1")
	queue := numbers[:25]
	for _, n := range numbers[25:] {
		if n == 14360655 {
			fmt.Println("")
		}
		if !isValid(n, queue) {
			return n
		}
		queue = append(queue[1:], n)
	}
	return 0
}

// Step2 solves step 2
func Step2(numbers []uint64, wanted uint64) uint64 {
	defer timeTrack(time.Now(), "Step 2")
	queue, acc := list.New(), uint64(0)
	for _, n := range numbers {
		if n >= wanted {
			queue, acc = list.New(), 0
			continue
		}
		acc += n
		queue.PushFront(n)
		if acc == wanted {
			return Min(queue) + Max(queue)
		}
		for acc >= wanted {
			val := queue.Back().Value.(uint64)
			acc -= val
			queue.Remove(queue.Back())
		}
	}
	return 0
}
