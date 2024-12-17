package day17

import (
	. "aoc/utils"
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

type Operand func(map[string]interface{}, int)

func incrementPointer(memory map[string]interface{}) {
	curptr := Registry(memory, "intptr")
	memory["intptr"] = curptr + 2
}

func dv(reg string, memory map[string]interface{}, operand int) {
	a := Registry(memory, "A")
	op := ComboOperand(memory, operand)
	memory[reg] = a / (1 << op)
	incrementPointer(memory)
}

func adv(memory map[string]interface{}, operand int) {
	dv("A", memory, operand)
}

func bxl(memory map[string]interface{}, operand int) {
	b := Registry(memory, "B")
	memory["B"] = b ^ operand
	incrementPointer(memory)
}

func bst(memory map[string]interface{}, operand int) {
	op := ComboOperand(memory, operand)
	memory["B"] = op % 8
	incrementPointer(memory)
}

func jnz(memory map[string]interface{}, operand int) {
	if Registry(memory, "A") == 0 {
		incrementPointer(memory)
		return
	}
	memory["intptr"] = operand
}

func bxc(memory map[string]interface{}, _ int) {
	b := Registry(memory, "B")
	c := Registry(memory, "C")
	memory["B"] = b ^ c
	incrementPointer(memory)
}

func out(memory map[string]interface{}, operand int) {
	value := ComboOperand(memory, operand) % 8
	memory["out"] = memory["out"].(string) + fmt.Sprintf("%d,", value)
	incrementPointer(memory)
}

func bdv(memory map[string]interface{}, operand int) {
	dv("B", memory, operand)
}

func cdv(memory map[string]interface{}, operand int) {
	dv("C", memory, operand)
}

var (
	oplist = []Operand{
		adv,
		bxl,
		bst,
		jnz,
		bxc,
		out,
		bdv,
		cdv,
	}
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (int, string) {
	s, _ := os.ReadFile(filepath)
	var a int
	var program string
	for i, line := range strings.Split(string(s), "\n") {
		if i == 0 {
			a = ToInt(line[12:])
		} else if i == 4 {
			program = line[9:]
		}
	}
	return a, program
}

func Registry(memory map[string]interface{}, id string) int {
	return memory[id].(int)
}

func ComboOperand(memory map[string]interface{}, op int) int {
	if op >= 7 {
		panic("reserved combo operand")
	}
	if op == 4 {
		return memory["A"].(int)
	}
	if op == 5 {
		return memory["B"].(int)
	}
	if op == 7 {
		return memory["C"].(int)
	}
	return op
}

func initMemory(a int) map[string]interface{} {
	return map[string]interface{}{
		"A":      a,
		"B":      0,
		"C":      0,
		"intptr": 0,
		"out":    "",
	}
}

func execute(a int, program []int) string {
	memory := initMemory(a)
	for {
		intptr := Registry(memory, "intptr")
		if intptr >= len(program) {
			break
		}
		opcode := program[intptr]
		op := program[intptr+1]
		oplist[opcode](memory, op)
	}
	return memory["out"].(string)
}

func Solve(a int, programStr string) (p1 string, p2 int) {
	program := Map(strings.Split(programStr, ","), ToInt)
	p1 = execute(a, program)
	exp := programStr + ","

	for i := 100100011178010; i > 0; i++ { // bruteforce ain't it
		sss := execute(i, program)
		if sss == exp {
			p2 = i
			break
		}
	}
	return
}

func TestDay17(t *testing.T) {
	r := R.New(t)
	// p1Ex, p2Ex := Solve(ReadInput(example))
	// r.Equal("4,6,3,5,6,3,5,2,1,0,", p1Ex, "example p1")
	// r.Equal(0, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal("1,5,7,4,1,6,0,3,0,", p1, "input p1")
	r.Equal(0, p2, "input p2")
}

func BenchmarkDay17(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
