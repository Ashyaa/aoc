package day23

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

var (
	offset = [][]int{
		{-1, 0},
		{0, 1},
		{1, 0},
		{0, -1},
	}
	slope = []rune{
		'^',
		'>',
		'v',
		'<',
	}
)

func inBounds(x, y, lines, cols int) bool {
	return 0 <= x && x < lines && 0 <= y && y < cols
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

func isIntersection(arr [][]rune, i, j, lines, cols int) bool {
	count := 0
	for _, o := range offset {
		x, y := i+o[0], j+o[1]
		if !inBounds(x, y, lines, cols) {
			continue
		}
		if arr[x][y] != '#' {
			count++
		}
	}
	return count != 2
}

func neighbours(arr [][]rune, i, j, lines, cols int) (res [][]int) {
	for dir, o := range offset {
		x, y := i+o[0], j+o[1]
		if !inBounds(x, y, lines, cols) {
			continue
		}
		if arr[x][y] == '.' || arr[x][y] == slope[dir] {
			res = append(res, []int{x, y})
		}
	}
	return
}

func getEdges(idxToEdge map[int]int, x, y, lines, cols int, chars [][]rune) map[int]int {
	res := make(map[int]int)
	for _, n := range neighbours(chars, x, y, lines, cols) {
		prevX, prevY := x, y
		nx, ny := n[0], n[1]
		distance := 1
		deadEnd := false
		for !deadEnd {
			deadEnd = true
			for _, nn := range neighbours(chars, nx, ny, lines, cols) {
				nnx, nny := nn[0], nn[1]
				if nnx == prevX && nny == prevY {
					continue
				}
				prevX, prevY = nx, ny
				nx, ny = nnx, nny
				deadEnd = false
				break
			}
			distance += 1
			other := nx*cols + ny
			if e, ok := idxToEdge[other]; ok {
				res[e] = distance
				break
			}
		}
	}
	return res
}

func graph(chars [][]rune) []map[int]int {
	lines, cols := len(chars), len(chars[0])
	getIdx := func(a, b int) int {
		return a*cols + b
	}
	edges := []map[int]int{}
	vertices := [][]int{}
	isEdge := map[int]int{}
	for i, l := range chars {
		for j, c := range l {
			if c == '#' {
				continue
			}
			if isIntersection(chars, i, j, lines, cols) {
				isEdge[getIdx(i, j)] = len(edges)
				edges = append(edges, make(map[int]int))
				vertices = append(vertices, []int{i, j})
			}
		}
	}
	for e, v := range vertices {
		edges[e] = getEdges(isEdge, v[0], v[1], lines, cols, chars)
	}
	return edges
}

func dijkstra(graph []map[int]int, idx, dist int, seen []bool) int {
	if idx == len(seen)-1 {
		return dist
	}
	res := -1
	newSeen := slices.Clone(seen)
	newSeen[idx] = true
	for other, d := range graph[idx] {
		if !seen[other] {
			res = max(res, dijkstra(graph, other, dist+d, newSeen))
		}
	}
	return res
}

func Solve(chars [][]rune) (p1 int, p2 int) {
	g := graph(chars)
	p1 = dijkstra(g, 0, 0, make([]bool, len(g)))
	for self := range g {
		for other := self + 1; other < len(g); other++ {
			if v, ok := g[self][other]; ok {
				g[other][self] = v
			}
			if v, ok := g[other][self]; ok {
				g[self][other] = v
			}
		}
	}
	p2 = dijkstra(g, 0, 0, make([]bool, len(g)))
	return
}

func TestDay23(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(exampleFile))
	r.Equal(94, p1Ex, "example p1")
	r.Equal(154, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(inputFile))
	r.Equal(2362, p1, "input p1")
	r.Equal(6538, p2, "input p2")
}

func BenchmarkDay23(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(inputFile))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
