package day05

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

type conv struct {
	dstBegin, srcBegin, srcEnd int
}

func (c conv) InRange(n int) bool {
	return n >= c.srcBegin && n <= c.srcEnd
}

func (c conv) Call(n int) int {
	return c.dstBegin + n - c.srcBegin
}

func (c conv) intersects(otherBegin, otherEnd int) bool {
	return c.srcBegin < otherEnd && otherBegin < c.srcEnd
}

func (c conv) intersection(otherBegin, otherEnd int) (interStart, interEnd int, ok bool) {
	if !c.intersects(otherBegin, otherEnd) {
		return
	}
	return max(c.srcBegin, otherBegin), min(c.srcEnd, otherEnd), true
}

func (c conv) outOfIntersection(otherBegin, otherEnd int) (res []int) {
	interBegin, interEnd, ok := c.intersection(otherBegin, otherEnd)
	if !ok {
		return
	}
	if otherBegin < interBegin {
		res = append(res, otherBegin, interBegin)
	}
	if interEnd < otherEnd {
		res = append(res, interEnd, otherEnd)
	}
	return
}

type convs []conv

func (cs convs) Call(n int) int {
	for _, conv := range cs {
		if conv.InRange(n) {
			return conv.Call(n)
		}
	}
	return n
}

func convFromSlice(s []int) conv {
	return conv{s[0], s[1], s[1] + s[2]}
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (seeds []int, maps []convs) {
	firstLine := true
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	maps = make([]convs, 7)
	mapIdx := -1
	for sc.Scan() {
		line := sc.Text()
		if len(line) == 0 {
			continue
		}
		if firstLine {
			words := strings.Split(line[7:], " ")
			for _, word := range words {
				seed, _ := strconv.Atoi(word)
				seeds = append(seeds, seed)
			}
			firstLine = false
			continue
		}
		if strings.HasSuffix(line, "map:") {
			mapIdx += 1
			continue
		}
		words := strings.Split(line, " ")
		numbers := []int{}
		for _, word := range words {
			n, _ := strconv.Atoi(word)
			numbers = append(numbers, n)
		}
		maps[mapIdx] = append(maps[mapIdx], convFromSlice(numbers))
	}
	return
}

func First(seeds []int, maps []convs) int {
	locations := []int{}
	for _, seed := range seeds {
		src := seed
		for _, convs := range maps {
			src = convs.Call(src)
		}
		locations = append(locations, src)
	}
	return slices.Min(locations)
}

func Second(seeds []int, maps []convs) int {
	source_ranges := []int{}
	for idx := range seeds {
		if idx%2 != 0 {
			continue
		}
		source_ranges = append(source_ranges, seeds[idx], seeds[idx]+seeds[idx+1])
	}
	for _, convs := range maps {
		idx := 0
		for {
			if idx >= len(source_ranges) {
				break
			}
			srcBegin, srcEnd := source_ranges[idx], source_ranges[idx+1]
			for _, conv := range convs {
				interBegin, interEnd, ok := conv.intersection(srcBegin, srcEnd)
				if ok {
					source_ranges[idx] = conv.Call(interBegin)
					source_ranges[idx+1] = conv.Call(interEnd)
					source_ranges = append(source_ranges, conv.outOfIntersection(srcBegin, srcEnd)...)
					break
				}
			}
			idx += 2
		}
	}
	return slices.Min(source_ranges)
}

func TestDay05(t *testing.T) {
	r := R.New(t)
	exSeeds, exMaps := ReadInput(exampleFile)
	seeds, maps := ReadInput(inputFile)
	r.Equal(35, First(exSeeds, exMaps), "example p1")
	r.Equal(177942185, First(seeds, maps), "input p1")
	r.Equal(46, Second(exSeeds, exMaps), "example p2")
	r.Equal(69841803, Second(seeds, maps), "input p2")
}

func BenchmarkDay05(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		a, b := ReadInput(inputFile)
		First(a, b)
		Second(a, b)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
