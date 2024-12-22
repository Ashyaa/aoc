package day22

import (
	. "aoc/utils"
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
	p       = (1 << 24) - 1 // bitmask for 24 bits integers
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []int) {
	raw, _ := os.ReadFile(filepath)
	return Map(strings.Split(string(raw), "\n"), ToInt)
}

func compute(n int) int {
	k := ((n << 6) ^ n) & p
	m := ((k >> 5) ^ k) // mask not needed here, all integers are 4bits or less
	return ((m << 11) ^ m) & p
}

func predict(n int, cache map[[4]int]int) int {
	current := n
	diffs := NewQueue[int]()
	seen := NewSet[[4]int]()
	for range 2000 {
		next := compute(current)
		price := (next % 10)
		diffs.Push(price - (current % 10))
		if diffs.Len() > 4 {
			diffs.Pop()
		}
		if diffs.Len() == 4 {
			sequence := [4]int(diffs)
			if !seen.Contains(sequence) {
				cache[sequence] += price
				seen.Add(sequence)
			}
		}
		current = next
	}

	return current
}

func Solve(input []int) (p1 int, p2 int) {
	cache := make(map[[4]int]int)
	for _, n := range input {
		p1 += predict(n, cache)
	}

	for _, v := range cache {
		p2 = max(p2, v)
	}

	return
}

func TestDay22(t *testing.T) {
	r := R.New(t)
	p1Ex, _ := Solve(ReadInput(example))
	r.Equal(37327623, p1Ex, "example p1")
	_, p2Ex := Solve([]int{1, 2, 3, 2024})
	r.Equal(23, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(15613157363, p1, "input p1")
	r.Equal(1784, p2, "input p2")
}

func BenchmarkDay22(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
