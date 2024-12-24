package day24

import (
	. "aoc/utils"
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

type gate struct {
	a, op, b string
}

func (g gate) compute(memory map[string]int, gates map[string]gate) int {
	a, okA := memory[g.a]
	if !okA {
		a = gates[g.a].compute(memory, gates)
	}
	b, okB := memory[g.b]
	if !okB {
		b = gates[g.b].compute(memory, gates)
	}
	if g.op == "AND" {
		return a & b
	}
	if g.op == "OR" {
		return a | b
	}
	return a ^ b
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (map[string]int, map[string]gate) {
	raw, _ := os.ReadFile(filepath)
	sections := strings.Split(string(raw), "\n\n")
	memory := make(map[string]int)
	gates := make(map[string]gate)
	for _, line := range strings.Split(sections[0], "\n") {
		elems := strings.Split(line, ": ")
		memory[elems[0]] = ToInt(elems[1])
	}
	for _, line := range strings.Split(sections[1], "\n") {
		elems := strings.Split(line, " -> ")
		operation := strings.Split(elems[0], " ")
		gates[elems[1]] = gate{operation[0], operation[1], operation[2]}
	}
	return memory, gates
}

func assertCarryOperand(name string, gates map[string]gate, n int) (res []string) {
	g := gates[name]
	if g.op != "AND" { // carry part shall always be an AND
		res = append(res, name)
		return
	}
	if strings.ContainsAny(g.a, "xy") && strings.ContainsAny(g.b, "xy") {
		// operand is the AND between the two previous bits, no check there
	} else { // operand is the AND between the XOR of the two previous bits and the carry before
		a := gates[g.a]
		if a.op == "AND" && n > 2 {
			res = append(res, a.a)
		}
		b := gates[g.b]
		if b.op == "AND" && n > 2 {
			res = append(res, g.b)
		}
	}
	return
}

func assertBitOperand(name string, gates map[string]gate, n int) (res []string) {
	g := gates[name]
	switch g.op {
	case "AND": // invalid if not the carry from the very first bit
		if n != 1 {
			res = append(res, name)
		}
	case "XOR": // sum part
		if !(strings.ContainsAny(g.a, "xy") && strings.ContainsAny(g.b, "xy")) || ToInt(g.a[1:]) != n {
			res = append(res, name)
		}
	case "OR": // carry part
		res = append(res, assertCarryOperand(g.a, gates, n)...)
		res = append(res, assertCarryOperand(g.b, gates, n)...)
	}
	return
}

func assertBit(name string, gates map[string]gate, n int) (res []string) {
	g := gates[name]
	if g.op != "XOR" { // sum part shall always be a XOR
		res = append(res, name)
		return
	}
	res = append(res, assertBitOperand(g.a, gates, n)...)
	res = append(res, assertBitOperand(g.b, gates, n)...)
	return
}

func Solve(memory map[string]int, gates map[string]gate) (p1 int, p2 string) {
	i, ex := 0, len(memory) <= 10
	for {
		g, ok := gates[fmt.Sprintf("z%02d", i)]
		if !ok {
			break
		}
		p1 += g.compute(memory, gates) << i
		i++
	}
	if ex {
		return
	}

	diff, shift := p1, 0
	res := NewSet[string]() // use a set to avoid adding duplicates when traversing carry blocks
	for diff != 0 {
		key := fmt.Sprintf("z%02d", shift)
		err := assertBit(key, gates, shift)
		if diff>>1 != 0 { // avoid adding the XOR for the most significant bit as it is an odd case
			res.Add(err...)
		}
		shift++
		diff = diff >> 1
	}
	r := res.ToSlice()
	slices.Sort(r)
	p2 = strings.Join(r, ",")

	return
}

func TestDay24(t *testing.T) {
	r := R.New(t)
	p1Ex, _ := Solve(ReadInput(example))
	r.Equal(4, p1Ex, "example p1")
	p1Ex2, _ := Solve(ReadInput(example2))
	r.Equal(2024, p1Ex2, "example 2 p1")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(56278503604006, p1, "input p1")
	r.Equal("bhd,brk,dhg,dpd,nbf,z06,z23,z38", p2, "input p2")
}

func BenchmarkDay24(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
