package day07

import (
	U "aoc/utils"
	"bufio"
	"fmt"
	"math"
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
func ReadInput(filepath string) (res [][]int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, U.Map(strings.Split(strings.Replace(sc.Text(), ":", "", -1), " "), U.ToInt))
	}
	return
}

func compute(operands []int, operators, wanted int, p2 bool) bool {
	res := operands[0]
	if len(operands) == 1 {
		return res == wanted
	}
	idx := 1
	div := 2
	if p2 {
		div = 3
	}
	for idx < len(operands) {
		operator := operators % div
		operators = operators / div
		if operator == 2 {
			res = U.ToInt(fmt.Sprintf("%d%d", res, operands[idx]))
		} else if operator == 1 {
			res *= operands[idx]
		} else {
			res += operands[idx]
		}
		if res > wanted {
			return false
		}
		idx++
	}
	return res == wanted
}

func Solve(input [][]int) (p1 int, p2 int) {
	for _, line := range input {
		wanted := line[0]
		operands := line[1:]
		nbOperators := float64(len(operands) - 1)
		nb := int(math.Pow(2, nbOperators))
		match := false
		for n := range nb {
			if compute(operands, n, wanted, false) {
				match = true
				break
			}
		}
		if match {
			p1 += wanted
			p2 += wanted
		} else {
			nb := int(math.Pow(3, nbOperators))
			match := false
			for n := range nb {
				if compute(operands, n, wanted, true) {
					match = true
					break
				}
			}
			if match {
				p2 += wanted
			}
		}
	}
	return
}

func TestDay07(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(3749, p1Ex, "example p1")
	r.Equal(11387, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(2314935962622, p1, "input p1")
	r.Equal(401477450831495, p2, "input p2")
}

func BenchmarkDay07(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
