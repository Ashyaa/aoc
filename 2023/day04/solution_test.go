package day04

import (
	"bufio"
	"os"
	"strconv"
	"strings"
	"testing"

	R "github.com/stretchr/testify/require"
)

const (
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

func SplitLines(s string) []string {
	var lines []string
	sc := bufio.NewScanner(strings.NewReader(s))
	for sc.Scan() {
		lines = append(lines, sc.Text())
	}
	return lines
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]int) {
	data, _ := os.ReadFile(filepath)
	for _, line := range SplitLines(string(data)) {
		l := strings.ReplaceAll(line, "  ", " ")
		idx := strings.Index(l, ": ")
		numbers := l[idx+2:]
		ints := []int{}
		for _, str_n := range strings.Split(numbers, " ") {
			if str_n == "|" {
				ints = append(ints, -1)
				continue
			}
			n, _ := strconv.Atoi(str_n)
			ints = append(ints, n)
		}
		res = append(res, ints)
	}
	return
}

func Solve(input [][]int) (p1, p2 int) {
	matches := make([]int, len(input))
	for idx := len(input) - 1; idx >= 0; idx-- {
		game := input[idx]
		card := map[int]bool{}
		cardEnd := false
		nbMatches := -1
		for _, n := range game {
			if n < 0 {
				cardEnd = true
				continue
			}
			if _, match := card[n]; cardEnd && match {
				nbMatches += 1
			} else if !cardEnd {
				card[n] = true
			}
		}
		if nbMatches >= 0 {
			p1 += 1 << nbMatches
		}
		matches[idx] = nbMatches + 1
		copies := 0
		for other := matches[idx]; other > 0; other-- {
			copies += matches[idx+other]
		}
		matches[idx] = 1 + copies
		p2 += matches[idx]
	}
	return
}

func TestDay04(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	input := ReadInput(inputFile)
	p1, p2 := Solve(example)
	r.Equal(13, p1)
	r.Equal(30, p2)
	p1, p2 = Solve(input)
	r.Equal(23678, p1)
	r.Equal(15455663, p2)
}

func BenchmarkDay04(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(inputFile))
	}
}
