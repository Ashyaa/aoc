package day02

import (
	"aoc/utils"
	"bufio"
	"fmt"
	"os"
	"strconv"
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
func ReadInput(filepath string) (res [][]int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)

	toInt := func(s string) int {
		res, _ := strconv.Atoi(s)
		return res
	}

	for sc.Scan() {
		// parsing here...
		res = append(res, utils.Map(strings.Split(sc.Text(), " "), toInt))
	}
	return
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func isDistanceSafe(n1, n2 int) bool {
	dist := abs(n1 - n2)
	if dist == 0 || dist > 3 {
		return false
	}
	return true
}

func isSafe(series []int) bool {
	n0 := series[0]
	nj := series[1]
	if !isDistanceSafe(n0, nj) {
		return false
	}
	increasing := n0 < nj
	for i := 2; i < len(series); i++ {
		n := series[i]
		if !isDistanceSafe(n, nj) {
			return false
		}
		if (nj < n) != increasing {
			return false
		}
		nj = n
	}
	return true
}

func Solve(input [][]int) (p1 int, p2 int) {
	for _, series := range input {
		if isSafe(series) {
			p1++
			p2++
		} else {
			for i := range len(series) {
				s := append([]int{}, series[:i]...)
				s = append(s, series[i+1:]...)
				if isSafe(s) {
					p2++
					break
				}
			}
		}
	}
	return
}

func TestDay02(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(2, p1Ex, "example p1")
	r.Equal(4, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(402, p1, "input p1")
	r.Equal(455, p2, "input p2")
}

func BenchmarkDay02(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
