package day06

import (
	"bufio"
	"fmt"
	"math"
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

// x (time - x) = distance
// x*time - x² = distance
// x² - x * time + distance = 0
// by construction of the exercise, we know that D = time² - 4*distance > 0
// so first root is (time - sqrt(D)) / 2
func NbWins(time, distance int) int {
	discriminant := float64(time*time - 4*distance)
	root := math.Floor((float64(time) - math.Sqrt(discriminant)) / 2)
	return 1 + time - 2*int(root+1)
}

func First(input []int) int {
	res := 1
	for i := 0; i < len(input); i += 2 {
		time, distance := input[i], input[i+1]
		res *= NbWins(time, distance)
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
	return NbWins(time, distance)
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
