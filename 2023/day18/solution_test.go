package day18

import (
	"bufio"
	"fmt"
	"os"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []string) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		// parsing here...
		res = append(res, sc.Text())
	}
	return
}

func Solve(input []string) (p1 int, p2 int) {
	return
}

func TestDay18(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(0, p1Ex, "example p1")
	r.Equal(0, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(0, p1, "input p1")
	r.Equal(0, p2, "input p2")
}

func BenchmarkDay18(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
