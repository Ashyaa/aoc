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

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []string) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		// parsing here...
		res = append(res, sc.Text())
	}
	return
}

func isValid(buffer []rune, counts []int) bool {
	fields := strings.Fields(string(buffer))
	if len(fields) != len(counts) {
		return false
	}
	for idx, f := range fields {
		c := counts[idx]
		if len(f) != c {
			return false
		}
	}
	return true
}

func missingIndexes(s string) (res []int) {
	for idx, c := range s {
		if c == '?' {
			res = append(res, idx)
		}
	}
	return
}

func newSprings(combination, nbBits int) (res []int, sum int) {
	for shift := 0; shift < nbBits; shift++ {
		mask := 1 << shift
		bit := (combination & mask) >> shift
		res = append(res, bit)
		sum += bit
	}
	return
}

func compute(s, counts string) (res int) {
	springs := []int{}
	totalSprings := 0
	for _, rawCount := range strings.Split(counts, ",") {
		count, _ := strconv.Atoi(rawCount)
		totalSprings += count
		springs = append(springs, count)
	}
	curNbSprings := strings.Count(s, "#")
	toFind := totalSprings - curNbSprings
	missingIdxs := missingIndexes(s)
	nbMissing := len(missingIdxs)
	maxCombination := 1
	for i := 1; i <= toFind; i++ {
		maxCombination += 1 << (nbMissing - i)
	}
	for combination := (1 << toFind) - 1; combination < maxCombination; combination++ {
		toAdd, sum := newSprings(combination, nbMissing)
		if sum != toFind {
			continue
		}
		buffer := []rune(strings.ReplaceAll(s, ".", " "))
		for idx, newSpring := range toAdd {
			newChar := ' '
			if newSpring == 1 {
				newChar = '#'
			}
			buffer[missingIdxs[idx]] = newChar
		}
		if isValid(buffer, springs) {
			res += 1
		}
	}
	return
}

func Solve(input []string) (p1 int, p2 int) {
	for _, s := range input {
		tmp := strings.Split(s, " ")
		p1 += compute(tmp[0], tmp[1])
		// s1, s2 := tmp[0], tmp[1]
		// for i := 0; i < 4; i++ {
		// 	s1 += "?" + tmp[0]
		// 	s2 += "?" + tmp[1]
		// }
	}
	return
}

func TestDay12(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(21, p1Ex, "example p1")
	// r.Equal(525152, p2Ex, "example p2")
	r.Equal(0, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(7236, p1, "input p1")
	r.Equal(0, p2, "input p2")
}

func BenchmarkDay12(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
