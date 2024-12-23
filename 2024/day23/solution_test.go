package day23

import (
	. "aoc/utils"
	"bufio"
	"fmt"
	"os"
	"slices"
	"sort"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

type connection struct {
	a, b string
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []connection) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		conn := strings.Split(sc.Text(), "-")
		res = append(res, connection{conn[0], conn[1]})
	}
	return
}

func grpId(a []string) string {
	sort.Strings(a)
	return strings.Join(a, ",")
}

func findLargest(conn map[string]Set[string], trios map[string][]string) string {
	currentGroups := [][]string{}
	for _, t := range trios {
		currentGroups = append(currentGroups, t)
	}
	for {
		nextGroups := [][]string{}
		seen := NewSet[string]()

		for _, group := range currentGroups {
			inter := conn[group[0]]
			for _, other := range group[1:] {
				inter = inter.Intersection(conn[other])
			}
			for i := range inter {
				grp := append(slices.Clone(group), i)
				id := grpId(grp)
				if seen.Contains(id) {
					continue
				}
				seen.Add(id)
				nextGroups = append(nextGroups, grp)
			}
		}

		if len(nextGroups) == 0 {
			break
		}
		currentGroups = nextGroups
	}
	return grpId(currentGroups[0])
}

func Solve(input []connection) (p1 int, p2 string) {
	neighbours := map[string]Set[string]{}
	for _, conn := range input {
		_, okA := neighbours[conn.a]
		if !okA {
			neighbours[conn.a] = NewSet[string]()
		}
		grpA := neighbours[conn.a]
		grpA.Add(conn.b)
		neighbours[conn.a] = grpA

		_, okB := neighbours[conn.b]
		if !okB {
			neighbours[conn.b] = NewSet[string]()
		}
		grpB := neighbours[conn.b]
		grpB.Add(conn.a)
		neighbours[conn.b] = grpB
	}
	trios := map[string][]string{}
	for computer, others := range neighbours {
		for other := range others {
			for i := range others.Intersection(neighbours[other]) {
				trio := []string{computer, other, i}
				trios[grpId(trio)] = trio
			}
		}
	}

	for _, trio := range trios {
		if trio[0][0] == 't' || trio[1][0] == 't' || trio[2][0] == 't' {
			p1++
		}
	}
	p2 = findLargest(neighbours, trios)
	return
}

func TestDay23(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(7, p1Ex, "example p1")
	r.Equal("co,de,ka,ta", p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(1419, p1, "input p1")
	r.Equal("af,aq,ck,ee,fb,it,kg,of,ol,rt,sc,vk,zh", p2, "input p2")
}

func BenchmarkDay23(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
