package day13

import (
	U "aoc/utils"
	"fmt"
	"math"
	"os"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
	p2Dist  = 10000000000000
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res [][3]U.Coord) {
	raw, _ := os.ReadFile(filepath)
	for _, tmp := range strings.Split(string(raw), "\n\n") {
		lines := strings.Split(tmp, "\n")
		btnA := strings.Split(lines[0][10:], ", ")
		btnB := strings.Split(lines[1][10:], ", ")
		prize := strings.Split(lines[2][7:], ", ")
		res = append(res, [3]U.Coord{
			{X: U.ToInt(btnA[0][2:]), Y: U.ToInt(btnA[1][2:])},
			{X: U.ToInt(btnB[0][2:]), Y: U.ToInt(btnB[1][2:])},
			{X: U.ToInt(prize[0][2:]), Y: U.ToInt(prize[1][2:])},
		})
	}
	return
}

func GCD(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

// computes the (x, y) being the coordinates of the intersection
// of the ax * x + bx * y = cx and ay * x + by * y = cy lines
// if x and y are not integers, the function returns 0, 0 (no integer solution)
func diophantienne(ax, bx, cx, dx, ay, by, cy, dy int) (int, int) {
	if cx%dx != 0 || cy%dy != 0 {
		return 0, 0
	}
	x := float64(cy*bx-cx*by) / float64(ay*bx-ax*by)
	y := float64(cy*ax-ay*cx) / float64(by*ax-bx*ay)
	if math.Round(x) != x || math.Round(y) != y {
		return 0, 0
	}
	return int(x), int(y)
}

func Solve(input [][3]U.Coord) (p1 int, p2 int) {
	for _, game := range input {
		btnA, btnB, prize := game[0], game[1], game[2]
		gcdx := GCD(btnA.X, btnB.X)
		gcdy := GCD(btnA.Y, btnB.Y)
		a1, b1 := diophantienne(btnA.X, btnB.X, prize.X, gcdx, btnA.Y, btnB.Y, prize.Y, gcdy)
		p1 += 3*a1 + b1
		a2, b2 := diophantienne(btnA.X, btnB.X, prize.X+p2Dist, gcdx, btnA.Y, btnB.Y, prize.Y+p2Dist, gcdy)
		p2 += 3*a2 + b2
	}
	return
}

func TestDay13(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(480, p1Ex, "example p1")
	r.Equal(875318608908, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(31552, p1, "input p1")
	r.Equal(95273925552482, p2, "input p2")
}

func BenchmarkDay13(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
