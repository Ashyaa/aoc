package day09

import (
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
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		arr := make([]int, 0)
		for _, f := range strings.Fields(sc.Text()) {
			n, _ := strconv.Atoi(f)
			arr = append(arr, n)
		}
		res = append(res, arr)
	}
	return
}

func sum(arr []int) (res int) {
	for _, n := range arr {
		res += n
	}
	return
}

func sub(arr []int) (res int) {
	for idx := len(arr) - 1; idx >= 0; idx-- {
		res = arr[idx] - res
	}
	return
}

func Solve(input [][]int) (p1, p2 int) {
	for _, arr := range input {
		buffer := append([]int{}, arr...)
		stackp1, stackp2 := []int{}, []int{}
		for {
			diffs := []int{}
			zeroes := 0
			stackp1 = append(stackp1, buffer[len(buffer)-1])
			stackp2 = append(stackp2, buffer[0])
			for idx := 1; idx < len(buffer); idx++ {
				diff := buffer[idx] - buffer[idx-1]
				if diff == 0 {
					zeroes += 1
				}
				diffs = append(diffs, diff)
			}
			if zeroes == len(diffs) {
				stackp2 = append(stackp2, 0)
				break
			}
			buffer = diffs
		}
		p1 += sum(stackp1)
		p2 += sub(stackp2)
	}
	return
}

func TestDay09(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	input := ReadInput(inputFile)
	p1, p2 := Solve(example)
	r.Equal(114, p1, "example p1")
	r.Equal(2, p2, "example p2")
	p1, p2 = Solve(input)
	r.Equal(2043677056, p1, "input p1")
	r.Equal(1062, p2, "input p2")
}

func BenchmarkDay09(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(inputFile))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
