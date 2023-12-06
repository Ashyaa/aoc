package day06

import (
	"bufio"
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
func ReadInput(filepath string) (res []int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	sc.Scan()
	times := strings.Fields(sc.Text())
	sc.Scan()
	distances := strings.Fields(sc.Text())
	for i := 1; i < len(times); i++ {
		time, _ := strconv.Atoi(times[i])
		distance, _ := strconv.Atoi(distances[i])
		res = append(res, time, distance)
	}
	return
}

func First(input []int) int {
	res := 1
	for i := 0; i < len(input); i += 2 {
		time, distance := input[i], input[i+1]
		nbWins := 0
		for t := 1; t < (time+1)/2; t++ {
			d := t * (time - t)
			if d > distance {
				nbWins += 1
			}
		}
		nbWins *= 2
		if time%2 == 0 {
			nbWins += 1
		}
		res *= nbWins

	}
	return res
}

func Second(input []int) (res int) {
	timeStr, distanceStr := "", ""
	for i := 0; i < len(input); i += 2 {
		timeStr += strconv.Itoa(input[i])
		distanceStr += strconv.Itoa(input[i+1])
	}
	time, _ := strconv.Atoi(timeStr)
	distance, _ := strconv.Atoi(distanceStr)
	for t := 1; t < (time+1)/2; t++ {
		d := t * (time - t)
		if d > distance {
			res += 1
		}
	}
	res *= 2
	if time%2 == 0 {
		res += 1
	}
	return res
}

func TestDay06(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	input := ReadInput(inputFile)
	r.Equal(288, First(example), "example p1")
	r.Equal(3316275, First(input), "input p1")
	r.Equal(71503, Second(example), "example p2")
	r.Equal(27102791, Second(input), "input p2")
}

func BenchmarkDay06(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		input := ReadInput(inputFile)
		First(input)
		Second(input)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
