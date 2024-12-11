package day11

import (
	U "aoc/utils"
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
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
func ReadInput(filepath string) (res []int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = U.Map(strings.Split(sc.Text(), " "), U.ToInt)
	}
	return
}

func magnitude(n int) int {
	f := math.Log10(float64(n))
	return 1 + int(math.Floor(f))
}

func split(n int) (int, int) {
	s := strconv.Itoa(n)
	half := len(s) / 2
	return U.ToInt(s[:half]), U.ToInt(s[half:])
}

func rec(c U.Coord, cache map[U.Coord]int) int {
	if r, ok := cache[c]; ok {
		return r
	}
	if c.Y == 0 {
		return 1
	}
	var res int
	if c.X == 0 {
		res = rec(U.Coord{X: 1, Y: c.Y - 1}, cache)
	} else if magnitude(c.X)%2 == 0 {
		s1, s2 := split(c.X)
		res = rec(U.Coord{X: s1, Y: c.Y - 1}, cache) + rec(U.Coord{X: s2, Y: c.Y - 1}, cache)
	} else {
		res = rec(U.Coord{X: c.X * 2024, Y: c.Y - 1}, cache)
	}
	cache[c] = res
	return res
}

func Solve(input []int) (p1 int, p2 int) {
	cache := map[U.Coord]int{}
	for _, n := range input {
		p2 += rec(U.Coord{X: n, Y: 75}, cache)
		p1 += rec(U.Coord{X: n, Y: 25}, cache)
	}
	return
}

func TestDay11(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(55312, p1Ex, "example p1")
	r.Equal(65601038650482, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(231278, p1, "input p1")
	r.Equal(274229228071551, p2, "input p2")
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
