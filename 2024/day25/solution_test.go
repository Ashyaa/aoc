package day25

import (
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
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (keys, locks [][]int) {
	raw, _ := os.ReadFile(filepath)
	for _, schema := range strings.Split(string(raw), "\n\n") {
		lines := strings.Split(schema, "\n")
		buf := []int{}
		for j := range len(lines[0]) {
			s := []rune{}
			for i := range len(lines) {
				s = append(s, []rune(lines[i])[j])
			}
			buf = append(buf, strings.Count(string(s), "#")-1)
		}
		if schema[0] == '.' { // key
			keys = append(keys, buf)
		} else { // lock
			locks = append(locks, buf)
		}
	}
	return
}

func matches(key, lock []int) bool {
	for i, k := range key {
		l := lock[i]
		if k+l > 5 {
			return false
		}
	}
	return true
}

func Solve(keys, locks [][]int) (p1 int, p2 int) {
	for _, key := range keys {
		for _, lock := range locks {
			if matches(key, lock) {
				p1++
			}
		}
	}
	return
}

func TestDay25(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(3, p1Ex, "example p1")
	r.Equal(0, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(3508, p1, "input p1")
	r.Equal(0, p2, "input p2")
}

func BenchmarkDay25(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
