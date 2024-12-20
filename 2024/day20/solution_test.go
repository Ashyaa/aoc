package day20

import (
	. "aoc/utils"
	"bufio"
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
func ReadInput(filepath string) (res Matrix[rune], start Coord, example bool) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	buf := make([][]rune, 0)
	x := 0
	for sc.Scan() {
		line := sc.Text()
		if y := strings.Index(line, "S"); y > 0 {
			start.X = x
			start.Y = y
		}
		buf = append(buf, []rune(line))
		x += 1
	}
	return NewMatrix(buf), start, strings.Contains(filepath, "example")
}

func getPath(input Matrix[rune], start Coord) (res []Coord) {
	current := start
	history := make(map[Coord]int)
	idx := 0
	for input.At(current.X, current.Y) != 'E' {
		res = append(res, current)
		history[current] = idx
		idx++
		for _, n := range input.Neighbours(current.X, current.Y) {
			if n.Value == '#' {
				continue
			}

			if _, ok := history[Coord{X: n.X, Y: n.Y}]; !ok {
				current = Coord{X: n.X, Y: n.Y}
				break
			}
		}
	}
	res = append(res, current)
	return res
}

func absInt(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func manhattan(start, end Coord) int {
	return absInt(start.X-end.X) + absInt(start.Y-end.Y)
}

func Solve(input Matrix[rune], start Coord, example bool) (p1 int, p2 int) {
	pth := getPath(input, start)
	p2Threshold := 100
	if example {
		p2Threshold = 50
	}

	for i := 0; i < len(pth); i++ {
		for j := i + 3; j < len(pth); j++ {
			start, end := pth[i], pth[j]
			dist := manhattan(start, end)
			if dist == 2 && j-i-2 >= 100 {
				p1++
			}
			if dist <= 20 && j-i-dist >= p2Threshold {
				p2++
			}
		}
	}
	return
}

func TestDay20(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(0, p1Ex, "example p1")
	r.Equal(285, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(1399, p1, "input p1")
	r.Equal(994807, p2, "input p2")
}

func BenchmarkDay20(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
