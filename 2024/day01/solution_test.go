package day01

import (
	"aoc/utils"
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
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
func ReadInput(filepath string) (l1, l2 []int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		// parsing here...
		raws := strings.Split(sc.Text(), "   ")
		n1, _ := strconv.Atoi(raws[0])
		n2, _ := strconv.Atoi(raws[1])
		l1 = append(l1, n1)
		l2 = append(l2, n2)
	}
	return
}

func Solve(l1, l2 []int) (p1 int, p2 int) {
	sort.Ints(l1)
	sort.Ints(l2)
	counter := utils.NewCounter[int]()
	counter.Add(l2...)
	for i, n1 := range l1 {
		n2 := l2[i]
		p1 += int(math.Abs(float64(n2 - n1)))
		p2 += n1 * counter.Count(n1)
	}
	return
}

func TestDay01(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(11, p1Ex, "example p1")
	r.Equal(31, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(2066446, p1, "input p1")
	r.Equal(24931009, p2, "input p2")
}

func BenchmarkDay01(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
