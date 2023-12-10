package day10

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input    = "./input.txt"
	example  = "./example.txt"
	example2 = "./example2.txt"
	example3 = "./example3.txt"
	example4 = "./example4.txt"
	example5 = "./example5.txt"
)

var (
	connectPoints = map[rune][]bool{
		'-': {false, true, false, true},
		'|': {true, false, true, false},
		'F': {false, true, true, false},
		'J': {true, false, false, true},
		'L': {true, true, false, false},
		'7': {false, false, true, true},
		'.': {false, false, false, false},
		'S': {true, true, true, true},
	}

	directions = [][]int{
		{-1, 0}, // 0 = North
		{0, 1},  // 1 = East
		{1, 0},  // 2 = South
		{0, -1}, // 3 = West
	}
)

func getChar(dir1, dir2 int) rune {
	for char, dirs := range connectPoints {
		if char == 'S' {
			continue
		}
		if dirs[dir1] && dirs[dir2] {
			return char
		}
	}
	return 'S'
}

func connects(self, other rune, direction int) bool {
	return connectPoints[self][direction] && connectPoints[other][(direction+2)%4]
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) ([]rune, int, int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	res := []string{}
	for sc.Scan() {
		res = append(res, "."+sc.Text()+".")
	}
	padding := strings.Repeat(".", len(res[0]))
	res = append([]string{padding}, append(res, padding)...)
	return []rune(strings.Join(res, "")), len(res), len(res[0])
}

func floodFill(input []rune, idx, cols int, loopIdxs map[int]bool) []rune {
	if _, inLoop := loopIdxs[idx]; inLoop || input[idx] == '■' {
		return input
	}
	seen := make([]bool, len(input))
	q := []int{idx}
	res := make([]rune, 0)
	res = append(res, input...)

	for len(q) > 0 {
		idx := q[0]
		q = q[1:]
		if seen[idx] {
			continue
		}
		i, j := idx/cols, idx%cols

		seen[idx] = true
		res[idx] = '■'

		for _, offset := range directions {
			x, y := i+offset[0], j+offset[1]
			newIdx := x*cols + y
			_, inLoop := loopIdxs[newIdx]
			if 0 <= newIdx && newIdx < len(input) && !inLoop {
				q = append(q, newIdx)
			}
		}
	}
	return res
}

func isEdge(input []rune, i, j, cols int) int {
	for dir, offset := range directions {
		x, y := i+offset[0], j+offset[1]
		if input[x*cols+y] == '■' {
			return dir
		}
	}
	return -1
}

func Solve(input []rune, lines, cols int) (int, int) {
	toIdx := func(i, j int) int {
		return i*cols + j
	}
	toCoords := func(idx int) (int, int) {
		return idx / cols, idx % cols
	}
	loopIdxs := make(map[int]bool)
	startNeighbour := -1
	comesFrom := -1
	for idx, self := range input {
		i, j := idx/cols, idx%cols
		if i == 0 || i == lines-1 || j == 0 || j == cols-1 {
			continue
		}
		for d, offset := range directions {
			otherIdx := toIdx(i+offset[0], j+offset[1])
			other := input[otherIdx]
			if other != 'S' {
				continue
			}
			if connects(self, other, d) {
				loopIdxs[idx] = true
				if other == 'S' && startNeighbour < 0 {
					startNeighbour = idx
					comesFrom = d
				}
				break
			}
		}
		if startNeighbour >= 0 {
			break
		}
	}
	sdir1 := (comesFrom + 2) % 4
	next := '.'
	idx := startNeighbour
	prevDirection := comesFrom
	for next != 'S' {
		char := input[idx]
		i, j := toCoords(idx)
		for d, ok := range connectPoints[char] {
			if !ok || d == prevDirection {
				continue
			}
			offset := directions[d]
			nextIdx := toIdx(i+offset[0], j+offset[1])
			next = input[nextIdx]
			prevDirection = (d + 2) % 4
			idx = nextIdx
			loopIdxs[idx] = true
			break
		}
		if input[idx] == 'S' {
			input[idx] = getChar(sdir1, prevDirection)
		}
	}
	s := floodFill(input, 0, cols, loopIdxs)
	next = '.'
	idx = startNeighbour
	prevDirection = comesFrom
	edge := -1
	remaining := len(loopIdxs)
	for remaining > 0 {
		char := s[idx]
		i, j := toCoords(idx)
		nextDir := -1
		for d, ok := range connectPoints[char] {
			if !ok || d == prevDirection {
				continue
			}
			nextDir = d
			break
		}
		offset := directions[nextDir]
		nextIdx := toIdx(i+offset[0], j+offset[1])
		newDirection := (nextDir + 2) % 4
		rotation := (newDirection - prevDirection + 4) % 4
		prevDirection = newDirection
		idx = nextIdx
		if edge >= 0 {
			edgeDirs := []int{}
			switch char {
			case '7', 'F', 'L', 'J':
				if !connectPoints[char][edge] {
					for dir, ok := range connectPoints[char] {
						if !ok {
							edgeDirs = append(edgeDirs, dir)
						}
					}
				}
			default:
				edgeDirs = []int{edge}
			}
			for _, e := range edgeDirs {
				offset = directions[e]
				outIdx := toIdx(i+offset[0], j+offset[1])
				s = floodFill(s, outIdx, cols, loopIdxs)
			}
			edge = (edge + rotation + 4) % 4
		} else {
			remaining += 1
		}
		if e := isEdge(s, i, j, cols); edge < 0 && e >= 0 {
			edge = e
		}
		remaining -= 1
	}

	res := 0
	for idx, char := range s {
		_, inLoop := loopIdxs[idx]
		if !inLoop && char != '■' {
			s[idx] = 'I'
			res += 1
		}
	}
	return len(loopIdxs) / 2, res
}

func TestDay10(t *testing.T) {
	r := R.New(t)
	p1, p2 := Solve(ReadInput(example))
	r.Equal(8, p1, "example p1")
	r.Equal(1, p2, "example p1")

	_, p2 = Solve(ReadInput(example2))
	r.Equal(4, p2, "example2 p2")

	_, p2 = Solve(ReadInput(example3))
	r.Equal(4, p2, "example3 p2")

	_, p2 = Solve(ReadInput(example4))
	r.Equal(8, p2, "example4 p2")

	_, p2 = Solve(ReadInput(example5))
	r.Equal(10, p2, "example5 p2")

	p1, p2 = Solve(ReadInput(input))
	r.Equal(6690, p1, "input p1")
	r.Equal(525, p2, "input p2")
}

func BenchmarkDay10(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		input, lines, cols := ReadInput(input)
		Solve(input, lines, cols)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
