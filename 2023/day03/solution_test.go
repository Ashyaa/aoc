package dayXX

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
	"time"
	"unicode"

	R "github.com/stretchr/testify/require"
)

const (
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]rune) {
	data, _ := os.ReadFile(filepath)
	lines := strings.Split(string(data), "\n")
	nbChars := len(strings.TrimSpace(lines[0]))
	for i := range lines {
		lines[i] = "." + strings.TrimSpace(lines[i]) + "."
	}
	padding := strings.Repeat(".", nbChars+2)
	lines = append([]string{padding}, append(lines, padding)...)
	for _, l := range lines {
		res = append(res, []rune(l))
	}
	return res
}

var shifts = []int{-1, 0, 1}

func addNeighbours(i, j, lineLength int, neighbours map[int]bool) {
	for _, di := range shifts {
		ni := i + di
		for _, dj := range shifts {
			nj := j + dj
			idx := ni*lineLength + nj
			if di == 0 && dj == 0 {
				neighbours[idx] = false
				continue
			}
			r, ok := neighbours[idx]
			if di == 0 && dj == -1 && ok && !r {
				continue
			}
			neighbours[idx] = true
		}
	}
}

func checkNeighbours(input [][]rune, lineLength int, neighbours map[int]bool) (p1 bool, p2 int) {
	for idx, ok := range neighbours {
		if !ok {
			continue
		}
		i, j := idx/lineLength, idx%lineLength
		if input[i][j] != '.' {
			p1 = true
		}
		if input[i][j] == '*' {
			p2 = idx
		}
		if p1 && p2 > 0 {
			return
		}
	}
	return
}

func Solve(input [][]rune) (p1, p2 int) {
	nbLines := len(input)
	lineLength := len(input[0])
	foundGear := map[int]int{}
	for i, line := range input {
		if i == 0 || i == nbLines-1 {
			continue
		}
		neighbours := map[int]bool{}
		buffer := []rune{}
		for j, r := range line {
			if r == '.' && len(buffer) == 0 {
				continue
			}
			if unicode.IsDigit(r) {
				buffer = append(buffer, r)
				addNeighbours(i, j, lineLength, neighbours)
				continue
			}
			isPiece, idx := checkNeighbours(input, lineLength, neighbours)
			if isPiece {
				nb, _ := strconv.Atoi(string(buffer))
				p1 += nb
			}
			if idx > 0 {
				nb, _ := strconv.Atoi(string(buffer))
				nb1, ok := foundGear[idx]
				if ok {
					p2 += nb * nb1
				} else {
					foundGear[idx] = nb
				}
			}
			neighbours = map[int]bool{}
			buffer = []rune{}
		}
	}
	return
}

func TestDay03(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	input := ReadInput(inputFile)
	p1, p2 := Solve(example)
	r.Equal(4361, p1)
	r.Equal(467835, p2)
	p1, p2 = Solve(input)
	r.Equal(556057, p1)
	r.Equal(82824352, p2)
}

func BenchmarkDay03(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		input := ReadInput(inputFile)
		n, _ = Solve(input)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
