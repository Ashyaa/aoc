package day05

import (
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

type rule struct {
	a, b int
}

func toInt(s string) int {
	res, _ := strconv.Atoi(s)
	return res
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (rules []rule, updates [][]int) {
	raw, _ := os.ReadFile(filepath)
	tmp := strings.Split(string(raw), "\n\n")

	for _, line := range strings.Split(tmp[0], "\n") {
		pages := strings.Split(line, "|")
		rules = append(rules, rule{toInt(pages[0]), toInt(pages[1])})
	}

	for _, line := range strings.Split(tmp[1], "\n") {
		update := []int{}
		for _, page := range strings.Split(line, ",") {
			update = append(update, toInt(page))
		}
		updates = append(updates, update)
	}

	return
}

func isValid(update []int, rules []rule) bool {
	dic := map[int]int{}
	for i, v := range update {
		dic[v] = i
	}
	for _, rule := range rules {
		aIdx, okA := dic[rule.a]
		bIdx, okB := dic[rule.b]
		if !okA || !okB {
			continue
		}
		if aIdx > bIdx {
			return false
		}
	}
	return true
}

func applicableRules(dic map[int]int, rules []rule) (res []rule) {
	for _, rule := range rules {
		_, okA := dic[rule.a]
		_, okB := dic[rule.b]
		if !okA || !okB {
			continue
		}
		res = append(res, rule)
	}
	return res
}

func reorder(update []int, rules []rule) (res int) {
	dic := map[int]int{}
	for i, v := range update {
		dic[v] = i
	}
	for curIdx := 0; curIdx < (len(update)/2)+1; curIdx++ {
		rr := applicableRules(dic, rules)
		for k := range dic {
			matches := true
			for _, rr := range rr {
				if rr.b == k {
					matches = false
					break
				}
			}
			if matches {
				res = k
				delete(dic, k)
				break
			}
		}
	}
	return res
}

func Solve(rules []rule, updates [][]int) (p1 int, p2 int) {
	for _, update := range updates {
		ok := isValid(update, rules)
		if ok {
			pageIdx := (len(update) / 2)
			p1 += update[pageIdx]
			continue
		}
		p2 += reorder(update, rules)
	}
	return
}

func TestDay05(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(143, p1Ex, "example p1")
	r.Equal(123, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(4185, p1, "input p1")
	r.Equal(4480, p2, "input p2")
}

func BenchmarkDay05(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
