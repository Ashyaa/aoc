package day14

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
	rob     = '■'
)

type robot struct {
	p, v Coord
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []robot) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		frags := strings.Split(sc.Text(), " ")
		res = append(res, robot{
			p: ToCoords(frags[0][2:], ","),
			v: ToCoords(frags[1][2:], ","),
		})
	}
	return
}

func simulate(rob robot, width, height, seconds int) (res Coord) {
	res.X = (rob.p.X + seconds*rob.v.X) % width
	if res.X < 0 {
		res.X += width
	}
	res.Y = (rob.p.Y + seconds*rob.v.Y) % height
	if res.Y < 0 {
		res.Y += height
	}
	return
}

func default_line(width int) (res []rune) {
	for range width {
		res = append(res, ' ')
	}
	return
}

func isTree(rbs []Coord, height, width int) bool {
	runes := make([][]rune, 0)
	for range height {
		runes = append(runes, default_line(width))
	}
	for _, rb := range rbs {
		runes[rb.Y][rb.X] = rob
	}
	res := ""
	for _, line := range runes {
		s := string(line) + "\n"
		if strings.Contains(s, "■■■■■■■■■■■■■■■■■■■■■■■") {
			return true
		}
		res += s
	}
	return false
}

func Solve(input []robot, width, height int) (p1 int, p2 int) {
	hMid := (width / 2)
	vMid := (height / 2)
	quadrants := []int{0, 0, 0, 0}

	getQuadrant := func(c Coord) int {
		if c.X == hMid || c.Y == vMid {
			return -1
		}
		left := 0
		if c.X > hMid {
			left = 1
		}
		up := 0
		if c.Y > vMid {
			up = 2
		}
		return left + up
	}

	for _, rob := range input {
		final := simulate(rob, width, height, 100)
		idx := getQuadrant(final)
		if idx >= 0 {
			quadrants[idx]++
		}
	}
	p1 = Reduce(quadrants, nil, func(a, b int) int { return a * b })
	if width < 100 {
		return
	}

	for i := 101; i <= 10_000; i++ {
		state := []Coord{}
		for _, rob := range input {
			final := simulate(rob, width, height, i)
			state = append(state, final)
		}
		if isTree(state, height, width) {
			p2 = i
			break
		}
	}

	return
}

func TestDay14(t *testing.T) {
	r := R.New(t)
	p1Ex, _ := Solve(ReadInput(example), 11, 7)
	r.Equal(12, p1Ex, "example p1")
	p1, p2 := Solve(ReadInput(input), 101, 103)
	r.Equal(225943500, p1, "input p1")
	r.Equal(6377, p2, "input p2")
}

func BenchmarkDay14(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input), 101, 103)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
