package day19

import (
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
func ReadInput(filepath string) (have, wanted []string) {
	raw, _ := os.ReadFile(filepath)
	lines := strings.Split(string(raw), "\n")
	have = strings.Split(lines[0], ", ")
	wanted = lines[2:]
	return
}

func canSplit(cur string, have []string, cache map[string]int) (res int) {
	if v, ok := cache[cur]; ok {
		return v
	}
	if cur == "" {
		return cache[cur]
	}

	for _, w := range have {
		if !strings.HasPrefix(cur, w) {
			continue
		}
		res += canSplit(cur[len(w):], have, cache)
	}

	cache[cur] = res

	return cache[cur]
}

func Solve(have, wanted []string) (p1 int, p2 int) {
	for _, w := range wanted {
		permutations := canSplit(w, have, map[string]int{"": 1})
		if permutations > 0 {
			p1++
		}
		p2 += permutations
	}
	return
}

func TestDay19(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(6, p1Ex, "example p1")
	r.Equal(16, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(302, p1, "input p1")
	r.Equal(771745460576799, p2, "input p2")
}

func BenchmarkDay19(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
