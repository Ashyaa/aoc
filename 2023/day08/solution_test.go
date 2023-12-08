package day08

import (
	"bufio"
	"fmt"
	"os"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	inputFile    = "./input.txt"
	exampleFile  = "./example.txt"
	example2File = "./example2.txt"
)

type node struct {
	L, R string
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (instructions string, nodes map[string]node) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	sc.Scan()
	instructions = sc.Text()
	nodes = map[string]node{}
	sc.Scan()
	for sc.Scan() {
		line := sc.Text()
		nodes[line[:3]] = node{L: line[7:10], R: line[12:15]}
	}
	return
}

func First(instructions string, nodes map[string]node) (res int) {
	curNode := "AAA"
	for curNode != "ZZZ" {
		idx := res % len(instructions)
		char := instructions[idx]
		if char == 'L' {
			curNode = nodes[curNode].L
		} else {
			curNode = nodes[curNode].R
		}
		res += 1
	}
	return
}

func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func LCM(integers ...int) int {
	if len(integers) < 2 {
		panic("not enough ints")
	}
	a, b := integers[0], integers[1]
	result := a * b / GCD(a, b)

	for i := 2; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}

func Second(instructions string, nodes map[string]node) (res int) {
	curNodes := make([]string, 0)
	for k := range nodes {
		if k[2] == 'A' {
			curNodes = append(curNodes, k)
		}
	}
	stepsPerNode := make([]int, len(curNodes))
	endCount := 0
	for endCount < len(curNodes) {
		idx := res % len(instructions)
		char := instructions[idx]
		for i := range curNodes {
			if stepsPerNode[i] > 0 {
				continue
			}
			if char == 'L' {
				curNodes[i] = nodes[curNodes[i]].L
			} else {
				curNodes[i] = nodes[curNodes[i]].R
			}
			if curNodes[i][2] == 'Z' {
				stepsPerNode[i] = res + 1
				endCount += 1
			}
		}
		res += 1
	}
	return LCM(stepsPerNode...)
}

func TestDay08(t *testing.T) {
	r := R.New(t)
	exInstructions, exNodes := ReadInput(exampleFile)
	exInstructions2, exNodes2 := ReadInput(example2File)
	instructions, nodes := ReadInput(inputFile)
	r.Equal(2, First(exInstructions, exNodes), "example p1")
	r.Equal(20221, First(instructions, nodes), "input p1")
	r.Equal(6, Second(exInstructions2, exNodes2), "example p2")
	r.Equal(14616363770447, Second(instructions, nodes), "input p2")
}

func BenchmarkDay08(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		instructions, nodes := ReadInput(inputFile)
		First(instructions, nodes)
		Second(instructions, nodes)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
