package day17

import (
	"bufio"
	"container/heap"
	"fmt"
	"os"
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

var (
	offset = []int{
		-1, 0,
		0, 1,
		1, 0,
		0, -1,
	}
)

type item struct {
	heat, x, y, dir, count, index int
}

type PriorityQueue []*item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].heat < pq[j].heat
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x any) {
	n := len(*pq)
	it := x.(*item)
	it.index = n
	*pq = append(*pq, it)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	it := old[n-1]
	old[n-1] = nil
	it.index = -1
	*pq = old[0 : n-1]
	return it
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		// parsing here...
		row := []int{99999}
		for _, c := range sc.Text() {
			row = append(row, int(c)-48)
		}
		row = append(row, 99999)
		res = append(res, row)
	}
	padding := []int{}
	for range res[0] {
		padding = append(padding, 99999)
	}
	res = append(res, padding)
	return append([][]int{padding}, res...)
}

func inBounds(x, y, lines, cols int) bool {
	return 0 <= x && x < lines && 0 <= y && y < cols
}

func getNeighbours(it item, lines, cols int) (res []int) {
	turnRight := (it.dir + 1) % 4
	nx, ny := it.x+offset[2*turnRight], it.y+offset[2*turnRight+1]
	if inBounds(nx, ny, lines, cols) {
		res = append(res, nx, ny, turnRight, 1)
	}
	nx, ny = it.x+offset[2*it.dir], it.y+offset[2*it.dir+1]
	if it.count < 3 && inBounds(nx, ny, lines, cols) {
		res = append(res, nx, ny, it.dir, it.count+1)
	}
	turnLeft := (it.dir + 3) % 4
	nx, ny = it.x+offset[2*turnLeft], it.y+offset[2*turnLeft+1]
	if inBounds(nx, ny, lines, cols) {
		res = append(res, nx, ny, turnLeft, 1)
	}
	return
}

func getNeighboursP2(it item, lines, cols int) (res []int) {
	turnRight := (it.dir + 1) % 4
	nx, ny := it.x+offset[2*turnRight], it.y+offset[2*turnRight+1]
	if it.count >= 4 && inBounds(nx, ny, lines, cols) {
		res = append(res, nx, ny, turnRight, 1)
	}
	nx, ny = it.x+offset[2*it.dir], it.y+offset[2*it.dir+1]
	if it.count < 10 && inBounds(nx, ny, lines, cols) {
		res = append(res, nx, ny, it.dir, it.count+1)
	}
	turnLeft := (it.dir + 3) % 4
	nx, ny = it.x+offset[2*turnLeft], it.y+offset[2*turnLeft+1]
	if it.count >= 4 && inBounds(nx, ny, lines, cols) {
		res = append(res, nx, ny, turnLeft, 1)
	}
	return
}

func (it item) key() string {
	return strconv.Itoa(it.x) + "." + strconv.Itoa(it.y) + "." + strconv.Itoa(it.dir) + "." + strconv.Itoa(it.count)
}

func find(arr [][]int, p2 bool) int {
	getNb := getNeighbours
	if p2 {
		getNb = getNeighboursP2
	}
	lines, cols := len(arr), len(arr[0])
	startX, startY, endX, endY := 1, 1, lines-2, cols-2
	q := PriorityQueue{{0, startX, startY, 1, 1, 0}, {0, startX, startY, 2, 1, 0}}
	heap.Init(&q)
	visited := make(map[string]bool)
	for q.Len() > 0 {
		it := heap.Pop(&q).(*item)
		if it.x == 0 || it.y == 0 || it.x == lines-1 || it.y == cols-1 {
			continue
		}
		if it.x == endX && it.y == endY {
			if p2 && it.count < 4 {
				continue
			}
			return it.heat
		}
		seen := false
		for c := 0; c < it.count+1; c++ {
			if _, ok := visited[it.key()]; ok {
				seen = true
				break
			}
		}
		if seen {
			continue
		}
		visited[it.key()] = true
		nbs := getNb(*it, lines, cols)
		for i := 0; i < len(nbs); i += 4 {
			nx, ny, dir, count := nbs[i], nbs[i+1], nbs[i+2], nbs[i+3]
			heap.Push(&q, &item{it.heat + arr[nx][ny], nx, ny, dir, count, 0})
		}
	}
	return -1
}

func Solve(input [][]int) (int, int) {
	return find(input, false), find(input, true)
}

func TestDay17(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(102, p1Ex, "example p1")
	r.Equal(94, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(635, p1, "input p1")
	r.Equal(734, p2, "input p2")
}

func BenchmarkDay17(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
