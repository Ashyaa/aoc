package day14

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
	input   = "./input.txt"
	example = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][]rune) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		// parsing here...
		res = append(res, []rune(sc.Text()))
	}
	return
}

func tiltV(input [][]rune, up bool) (res [][]rune) {
	res = make([][]rune, len(input))
	for i := range res {
		res[i] = make([]rune, len(input[0]))
	}
	for y := 0; y < len(input[0]); y++ {
		col := []rune{}
		for x := range input {
			col = append(col, input[x][y])
		}
		strs := []string{}
		for _, fragment := range strings.Split(string(col), "#") {
			if len(fragment) == 0 {
				strs = append(strs, fragment)
				continue
			}
			nbRocks := strings.Count(fragment, "O")
			if up {
				strs = append(strs, strings.Repeat("O", nbRocks)+strings.Repeat(".", len(fragment)-nbRocks))
			} else {
				strs = append(strs, strings.Repeat(".", len(fragment)-nbRocks)+strings.Repeat("O", nbRocks))
			}
		}
		for x, c := range strings.Join(strs, "#") {
			res[x][y] = c
		}
	}
	return
}

func tiltH(input [][]rune, right bool) (res [][]rune) {
	res = make([][]rune, len(input))
	for i := range res {
		res[i] = make([]rune, len(input[0]))
	}
	for x, line := range input {
		strs := []string{}
		for _, fragment := range strings.Split(string(line), "#") {
			if len(fragment) == 0 {
				strs = append(strs, fragment)
				continue
			}
			nbRocks := strings.Count(fragment, "O")
			if right {
				strs = append(strs, strings.Repeat(".", len(fragment)-nbRocks)+strings.Repeat("O", nbRocks))
			} else {
				strs = append(strs, strings.Repeat("O", nbRocks)+strings.Repeat(".", len(fragment)-nbRocks))
			}
		}
		for y, c := range strings.Join(strs, "#") {
			res[x][y] = c
		}
	}
	return
}

func weight(input [][]rune) (res int) {
	nbLines := len(input)
	for i, line := range input {
		res += strings.Count(string(line), "O") * (nbLines - i)
	}
	return res
}

func Solve(input [][]rune) (p1 int, p2 int) {
	buffer := []int{}
	newState := input
	for i := 0; i < 200; i++ {
		newState = tiltV(newState, true)
		if i == 0 {
			p1 = weight(newState)
		}
		newState = tiltH(newState, false)
		newState = tiltV(newState, false)
		newState = tiltH(newState, true)
		buffer = append(buffer, weight(newState))
	}
	period := -1
	offset := 0
	for {
		n := buffer[offset]
		for i := 1; i < 20; i++ {
			if buffer[offset+i] == n && buffer[offset+5*i] == n {
				period = i
				break
			}
		}
		if period > 0 {
			break
		}
		offset++
	}
	p2 = buffer[offset-1+((1000000000-offset)%period)]
	return
}

func TestDay14(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(136, p1Ex, "example p1")
	r.Equal(64, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(110407, p1, "input p1")
	r.Equal(87273, p2, "input p2")
}

func BenchmarkDay14(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
