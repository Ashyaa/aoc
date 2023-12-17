package day16

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	up = iota
	right
	down
	left
	input   = "./input.txt"
	example = "./example.txt"
)

func move(x, y, nbLines, nbCols, direction int) (int, int, bool) {
	var nx, ny int
	switch direction {
	case up:
		nx, ny = x-1, y
	case right:
		nx, ny = x, y+1
	case down:
		nx, ny = x+1, y
	case left:
		nx, ny = x, y-1
	}
	ok := 0 <= nx && nx < nbLines && 0 <= ny && ny < nbCols
	return nx, ny, ok
}

func rays(input [][]rune, x, y, dir int) (res []int) {
	lines, cols := len(input), len(input[0])
	switch input[x][y] {
	case '-':
		switch dir {
		case up, down:
			if nx, ny, ok := move(x, y, lines, cols, right); ok {
				res = append(res, nx, ny, right)
			}
			if nx, ny, ok := move(x, y, lines, cols, left); ok {
				res = append(res, nx, ny, left)
			}
			res = append(res, x, y, -1)
		case left, right:
			if nx, ny, ok := move(x, y, lines, cols, dir); ok {
				res = append(res, nx, ny, dir)
			}
		}
	case '|':
		switch dir {
		case left, right:
			if nx, ny, ok := move(x, y, lines, cols, up); ok {
				res = append(res, nx, ny, up)
			}
			if nx, ny, ok := move(x, y, lines, cols, down); ok {
				res = append(res, nx, ny, down)
			}
			res = append(res, x, y, -1)
		case up, down:
			if nx, ny, ok := move(x, y, lines, cols, dir); ok {
				res = append(res, nx, ny, dir)
			}
		}
	case '/':
		res = append(res, x, y, -1)
		switch dir {
		case up:
			if nx, ny, ok := move(x, y, lines, cols, right); ok {
				res = append(res, nx, ny, right)
			}
		case left:
			if nx, ny, ok := move(x, y, lines, cols, down); ok {
				res = append(res, nx, ny, down)
			}
		case down:
			if nx, ny, ok := move(x, y, lines, cols, left); ok {
				res = append(res, nx, ny, left)
			}
		case right:
			if nx, ny, ok := move(x, y, lines, cols, up); ok {
				res = append(res, nx, ny, up)
			}
		}
	case '\\':
		res = append(res, x, y, -1)
		switch dir {
		case up:
			if nx, ny, ok := move(x, y, lines, cols, left); ok {
				res = append(res, nx, ny, left)
			}
		case left:
			if nx, ny, ok := move(x, y, lines, cols, up); ok {
				res = append(res, nx, ny, up)
			}
		case down:
			if nx, ny, ok := move(x, y, lines, cols, right); ok {
				res = append(res, nx, ny, right)
			}
		case right:
			if nx, ny, ok := move(x, y, lines, cols, down); ok {
				res = append(res, nx, ny, down)
			}
		}
	}
	return
}

func fill(input [][]rune, x, y, dir int) int {
	seen := make(map[string]bool)
	energized := make(map[string]bool)
	lines, cols := len(input), len(input[0])
	q := []int{x, y, dir}

	for len(q) > 0 {
		x := q[0]
		y := q[1]
		dir := q[2]
		pos := strconv.Itoa(x) + "." + strconv.Itoa(y)
		ray := pos + "." + strconv.Itoa(dir)
		q = q[3:]
		if _, ok := seen[ray]; ok {
			continue
		}
		energized[pos] = true
		seen[ray] = true
		if input[x][y] == '.' {
			nx, ny, ok := move(x, y, lines, cols, dir)
			if !ok {
				continue
			}
			q = append(q, nx, ny, dir)
		} else {
			q = append(q, rays(input, x, y, dir)...)
		}

	}
	// display(seen, input)
	return len(energized)
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]rune) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		line := sc.Text()
		res = append(res, []rune(line))
	}
	return
}

func Solve(input [][]rune) (int, int) {
	res := []int{}
	for i := 0; i < len(input); i++ {
		res = append(res, fill(input, i, 0, right))
		res = append(res, fill(input, i, len(input[0])-1, left))
	}
	for i := 0; i < len(input[0]); i++ {
		res = append(res, fill(input, 0, i, down))
		res = append(res, fill(input, len(input)-1, i, up))
	}
	return res[0], slices.Max(res)
}

func TestDay16(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(46, p1Ex, "example p1")
	r.Equal(51, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(8551, p1, "input p1")
	r.Equal(8754, p2, "input p2")
}

func BenchmarkDay16(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
