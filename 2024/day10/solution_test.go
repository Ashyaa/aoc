package day10

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

func runeToInt(r rune) int {
	return U.ToInt(string(r))
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (U.Matrix[int], []U.Coord) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	buf := make([][]int, 0)
	x := 0
	starts := []U.Coord{}

	for sc.Scan() {
		line := U.Map([]rune(sc.Text()), runeToInt)
		for y, r := range line {
			if r == 0 {
				starts = append(starts, U.Coord{X: x, Y: y})
			}
		}
		buf = append(buf, line)
		x++
	}
	return U.NewMatrix(buf), starts
}

func Solve(mapp U.Matrix[int], starts []U.Coord) (p1 int, p2 int) {
	mapp.SetNeighboursFunc(func(i, j int) (res [][2]int) {
		curVal := mapp.At(i, j)
		for _, coords := range U.CardinalNeighbours(i, j) {
			ni, nj := coords[0], coords[1]
			if mapp.InBounds(ni, nj) && mapp.At(ni, nj) == curVal+1 {
				res = append(res, [2]int{ni, nj})
			}
		}
		return
	})
	for _, start := range starts {
		q1 := U.Queue[U.Coord]{}
		q2 := U.Queue[U.Coord]{}
		q1.Push(start)
		q2.Push(start)
		for !q1.IsEmpty() {
			cur := q1.Pop()
			if mapp.At(cur.X, cur.Y) == 9 {
				p1++
				continue
			}
			for _, coords := range mapp.Neighbours(cur.X, cur.Y) {
				c := U.Coord{X: coords.X, Y: coords.Y}
				if !slices.Contains(q1, c) {
					q1.Push(c)
				}
			}
		}
		for !q2.IsEmpty() {
			cur := q2.Pop()
			if mapp.At(cur.X, cur.Y) == 9 {
				p2++
				continue
			}
			for _, coords := range mapp.Neighbours(cur.X, cur.Y) {
				c := U.Coord{X: coords.X, Y: coords.Y}
				q2.Push(c)
			}
		}
	}
	return
}

func TestDay10(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(36, p1Ex, "example p1")
	r.Equal(81, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(472, p1, "input p1")
	r.Equal(969, p2, "input p2")
}

func BenchmarkDay10(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
