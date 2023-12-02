package dayXX

import (
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) []string {
	data, _ := os.ReadFile(filepath)
	return strings.Split(string(data), "\n")
}

func First(input []string) interface{} {
	return nil
}

func Second(input []string) interface{} {
	return nil
}

func TestDayXX(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	input := ReadInput(inputFile)
	r.Equal(nil, First(example))
	r.Equal(nil, First(input))
	r.Equal(nil, Second(example))
	r.Equal(nil, Second(input))
}

func BenchmarkDayXX(b *testing.B) {
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
