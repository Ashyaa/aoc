package day20

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input    = "./input.txt"
	example  = "./example.txt"
	example2 = "./example2.txt"
)

type signal struct {
	src   string
	dests []string
	v     bool
}

type block interface {
	Name() string
	Run(string, bool) (signal, bool)
	Dests() []string
	Srcs() []string
	SetInput(string)
}

type Flipflop struct {
	name  string
	dests []string
	srcs  []string
	m     bool
}

func (f *Flipflop) Name() string {
	return f.name
}

func (f *Flipflop) Run(_ string, s bool) (signal, bool) {
	if s {
		return signal{}, false
	}
	f.m = !f.m
	return signal{f.name, f.dests, f.m}, true
}

func (f *Flipflop) SetInput(s string) {
	if f.srcs == nil {
		f.srcs = make([]string, 0)
	}
	f.srcs = append(f.srcs, s)
}

func (f *Flipflop) Srcs() []string {
	return f.srcs
}

func (f *Flipflop) Dests() []string {
	return f.dests
}

type Broadcast struct {
	name  string
	dests []string
}

func (b *Broadcast) Name() string {
	return b.name
}

func (b *Broadcast) Run(_ string, s bool) (signal, bool) {
	return signal{b.name, b.dests, s}, true
}

func (b *Broadcast) SetInput(_ string) {
}

func (b *Broadcast) Srcs() []string {
	return []string{}
}

func (b *Broadcast) Dests() []string {
	return b.dests
}

type Conjunction struct {
	name  string
	dests []string
	mem   map[string]bool
}

func (c *Conjunction) Name() string {
	return c.name
}

func (c *Conjunction) Run(src string, s bool) (signal, bool) {
	count := 0
	v := true
	c.mem[src] = s
	for _, v := range c.mem {
		if v {
			count += 1
		}
	}
	if count == len(c.mem) {
		v = false
	}
	return signal{c.name, c.dests, v}, true
}

func (c *Conjunction) SetInput(s string) {
	if c.mem == nil {
		c.mem = make(map[string]bool)
	}
	c.mem[s] = false
}

func (c *Conjunction) Srcs() []string {
	srcs := []string{}
	for s := range c.mem {
		srcs = append(srcs, s)
	}
	return srcs
}

func (c *Conjunction) Dests() []string {
	return c.dests
}

func parseLine(s string) (res block) {
	tmp := strings.Split(s, " -> ")
	switch tmp[0][0:1] {
	case "%":
		res = &Flipflop{name: tmp[0][1:], dests: strings.Split(tmp[1], ", ")}
	case "&":
		res = &Conjunction{name: tmp[0][1:], dests: strings.Split(tmp[1], ", ")}
	default:
		res = &Broadcast{name: tmp[0], dests: strings.Split(tmp[1], ", ")}
	}
	return res
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) map[string]block {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	res := make(map[string]block)
	for sc.Scan() {
		block := parseLine(sc.Text())
		res[block.Name()] = block
	}
	for k, v := range res {
		for _, d := range v.Dests() {
			if d == "output" || d == "rx" {
				continue
			}
			res[d].SetInput(k)
		}
	}
	return res
}

func Press(input map[string]block, wanted map[string]int) (int, int, map[string]bool) {
	low, high := 1, 0
	seen := make(map[string]bool)
	for k := range wanted {
		seen[k] = false
	}
	fifo := []signal{
		{
			dests: []string{"broadcaster"},
			v:     false,
		},
	}
	for len(fifo) > 0 {
		cur := fifo[0]
		fifo = fifo[1:]
		for _, d := range cur.dests {
			b, ok := input[d]
			if !ok {
				continue
			}
			if _, ok := seen[cur.src]; ok && cur.v {
				seen[cur.src] = true
			}
			if sig, ok := b.Run(cur.src, cur.v); ok {
				fifo = append(fifo, sig)
				if sig.v {
					high += len(sig.dests)
				} else {
					low += len(sig.dests)
				}
			}
		}
	}
	return low, high, seen
}

func Solve(input map[string]block) (p1 int, p2 int) {
	low, high := 0, 0
	wanted := map[string]int{}
	for _, b := range input {
		if !slices.Contains(b.Dests(), "rx") {
			continue
		}
		for _, b2 := range b.Srcs() {
			wanted[b2] = 0
		}
		break
	}
	for i := 0; i < 1000; i++ {
		l, h, _ := Press(input, wanted)
		low += l
		high += h
	}
	count := 1000
	found := 0
	p2 = 1
	for found < len(wanted) {
		count++
		_, _, seen := Press(input, wanted)
		for _, v := range seen {
			if v {
				p2 *= count
				found++
			}
		}
	}
	return low * high, p2
}

func TestDay20(t *testing.T) {
	r := R.New(t)
	p1Ex, _ := Solve(ReadInput(example))
	r.Equal(32000000, p1Ex, "example p1")
	p1Ex, _ = Solve(ReadInput(example2))
	r.Equal(11687500, p1Ex, "example p1")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(777666211, p1, "input p1")
	r.Equal(243081086866483, p2, "input p2")
}

func BenchmarkDay20(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
