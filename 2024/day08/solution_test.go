package day08

import (
	U "aoc/utils"
	"bufio"
	"fmt"
	"os"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) U.Matrix[rune] {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	buf := make([][]rune, 0)
	for sc.Scan() {
		line := []rune(sc.Text())
		buf = append(buf, line)
	}
	return U.NewMatrix(buf)
}

func Solve(input U.Matrix[rune]) (p1 int, p2 int) {
	antennasByFreq := make(map[rune][]U.Coord)
	// save antenna location by frequencies
	for x := range input.Lines() {
		for y := range input.Columns() {
			freq := input.At(x, y)
			if freq == '.' {
				continue
			}
			if _, ok := antennasByFreq[freq]; !ok {
				antennasByFreq[freq] = []U.Coord{}
			}
			antennasByFreq[freq] = append(antennasByFreq[freq], U.Coord{X: x, Y: y})
		}
	}
	res := U.Set[U.Coord]{}
	res2 := U.Set[U.Coord]{}
	// for each couple of antennas
	for _, antennas := range antennasByFreq {
		nbAntennas := len(antennas)
		if nbAntennas < 2 {
			continue
		}
		for i := 0; i < nbAntennas; i++ {
			a1 := antennas[i]
			res2.Add(a1) // antennas are all antinodes if there are at least two of them
			for j := i + 1; j < nbAntennas; j++ {
				a2 := antennas[j]
				distX, distY := a2.X-a1.X, a2.Y-a1.Y // vector to be applies to the antenna location
				k := 1
				for { // loop on one direction until out of bounds
					antinode1 := U.Coord{X: a1.X - k*distX, Y: a1.Y - k*distY}
					if input.InBounds(antinode1.X, antinode1.Y) {
						if k == 1 { // add only the first found antinode for part 1
							res.Add(antinode1)
						}
						res2.Add(antinode1)
					} else {
						break
					}
					k++
				}
				k = 1
				for { // loop on the other direction until out of bounds
					antinode2 := U.Coord{X: a2.X + k*distX, Y: a2.Y + k*distY}
					if input.InBounds(antinode2.X, antinode2.Y) {
						if k == 1 { // add only the first found antinode for part 1
							res.Add(antinode2)
						}
						res2.Add(antinode2)
					} else {
						break
					}
					k++
				}
			}
		}
	}
	return len(res), len(res2)
}

func TestDay08(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(14, p1Ex, "example p1")
	r.Equal(34, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(379, p1, "input p1")
	r.Equal(1339, p2, "input p2")
}

func BenchmarkDay08(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
