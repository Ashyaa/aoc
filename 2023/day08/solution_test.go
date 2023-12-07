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
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
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

func First(input []string) interface{} {
	return nil
}

func Second(input []string) interface{} {
	return nil
}

func TestDay08(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	input := ReadInput(inputFile)
	r.Equal(nil, First(example), "example p1")
	r.Equal(nil, First(input), "input p1")
	r.Equal(nil, Second(example), "example p2")
	r.Equal(nil, Second(input), "input p2")
}

func BenchmarkDay08(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		input := ReadInput(inputFile)
		// n %= First(input)
		First(input)
		// n %= Second(input)
		Second(input)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}