package day11

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]rune) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, []rune(sc.Text()))
	}
	return
}

func expand(input [][]rune) ([]int, []int, []int) {
	emptyLines := []int{}
	emptyCols := []int{}
	galaxies := []int{}
	for j := 0; j < len(input[0]); j++ {
		empty := true
		for i := 0; i < len(input); i++ {
			if input[i][j] == '#' {
				empty = false
				break
			}
		}
		if empty {
			emptyCols = append(emptyCols, j)
		}
	}
	for i := 0; i < len(input); i++ {
		if !strings.Contains(string(input[i]), "#") {
			emptyLines = append(emptyLines, i)
		}
		for j := 0; j < len(input[0]); j++ {
			if input[i][j] == '#' {
				galaxies = append(galaxies, i, j)
			}
		}
	}
	return emptyLines, emptyCols, galaxies
}

func intAbs(n int) int {
	return int(math.Abs(float64(n)))
}

func manhattan(x1, y1, x2, y2 int) int {
	return intAbs(x1-x2) + intAbs(y1-y2)
}

func Solve(input [][]rune) (res, fill int) {
	emptyLines, emptyCols, galaxies := expand(input)
	for idx := 0; idx < len(galaxies); idx += 2 {
		x1, y1 := galaxies[idx], galaxies[idx+1]
		for jdx := idx + 2; jdx < len(galaxies); jdx += 2 {
			x2, y2 := galaxies[jdx], galaxies[jdx+1]
			dist := manhattan(x1, y1, x2, y2)
			for _, i := range emptyLines {
				if (x1 < i && i < x2) || (x2 < i && i < x1) {
					fill += 1
				}
			}
			for _, j := range emptyCols {
				if (y1 < j && j < y2) || (y2 < j && j < y1) {
					fill += 1
				}
			}
			res += dist
		}
	}
	return
}

func TestDay11(t *testing.T) {
	r := R.New(t)
	exRes, exFill := Solve(ReadInput(example))
	r.Equal(374, exRes+exFill, "example p1")
	r.Equal(1030, exRes+exFill*9, "example p2.1")
	r.Equal(8410, exRes+exFill*99, "example p2.2")
	res, fill := Solve(ReadInput(input))
	r.Equal(9769724, res+fill, "input p1")
	r.Equal(603020563700, res+fill*(1000000-1), "input p2")
}

func BenchmarkDay11(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
