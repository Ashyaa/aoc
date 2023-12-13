package day13

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

func nbDiffs(a, b string) (res int) {
	for i := range a {
		if a[i] != b[i] {
			res++
		}
	}
	return
}

func count(lines []string) (p1, p2 int) {
	lastLine := len(lines) - 1
	runeColumns := make([][]rune, len(lines[0]))
	for i := range runeColumns {
		runeColumns[i] = make([]rune, len(lines))
	}
	for idx, line := range lines {
		for j, c := range line {
			runeColumns[j] = append(runeColumns[j], c)
		}
		if idx == lastLine {
			break
		}
		halfSize := min(idx+1, lastLine-idx)
		diffs := 0
		for i := 0; i < halfSize; i++ {
			diffs += nbDiffs(lines[idx-i], lines[idx+1+i])
		}
		if diffs == 0 {
			p1 = (idx + 1) * 100
		} else if diffs == 1 {
			p2 = (idx + 1) * 100
		}
	}
	columns := []string{}
	for _, col := range runeColumns {
		columns = append(columns, string(col))
	}
	lastCol := len(columns) - 1
	for idx := range columns {
		if idx == lastCol {
			break
		}
		halfSize := min(idx+1, lastCol-idx)
		diffs := 0
		for i := 0; i < halfSize; i++ {
			diffs += nbDiffs(columns[idx-i], columns[idx+1+i])
		}
		if diffs == 0 {
			p1 = idx + 1
		} else if diffs == 1 {
			p2 = idx + 1
		}
	}
	return
}

func Solve(filepath string) (p1 int, p2 int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	lines := []string{}
	for sc.Scan() {
		line := sc.Text()
		if line != "" {
			lines = append(lines, line)
			continue
		}
		x, y := count(lines)
		p1, p2 = p1+x, p2+y
		lines = []string{}
	}
	x, y := count(lines)
	p1, p2 = p1+x, p2+y
	return
}

func TestDay13(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(example)
	r.Equal(405, p1Ex, "example p1")
	r.Equal(400, p2Ex, "example p2")
	p1, p2 := Solve(input)
	r.Equal(37113, p1, "input p1")
	r.Equal(30449, p2, "input p2")
}

func BenchmarkDay13(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(input)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
