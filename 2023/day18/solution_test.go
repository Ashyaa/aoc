package day18

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
	right = iota
	down
	left
	up
	input   = "./input.txt"
	example = "./example.txt"
)

var (
	charToDir = map[string]int{
		"U": up,
		"R": right,
		"D": down,
		"L": left,
	}
	offset = []int{
		0, 1,
		1, 0,
		0, -1,
		-1, 0,
	}
)

type line struct {
	dir, count   int
	dir2, count2 int
}

type point struct {
	x, y int
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []line) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		fields := strings.Fields(sc.Text())
		dir := charToDir[fields[0]]
		count, _ := strconv.Atoi(fields[1])
		dir2, _ := strconv.Atoi(fields[2][7:8])
		count2, _ := strconv.ParseInt(fields[2][2:7], 16, 64)
		res = append(res, line{dir, count, dir2, int(count2)})
	}
	return
}

func dist(x, y int) int {
	if x < y {
		return y - x
	}
	if x > y {
		return x - y
	}
	return 0
}

// shoelace formula computes the area of the polygon
// with Pick's theorem, we can deduce the number of inner points i:
// a == i + (b/2) - 1 => i = a + 1 - (b/2)
// with a the area, b the number of points on the boundary
func compute(pts []point) int {
	sum := 0
	p0 := pts[len(pts)-1]
	boundary := 0
	for _, p1 := range pts {
		sum += p0.y*p1.x - p0.x*p1.y
		boundary += dist(p0.x, p1.x) + dist(p0.y, p1.y)
		p0 = p1
	}
	inner := sum/2 + 1 - boundary/2
	return boundary + inner
}

func Solve(input []line, p2 bool) int {
	x, y := 1, 1
	pts := []point{{x, y}}
	for idx, l := range input {
		if idx == len(input)-1 {
			break
		}
		dir := l.dir
		count := l.count
		if p2 {
			dir = l.dir2
			count = l.count2
		}
		dx, dy := offset[2*dir], offset[2*dir+1]
		nx, ny := x+count*dx, y+count*dy
		pts = append(pts, point{nx, ny})
		x, y = nx, ny
	}
	return compute(pts)
}

func TestDay18(t *testing.T) {
	r := R.New(t)
	r.Equal(62, Solve(ReadInput(example), false), "example p1")
	r.Equal(952408144115, Solve(ReadInput(example), true), "example p2")
	r.Equal(41019, Solve(ReadInput(input), false), "input p1")
	r.Equal(96116995735219, Solve(ReadInput(input), true), "input p2")
}

func BenchmarkDay18(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		in := ReadInput(input)
		Solve(in, false)
		Solve(in, true)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
