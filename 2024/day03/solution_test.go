package day03

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input    = "./input.txt"
	example  = "./example.txt"
	example2 = "./example2.txt"
)

var (
	expr = regexp.MustCompile(`mul\(\d{1,3},\d{1,3}\)`)
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res string) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res += sc.Text()
	}
	return
}

func compute(s string) (res int) {
	for _, match := range expr.FindAllString(s, -1) {
		operands := strings.Split(match[4:len(match)-1], ",")
		m, _ := strconv.Atoi(operands[0])
		n, _ := strconv.Atoi(operands[1])
		res += m * n
	}
	return
}

func Solve(input string) (p1 int, p2 int) {
	p1 = compute(input)
	tmp2 := strings.Split(input, "don't()")
	newInput := tmp2[0]
	for _, s := range tmp2[1:] {
		remainder := strings.Split(s, "do()")
		if len(remainder) > 1 {
			newInput += strings.Join(remainder[1:], "")
		}
	}
	p2 = compute(newInput)
	return
}

func TestDay03(t *testing.T) {
	r := R.New(t)
	p1Ex, _ := Solve(ReadInput(example))
	r.Equal(161, p1Ex, "example p1")
	_, p2Ex := Solve(ReadInput(example2))
	r.Equal(48, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(173419328, p1, "input p1")
	r.Equal(90669332, p2, "input p2")
}

func BenchmarkDay03(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
