package day12

import (
	U "aoc/utils"
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

var (
	directions = []U.Coord{
		{X: -1, Y: 0},
		{X: 0, Y: 1},
		{X: 1, Y: 0},
		{X: 0, Y: -1},
	}
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) U.Matrix[rune] {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	buf := [][]rune{}
	for sc.Scan() {
		// parsing here...
		buf = append(buf, []rune(sc.Text()))
	}
	return U.NewMatrix(buf)
}

func floodFill(input U.Matrix[rune], start U.Coord) U.Set[U.Coord] {
	visited := U.Set[U.Coord]{}
	plant := input.At(start.X, start.Y)
	q := U.Queue[U.Coord]{start}

	for len(q) > 0 {
		current := q.Pop()
		if visited.Contains(current) {
			continue
		}
		visited.Add(current)

		for _, other := range input.Neighbours(current.X, current.Y) {
			if other.Value != plant {
				continue
			}
			q.Push(U.Coord{X: other.X, Y: other.Y})
		}
	}
	return visited
}

func nbSides(sides []U.Coord) int {
	buffer := sides
	res := [][]U.Coord{}
	for len(buffer) > 0 {
		side := buffer[0]
		buffer = buffer[1:]
		vertical := side.Z%2 != 0
		ax, min, max := side.X, side.Y, side.Y
		if vertical {
			ax, min, max = side.Y, side.X, side.X
		}
		sideList := []U.Coord{side}
		remainder := []U.Coord{}
		ok := true
		for ok {
			sideLen := len(sideList)
			for _, other := range buffer {
				add := false
				if other.Z != side.Z {
					remainder = append(remainder, other)
					continue
				}
				if vertical && other.Y == ax {
					if other.X == max+1 {
						max = max + 1
						add = true
					} else if other.X == min-1 {
						min = min - 1
						add = true
					}
				} else if !vertical && other.X == ax {
					if other.Y == max+1 {
						max = max + 1
						add = true
					} else if other.Y == min-1 {
						min = min - 1
						add = true
					}
				}
				if add {
					sideList = append(sideList, other)
				} else {
					remainder = append(remainder, other)
				}
			}
			ok = sideLen != len(sideList)
			buffer = remainder
			remainder = []U.Coord{}
		}
		res = append(res, sideList)
	}
	return len(res)
}

func perimeter(input U.Matrix[rune], region U.Set[U.Coord]) (int, int) {
	plant := '.'
	sides := []U.Coord{}
	for current := range region {
		if plant == '.' {
			plant = input.At(current.X, current.Y)
		}
		for idx, dir := range directions {
			nx, ny := current.X+dir.X, current.Y+dir.Y
			if !input.InBounds(nx, ny) || input.At(nx, ny) != plant {
				sides = append(sides, U.Coord{X: current.X, Y: current.Y, Z: idx})
			}
		}
	}

	res := len(sides)
	return res, nbSides(sides)
}

func Solve(input U.Matrix[rune]) (p1 int, p2 int) {
	visited := U.Set[U.Coord]{}
	for i := range input.Lines() {
		for j := range input.Columns() {
			current := U.Coord{X: i, Y: j}
			if visited.Contains(current) {
				continue
			}
			region := floodFill(input, current)
			perim, sides := perimeter(input, region)
			p1 += len(region) * perim
			p2 += len(region) * sides
			visited = visited.Union(region)
		}
	}
	return
}

func TestDay12(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(1930, p1Ex, "example p1")
	r.Equal(1206, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(1437300, p1, "input p1")
	r.Equal(849332, p2, "input p2")
}

func BenchmarkDay12(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
