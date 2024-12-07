package day06

import (
	U "aoc/utils"
	"bufio"
	"fmt"
	"os"
	"slices"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

var (
	directions = []U.Coord{
		{X: -1, Y: 0, Z: 0},
		{X: 0, Y: 1, Z: 0},
		{X: 1, Y: 0, Z: 0},
		{X: 0, Y: -1, Z: 0},
	}
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (U.Matrix[rune], U.Coord) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	buf := make([][]rune, 0)
	x := 0
	var start U.Coord
	for sc.Scan() {
		line := []rune(sc.Text())
		if y := slices.Index(line, '^'); y >= 0 {
			start.X = x
			start.Y = y
			line[y] = '.'
		}
		buf = append(buf, line)
		x++
	}
	return U.NewMatrix(buf), start
}

func Loops(mapp U.Matrix[rune], start U.Coord) bool {
	current := U.Coord{X: start.X, Y: start.Y, Z: (start.Z + 1) % 4}
	dir := directions[current.Z]
	visited := U.Set[U.Coord]{}
	for mapp.InBounds(current.X, current.Y) {
		if visited.Contains(current) {
			return true
		}
		visited.Add(current)
		next := U.Coord{X: current.X + dir.X, Y: current.Y + dir.Y, Z: current.Z} // move forward
		if !mapp.InBounds(next.X, next.Y) {                                       // exit on leaving the map
			break
		}
		for mapp.At(next.X, next.Y) == '#' { // turn right on obstacle
			newZ := (next.Z + 1) % 4
			dir = directions[newZ]
			next = U.Coord{X: current.X + dir.X, Y: current.Y + dir.Y, Z: newZ}
		}
		current = next
	}

	return false
}

func Solve(mapp U.Matrix[rune], start U.Coord) (_ int, p2 int) {
	visited := U.Set[int]{}
	getId := func(c U.Coord) int {
		return c.X*mapp.Columns() + c.Y
	}
	current := start
	dir := directions[start.Z]
	for mapp.InBounds(current.X, current.Y) {
		visited.Add(getId(current))
		next := U.Coord{X: current.X + dir.X, Y: current.Y + dir.Y, Z: current.Z} // move forward
		if !mapp.InBounds(next.X, next.Y) {                                       // exit on leaving the map
			break
		}
		for mapp.At(next.X, next.Y) == '#' { // turn right on obstacle
			newZ := (next.Z + 1) % 4
			dir = directions[newZ]
			next = U.Coord{X: current.X + dir.X, Y: current.Y + dir.Y, Z: newZ}
		}
		if !visited.Contains(getId(next)) {
			mapp.Set(next.X, next.Y, '#')
			if Loops(mapp, current) {
				p2++
			}
			mapp.Set(next.X, next.Y, '.')
		}

		current = next
	}
	return len(visited), p2
}

func TestDay06(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(41, p1Ex, "example p1")
	r.Equal(6, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(5331, p1, "input p1")
	r.Equal(1812, p2, "input p2")
}

func BenchmarkDay06(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
