package day22

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"sort"
	"strconv"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

var (
	toStr = strconv.Itoa
)

func fromStr(s string) int {
	res, _ := strconv.Atoi(s)
	return res
}

type Brick struct {
	XMin, XMax int
	YMin, YMax int
	ZMin, ZMax int
}

func NewBrick(line string) Brick {
	splits := strings.Split(strings.ReplaceAll(line, "~", ","), ",")
	xmin, xmax := min(fromStr(splits[0]), fromStr(splits[3])), max(fromStr(splits[0]), fromStr(splits[3]))
	ymin, ymax := min(fromStr(splits[1]), fromStr(splits[4])), max(fromStr(splits[1]), fromStr(splits[4]))
	zmin, zmax := min(fromStr(splits[2]), fromStr(splits[5])), max(fromStr(splits[2]), fromStr(splits[5]))
	return Brick{xmin, xmax, ymin, ymax, zmin, zmax}
}

func (b Brick) Volume() (res []string) {
	for x := b.XMin; x <= b.XMax; x++ {
		for y := b.YMin; y <= b.YMax; y++ {
			for z := b.ZMin; z <= b.ZMax; z++ {
				res = append(res, toStr(x)+"."+toStr(y)+"."+toStr(z))
			}
		}
	}
	return
}

func (b Brick) Top() (res []string) {
	z := toStr(b.ZMax)
	for x := b.XMin; x <= b.XMax; x++ {
		for y := b.YMin; y <= b.YMax; y++ {
			res = append(res, toStr(x)+"."+toStr(y)+"."+z)
		}
	}
	return
}

func (b Brick) IsSettled(surface map[string]bool) bool {
	if b.ZMin == 1 {
		return true
	}
	if len(surface) == 0 {
		return false
	}
	z := toStr(b.ZMin - 1)
	for x := b.XMin; x <= b.XMax; x++ {
		for y := b.YMin; y <= b.YMax; y++ {
			k := toStr(x) + "." + toStr(y) + "." + z
			if _, ok := surface[k]; ok {
				return true
			}
		}
	}
	return false
}

func (b *Brick) Fall() {
	b.ZMin--
	b.ZMax--
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []Brick) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, NewBrick(sc.Text()))
	}
	return
}

func SettledBricks(bricks []Brick, surface map[string]bool) (settled, notSettled []Brick) {
	for _, b := range bricks {
		if b.IsSettled(surface) {
			settled = append(settled, b)
		} else {
			notSettled = append(notSettled, b)
		}
	}
	return
}

func Surface(bricks []Brick) map[string]bool {
	res := make(map[string]bool)
	for _, b := range bricks {
		for _, coord := range b.Top() {
			res[coord] = true
		}
	}
	return res
}

func Fall(bricks []Brick) []Brick {
	var settled, newSettled []Brick
	notSettled := bricks
	surface := map[string]bool{}
	for len(notSettled) > 0 {
		newSettled, notSettled = SettledBricks(notSettled, surface)
		if len(newSettled) > 0 {
			settled = append(settled, newSettled...)
			surface = Surface(settled)
			continue
		}
		for idx := range notSettled {
			notSettled[idx].Fall()
		}
	}
	return settled
}

func GetVolume(bricks []Brick) map[string]int {
	volume := map[string]int{}
	for idx, b := range bricks {
		for _, coord := range b.Volume() {
			volume[coord] = idx
		}
	}
	return volume
}

func GetRelationship(bricks []Brick) ([][]int, [][]int) {
	volume := GetVolume(bricks)
	above, below := make([][]int, len(bricks)), make([][]int, len(bricks))
	for idx, b := range bricks {
		za, zb := toStr(b.ZMax+1), toStr(b.ZMin-1)
		for x := b.XMin; x <= b.XMax; x++ {
			for y := b.YMin; y <= b.YMax; y++ {
				if other, ok := volume[toStr(x)+"."+toStr(y)+"."+za]; ok {
					above[idx] = append(above[idx], other)
				}
				if other, ok := volume[toStr(x)+"."+toStr(y)+"."+zb]; ok {
					below[idx] = append(below[idx], other)
				}
			}
		}
		sort.Ints(above[idx])
		above[idx] = slices.Compact(above[idx])
		sort.Ints(below[idx])
		below[idx] = slices.Compact(below[idx])
	}
	return above, below
}

func all(below []int, falls map[int]bool) bool {
	for _, other := range below {
		if _, ok := falls[other]; !ok {
			return false
		}
	}
	return true
}

func collapse(above, below [][]int, idx int) (res int) {
	falls := map[int]bool{idx: true}
	q := []int{idx}
	for len(q) > 0 {
		cur := q[0]
		q = q[1:]
		for _, other := range above[cur] {
			_, alreadyFalling := falls[other]
			if all(below[other], falls) && !alreadyFalling {
				falls[other] = true
				q = append(q, other)
				res++
			}
		}
	}
	return
}

func Solve(input []Brick) (p1 int, p2 int) {
	fallen := Fall(input)
	above, below := GetRelationship(fallen)
	for b := range fallen {
		collapsed := collapse(above, below, b)
		p2 += collapsed
		if collapsed == 0 {
			p1++
		}
	}
	return
}

func TestDay22(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(5, p1Ex, "example p1")
	r.Equal(7, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(517, p1, "input p1")
	r.Equal(61276, p2, "input p2")
}

func BenchmarkDay22(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
