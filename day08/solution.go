package day8

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
	"time"
)

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}

var input = "./input.txt"

type operator func(int, int, int) (int, int)

var operators = map[string]operator{
	"nop": func(x, y, z int) (int, int) { return y + 1, z },
	"acc": func(x, y, z int) (int, int) { return y + 1, z + x },
	"jmp": func(x, y, z int) (int, int) { return x + y, z },
}

// Command in the program
type Command struct {
	typ string
	arg int
}

func (o *Command) isAcc() bool {
	return o.typ == "acc"
}

func (o *Command) invert() {
	switch o.typ {
	case "nop":
		o.typ = "jmp"
	case "jmp":
		o.typ = "nop"
	}
}

func (o *Command) execute(index, count int) (int, int) {
	return operators[o.typ](o.arg, index, count)
}

// ReadInput retrieves the content of the input file
func ReadInput() (res []Command) {
	data, _ := ioutil.ReadFile(input)
	for _, line := range strings.Split(string(data), "\n") {
		substr := strings.Split(line, " ")
		arg, _ := strconv.Atoi(substr[1])
		res = append(res, Command{substr[0], arg})
	}
	return
}

func execute(code []Command, index, count int) (int, error) {
	visited := make(map[int]bool)
	for index >= 0 && index < len(code) {
		if _, ok := visited[index]; ok {
			return count, fmt.Errorf("looped")
		}
		visited[index] = true
		index, count = code[index].execute(index, count)
	}
	return count, nil
}

// Step1 solves step 1
func Step1(code []Command) int {
	defer timeTrack(time.Now(), "Step 1")
	res, _ := execute(code, 0, 0)
	return res
}

func altExecute(code []Command, index, count int) (int, error) {
	code[index].invert()
	return execute(code, index, count)
}

// Step2 solves step 2
func Step2(code []Command) int {
	defer timeTrack(time.Now(), "Step 2")
	index, count := 0, 0
	for index >= 0 && index < len(code) {
		cmd := code[index]
		if !cmd.isAcc() {
			res, err := altExecute(code, index, count)
			if err == nil {
				return res
			}
		}
		index, count = cmd.execute(index, count)
	}
	return -1
}
