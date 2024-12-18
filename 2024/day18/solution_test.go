package day18

import (
	. "aoc/utils"
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
	offsets = []Coord{
		{X: -1, Y: -1},
		{X: -1, Y: 0},
		{X: -1, Y: 1},
		{X: 0, Y: -1},
		{X: 0, Y: 1},
		{X: 1, Y: -1},
		{X: 1, Y: 0},
		{X: 1, Y: 1},
	}
)

func Neighbours(c Coord) (res []Coord) {
	for _, o := range offsets {
		res = append(res, Coord{X: c.X + o.X, Y: c.Y + o.Y})
	}
	return
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []Coord) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, ToCoordsComma(sc.Text()))
	}
	return
}

func initMatrix(n int) Matrix[int] {
	buf := make([][]int, 0)
	for range n {
		buf = append(buf, make([]int, n))
	}
	return NewMatrix(buf)
}

func currentWalls(walls []Coord, step int) Set[Coord] {
	res := make(Set[Coord])
	nb := min(step, len(walls)-1)
	res.Add(walls[:nb]...)
	return res
}

func aStar(m Matrix[int], walls []Coord, p1 int) int {
	start := Coord{X: 0, Y: 0}
	n := m.Lines()
	end := Coord{X: n - 1, Y: n - 1}

	totalRisk := make([][]int, 0)
	for range n {
		totalRisk = append(totalRisk, make([]int, n))
	}
	maxRisk := 20 * n
	q := make([][]Coord, 0)
	for range maxRisk {
		q = append(q, make([]Coord, 0))
	}
	q[0] = append(q[0], start)
	curRisk := 0
	curMin := maxRisk

	for totalRisk[end.X][end.Y] == 0 {
		if curRisk >= min(curMin, maxRisk) {
			return curMin
		}
		for _, c := range q[curRisk] {
			curWalls := currentWalls(walls, curRisk)
			if p1 > 0 {
				curWalls = currentWalls(walls, p1)
			}
			if curRisk > totalRisk[c.X][c.Y] {
				continue
			}
			for _, elem := range m.Neighbours(c.X, c.Y) {
				nb := Coord{X: elem.X, Y: elem.Y}
				if curWalls.Contains(nb) {
					q[maxRisk-1] = append(q[maxRisk-1], nb)
					continue
				}
				deltaRisk := 1
				if totalRisk[nb.X][nb.Y] == 0 {
					totalRisk[nb.X][nb.Y] = curRisk + deltaRisk
					q[curRisk+deltaRisk] = append(q[curRisk+deltaRisk], Coord{X: nb.X, Y: nb.Y})
				}
			}
		}
		curRisk += 1
	}

	return totalRisk[end.X][end.Y]
}

func pathBlocked(walls []Coord, step, size int) bool {
	sWalls := currentWalls(walls, step)
	visited := Set[Coord]{}
	for _, w := range sWalls.ToSlice() {
		if visited.Contains(w) {
			continue
		}
		visited.Add(w)
		line := Set[Coord]{}
		line.Add(w)
		north, east, south, west := Set[Coord]{}, Set[Coord]{}, Set[Coord]{}, Set[Coord]{}
		q := Queue[Coord]{w}
		for !q.IsEmpty() {
			other := q.Pop()
			for _, nb := range Neighbours(other) {
				if !sWalls.Contains(nb) || line.Contains(nb) {
					continue
				}
				if nb.X == 0 {
					west.Add(other)
				} else if nb.X == size-1 {
					east.Add(other)
				}
				if nb.Y == 0 {
					north.Add(other)
				} else if nb.Y == size-1 {
					south.Add(other)
				}
				visited.Add(nb)
				line.Add(nb)
				q.Push(nb)
			}
		}
		if (len(north) > 0 && len(south) > 0) || (len(west) > 0 && len(east) > 0) {
			return true
		}
	}
	return false
}

func Solve(walls []Coord, size int) (p1 int, p2 string) {
	mat := initMatrix(size)
	nb := 1024
	if size == 7 {
		nb = 12
	}
	p1 = aStar(mat, walls, nb)
	for i := nb + 1; i < 10_000; i++ {
		if pathBlocked(walls, i, size) {
			p2 = fmt.Sprintf("%d,%d", walls[i-1].X, walls[i-1].Y)
			break
		}
	}
	return
}

func TestDay18(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example), 7)
	r.Equal(22, p1Ex, "example p1")
	r.Equal("6,1", p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input), 71)
	r.Equal(372, p1, "input p1")
	r.Equal("25,6", p2, "input p2")
}

func BenchmarkDay18(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input), 71)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
