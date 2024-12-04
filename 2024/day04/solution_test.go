package day04

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
	XMAS    = "XMAS"
	SAMX    = "SAMX"
)

var (
	MAS = []string{
		"MMSS",
		"MSSM",
		"SSMM",
		"SMMS",
	}
)

type coord struct {
	x, y int
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]rune) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, []rune(sc.Text()))
	}
	return
}

func inBounds(c coord, height, width int) bool {
	return 0 <= c.x && c.x < height && 0 <= c.y && c.y < width
}

func count(s string) (res int) {
	res += strings.Count(s, XMAS)
	res += strings.Count(s, SAMX)
	return
}

func diagonalNE(input [][]rune, h, w int, start coord) string {
	res := []rune{}
	cur := start
	for inBounds(cur, h, w) {
		res = append(res, input[cur.x][cur.y])
		cur = coord{cur.x + 1, cur.y - 1}
	}

	return string(res)
}

func diagonalNW(input [][]rune, h, w int, start coord) string {
	res := []rune{}
	cur := start
	for inBounds(cur, h, w) {
		res = append(res, input[cur.x][cur.y])
		cur = coord{cur.x + 1, cur.y + 1}
	}

	return string(res)
}

func Solve(input [][]rune) (p1 int, p2 int) {
	height, width := len(input), len(input[0])
	// horizontal
	for i := 0; i < height; i++ {
		p1 += count(string(input[i]))
	}
	// vertical
	for i := 0; i < width; i++ {
		buf := []rune{}
		for j := 0; j < height; j++ {
			buf = append(buf, input[j][i])
		}
		p1 += count(string(buf))
	}
	// diagonals
	for i := 0; i < height-3; i++ {
		p1 += count(diagonalNW(input, height, width, coord{i, 0}))
	}
	for i := 1; i < width-3; i++ {
		p1 += count(diagonalNW(input, height, width, coord{0, i}))
	}
	for i := 0; i < height-3; i++ {
		p1 += count(diagonalNE(input, height, width, coord{i, width - 1}))
	}
	for i := 3; i < width-1; i++ {
		p1 += count(diagonalNE(input, height, width, coord{0, i}))
	}

	for i := 1; i < height-1; i++ {
		for j := 1; j < width-1; j++ {
			if input[i][j] != 'A' {
				continue
			}
			if slices.Contains(MAS, string([]rune{input[i-1][j-1], input[i-1][j+1], input[i+1][j+1], input[i+1][j-1]})) {
				p2++
			}
		}
	}

	return
}

func TestDay04(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(18, p1Ex, "example p1")
	r.Equal(9, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(2427, p1, "input p1")
	r.Equal(1900, p2, "input p2")
}

func BenchmarkDay04(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
