package day02

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
	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []map[string]int) {
	data, _ := os.ReadFile(filepath)
	for _, line := range strings.Split(string(data), "\n") {
		tmp := strings.Split(strings.TrimSpace(line), ": ")[1]
		game := map[string]int{"red": 0, "green": 0, "blue": 0}
		for _, raw := range strings.Split(strings.ReplaceAll(tmp, ";", ","), ", ") {
			d := strings.Split(raw, " ")
			nb, _ := strconv.Atoi(d[0])
			game[d[1]] = max(game[d[1]], nb)
		}
		res = append(res, game)
	}
	return
}

func First(input []map[string]int) int {
	res := 0
	set := map[string]int{"red": 12, "green": 13, "blue": 14}
	for id, game := range input {
		ok := true
		for k, v := range game {
			if v > set[k] {
				ok = false
				break
			}
		}
		if ok {
			res += id + 1
		}
	}
	return res
}

func Second(input []map[string]int) int {
	res := 0
	for _, game := range input {
		p := 1
		for _, v := range game {
			p *= v
		}
		res += p
	}
	return res
}

func TestDay02(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	input := ReadInput(inputFile)
	r.Equal(8, First(example), "example p1")
	r.Equal(2283, First(input), "input p1")
	r.Equal(2286, Second(example), "example p2")
	r.Equal(78669, Second(input), "input p2")
}

func BenchmarkDay02(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		input := ReadInput(inputFile)
		n %= First(input)
		n %= Second(input)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
