package day12

import (
	"bufio"
	"fmt"
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

var (
	cache = make(map[string]int)
)

func cachedRecursion(s string, counts []int) int {
	cacheKey := s
	for _, count := range counts { // build cache key
		cacheKey += "." + strconv.Itoa(count)
	}
	if v, ok := cache[cacheKey]; ok { // cache hit
		return v
	}
	if len(s) == 0 {
		if len(counts) == 0 {
			return 1
		}
		return 0
	}
	head, tail := s[0], s[1:]
	switch head {
	case '?': // recurse over the two possibilities
		return cachedRecursion("."+tail, counts) + cachedRecursion("#"+tail, counts)
	case '.': // no spring: recurse on the tail
		res := cachedRecursion(tail, counts)
		cache[cacheKey] = res
		return res
	case '#':
		if len(counts) == 0 { // spring group found but none expected
			cache[cacheKey] = 0
			return 0
		}
		if len(s) < counts[0] { // spring group expected but impossible to reach with the remaining characters
			cache[cacheKey] = 0
			return 0
		}
		if strings.Contains(s[0:counts[0]], ".") { // spring group expected but the n next character do not match
			cache[cacheKey] = 0
			return 0
		}
		if len(counts) > 1 { // more groups remain
			if len(s) < counts[0]+1 || s[counts[0]] == '#' { // impossible to have one more group, or current group is too long
				cache[cacheKey] = 0
				return 0
			}
			cache[cacheKey] = cachedRecursion(s[counts[0]+1:], counts[1:])
			return cache[cacheKey]
		} else { // it was the last group
			cache[cacheKey] = cachedRecursion(s[counts[0]:], counts[1:])
			return cache[cacheKey]
		}
	}
	return 0
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []string) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, sc.Text())
	}
	return
}

func Solve(input []string) (p1 int, p2 int) {
	for _, line := range input {
		tmp := strings.Split(line, " ")
		counts := []int{}
		for _, rawGrp := range strings.Split(tmp[1], ",") {
			grp, _ := strconv.Atoi(rawGrp)
			counts = append(counts, grp)
		}
		p1 += cachedRecursion(tmp[0], counts)
		s, countsP2 := tmp[0], counts
		for i := 0; i < 4; i++ {
			s += "?" + tmp[0]
			counts = append(countsP2, counts...)
		}
		p2 += cachedRecursion(s, counts)
	}
	return
}

func TestDay12(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(21, p1Ex, "example p1")
	r.Equal(525152, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(7236, p1, "input p1")
	r.Equal(11607695322318, p2, "input p2")
}

func BenchmarkDay12(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		cache = map[string]int{}
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
