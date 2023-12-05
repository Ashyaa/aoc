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
	dstMin, dstMax, srcMin, srcMax int
}

func (c conv) InRange(n int, reverse bool) bool {
	if reverse {
		return n >= c.dstMin && n <= c.dstMax
	}
	return n >= c.srcMin && n <= c.srcMax
}

func (c conv) Call(n int, reverse bool) int {
	if reverse {
		return c.srcMin + n - c.dstMin
	}
	return c.dstMin + n - c.srcMin
}

type convs []conv

func (cs convs) Call(n int, reverse bool) int {
	for _, conv := range cs {
		if conv.InRange(n, reverse) {
			return conv.Call(n, reverse)
		}
	}
	return n
}

func (cs convs) Min() int {
	var res int
	min := 1 << 32
	for _, conv := range cs {
		if conv.dstMin < min {
			min = conv.dstMin
			res = conv.srcMin
		}
	}
	return res
}

func intersects(a, b, c, d int) bool {
	return a < d && c < b
}

func intersection(a, b, c, d int) (start, end int, ok bool) {
	if !intersects(a, b, c, d) {
		return start, end, false
	}
	return max(a, c), min(b, b), ok
}

func outOfIntersection(a, b, c, d int) (res []int) {
	interMin, interMax, ok := intersection(a, b, c, d)
	if !ok {
		return
	}
	if a < interMin {
		res = append(res, a, interMin)
	}
	if interMax < b {
		res = append(res, interMax, b)
	}
	return
}

func convFromSlice(s []int) conv {
	return conv{s[0], s[0] + s[2], s[1], s[1] + s[2]}
}

func SplitLines(s string) []string {
	var lines []string
	sc := bufio.NewScanner(strings.NewReader(s))
	for sc.Scan() {
		lines = append(lines, sc.Text())
	}
	return lines
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (seeds []int, maps []convs) {
	data, _ := os.ReadFile(filepath)
	maps = make([]convs, 7)
	mapIdx := -1
	for idx, line := range SplitLines(string(data)) {
		if idx == 0 {
			words := strings.Split(line[7:], " ")
			for _, word := range words {
				seed, _ := strconv.Atoi(word)
				seeds = append(seeds, seed)
			}
			continue
		}
		if len(line) == 0 {
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
			src = convs.Call(src, false)
		}
		locations = append(locations, src)
	}
	return slices.Min(locations)
}

func Second(seeds []int, maps []convs) int {
	for idx := range seeds {
		if idx%2 == 0 {
			continue
		}
		seeds[idx] += seeds[idx-1]
	}
	for finalTarget := 0; finalTarget < (1 << 32); finalTarget++ {
		target := finalTarget
		isSeed := false
		for idx := len(maps) - 1; idx >= 0; idx-- {
			convs := maps[idx]
			target = convs.Call(target, true)
		}
		for i := 0; i < len(seeds); i += 2 {
			min, max := seeds[i], seeds[i+1]
			if min <= target && target <= max {
				isSeed = true
				break
			}
		}
		if isSeed {
			return finalTarget
		}
	}
	panic("not found")
}

func SecondImproved(seeds []int, maps []convs) int {
	source_ranges := []int{}
	for idx := range seeds {
		if idx%2 == 0 {
			continue
		}
		source_ranges = append(source_ranges, seeds[idx-1], seeds[idx]+seeds[idx-1])
	}
	idx := 0
	for {
		if idx >= len(source_ranges) {
			break
		}
		for _, convs := range maps {
			min, max := source_ranges[idx], source_ranges[idx+1]
			for _, conv := range convs {
				interMin, interMax, ok := intersection(min, max, conv.srcMin, conv.srcMax)
				if ok {
					source_ranges[idx] = conv.dstMin + (interMin - min)
					source_ranges[idx+1] = conv.dstMax + (interMax - max)
				}
				if otherRanges := outOfIntersection(min, max, conv.srcMin, conv.srcMax); len(otherRanges) > 0 {
					source_ranges = append(source_ranges, otherRanges...)
				}
				break
			}
		}
		idx += 2
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
	// r.Equal(69841803, Second(seeds, maps), "input p2")
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
