package day16

import (
	. "aoc/utils"
	"bufio"
	"fmt"
	"os"
	"slices"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input    = "./input.txt"
	example  = "./example.txt"
	example2 = "./example2.txt"
	maxInt   = 1 << 32
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res Matrix[rune], start, end Coord) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	buf := make([][]rune, 0)
	x := 0
	for sc.Scan() {
		line := []rune(sc.Text())
		if y := slices.Index(line, 'S'); y >= 0 {
			start.X = x
			start.Y = y
		} else if y := slices.Index(line, 'E'); y >= 0 {
			end.X = x
			end.Y = y
		}
		buf = append(buf, line)
		x++
	}
	res = NewMatrix(buf)
	return
}

type item struct {
	Coord
	score int
	path  Set[Coord]
}

func canVisit(it item, visited map[Coord]int) bool {
	prev, ok := visited[it.Coord]
	if ok && prev < it.score {
		return false
	}
	visited[it.Coord] = it.score
	return true
}

func heapedDijkstra(input Matrix[rune], start, end Coord) (int, int) {
	q := NewPriorityQueue(item{start, 0, NewSet(start)})
	visited := map[Coord]int{}
	lowestScore := -1
	positions := NewSet[Coord]()

	for q.Len() > 0 {
		it := q.Pop()
		if lowestScore >= 0 && lowestScore < it.score {
			break
		}

		if it.X == end.X && it.Y == end.Y {
			lowestScore = it.score
			positions = positions.Union(it.path)
			continue
		}

		if !canVisit(it, visited) {
			continue
		}

		offset := Directions[it.Z]
		next := item{Coord{X: it.X + offset.X, Y: it.Y + offset.Y, Z: it.Z}, it.score + 1, it.path.Copy()}
		next.path.Add(Coord{X: next.X, Y: next.Y})
		if input.At(next.X, next.Y) != '#' && canVisit(next, visited) {
			q.Push(next, it.score+1)
		}
		left := item{Coord{X: it.X, Y: it.Y, Z: (it.Z + 3) % 4}, it.score + 1000, it.path.Copy()}
		if canVisit(left, visited) {
			q.Push(left, it.score+1000)
		}

		right := item{Coord{X: it.X, Y: it.Y, Z: (it.Z + 1) % 4}, it.score + 1000, it.path.Copy()}
		if canVisit(right, visited) {
			q.Push(right, it.score+1000)
		}
	}

	return lowestScore, len(positions)
}

func Solve(input Matrix[rune], start, end Coord) (p1 int, p2 int) {
	start.Z = 1
	p1, p2 = heapedDijkstra(input, start, end)
	return
}

func TestDay16(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(7036, p1Ex, "example p1")
	r.Equal(45, p2Ex, "example p2")
	p1Ex2, p2Ex2 := Solve(ReadInput(example2))
	r.Equal(11048, p1Ex2, "example 2 p1")
	r.Equal(64, p2Ex2, "example 2 p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(72400, p1, "input p1")
	r.Equal(435, p2, "input p2")
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
