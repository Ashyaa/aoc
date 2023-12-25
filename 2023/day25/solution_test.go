package day25

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
	"github.com/twmb/algoimpl/go/graph"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res map[string][]string) {
	s, _ := os.Open(filepath)
	res = make(map[string][]string)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		fields := strings.Fields(strings.ReplaceAll(sc.Text(), ":", ""))
		if _, ok := res[fields[0]]; !ok {
			res[fields[0]] = []string{}
		}
		for i := 1; i < len(fields); i++ {
			if _, ok := res[fields[i]]; !ok {
				res[fields[i]] = []string{}
			}
			res[fields[0]] = append(res[fields[0]], fields[i])
			res[fields[i]] = append(res[fields[i]], fields[0])
		}
	}
	return
}

func Solve(input map[string][]string) (res int) {
	g := graph.New(graph.Undirected)
	nodes := make(map[string]graph.Node)
	for k := range input {
		n := g.MakeNode()
		*n.Value = k
		nodes[k] = n
	}
	for k, v := range input {
		for _, other := range v {
			g.MakeEdge(nodes[k], nodes[other])
		}
	}
	for _, e := range g.RandMinimumCut(500, 16) {
		g.RemoveEdge(e.Start, e.End)
	}
	groups := g.StronglyConnectedComponents()
	return len(groups[0]) * len(groups[1])
}

func TestDay25(t *testing.T) {
	r := R.New(t)
	ex := Solve(ReadInput(example))
	r.Equal(54, ex, "example p1")
	res := Solve(ReadInput(input))
	r.Equal(558376, res, "example p1")
}

func BenchmarkDay25(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
