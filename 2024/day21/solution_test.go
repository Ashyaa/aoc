package day21

import (
	. "aoc/utils"
	"bufio"
	"fmt"
	"os"
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
	doorButtons = []rune{
		'7',
		'8',
		'9',
		'4',
		'5',
		'6',
		'1',
		'2',
		'3',
		'0',
		'A',
	}
	door = map[rune]Coord{
		'7': {X: 0, Y: 0},
		'8': {X: 0, Y: 1},
		'9': {X: 0, Y: 2},
		'4': {X: 1, Y: 0},
		'5': {X: 1, Y: 1},
		'6': {X: 1, Y: 2},
		'1': {X: 2, Y: 0},
		'2': {X: 2, Y: 1},
		'3': {X: 2, Y: 2},
		'0': {X: 3, Y: 1},
		'A': {X: 3, Y: 2},
	}
	robotButtons = []rune{
		'<',
		'v',
		'>',
		'^',
		'A',
	}
	robot = map[rune]Coord{
		'<': {X: 1, Y: 0},
		'v': {X: 1, Y: 1},
		'>': {X: 1, Y: 2},
		'^': {X: 0, Y: 1},
		'A': {X: 0, Y: 2},
	}

	doorPaths  = genPaths(doorButtons, door)
	robotPaths = genPaths(robotButtons, robot)
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []string) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, sc.Text())
	}
	return
}

func gen(s rune, count int) string {
	res := []rune{}
	for range count {
		res = append(res, s)

	}
	return string(res)
}

func pathName(start, end rune) string {
	return string([]rune{start, end})
}

func genPaths(btns []rune, coords map[rune]Coord) map[string]string {
	keypad := len(btns) == 11
	res := make(map[string]string)
	for i, start := range btns {
		startPos := coords[start]
		res[pathName(start, start)] = "A"
		for j := i + 1; j < len(btns); j++ {
			end := btns[j]
			p1, p2 := pathName(start, end), pathName(end, start)
			ver := coords[end].X - startPos.X
			cVer, cVerRev := 'v', '^'
			if ver < 0 {
				cVerRev, cVer = 'v', '^'
				ver *= -1
			}
			hor := coords[end].Y - startPos.Y
			cHor, cHorRev := '>', '<'
			if hor < 0 {
				cHorRev, cHor = '>', '<'
				hor *= -1
			}

			if (keypad && startPos.Y == 0 && coords[end].X == 3) || (!keypad && startPos.Y == 0 && coords[end].X == 0) {
				res[p1] = gen(cHor, hor) + gen(cVer, ver) + "A"
				res[p2] = gen(cVerRev, ver) + gen(cHorRev, hor) + "A"
			} else if coords[end].Y-startPos.Y < 0 {
				res[p1] = gen(cHor, hor) + gen(cVer, ver) + "A"
				res[p2] = gen(cVerRev, ver) + gen(cHorRev, hor) + "A"
			} else if coords[end].Y-startPos.Y >= 0 {
				res[p1] = gen(cVer, ver) + gen(cHor, hor) + "A"
				res[p2] = gen(cHorRev, hor) + gen(cVerRev, ver) + "A"
			}
		}
	}
	return res
}

func pressPad(code string, pths map[string]string) (res string) {
	cur := 'A'
	for _, c := range code {
		pth := pathName(cur, c)
		res += pths[pth]
		cur = c
	}
	return
}

func getSteps(s string) (res []string) {
	ss := strings.Split(s, "A")
	for i, c := range ss {
		if i == len(ss)-1 {
			res = append(res, c)
		} else {
			res = append(res, c+"A")
		}
	}
	return
}

func recurse(code string, maxRobots, robot int, cache map[string][]int) int {
	if val, ok := cache[code]; ok {
		if val[robot-1] != 0 {
			return val[robot-1]
		}
	} else {
		cache[code] = make([]int, maxRobots)
	}

	seq := pressPad(code, robotPaths)
	cache[code][0] = len(seq)

	if robot == maxRobots {
		return len(seq)
	}

	count := 0
	for _, s := range getSteps(seq) {
		c := recurse(s, maxRobots, robot+1, cache)
		if _, ok := cache[s]; !ok {
			cache[s] = make([]int, maxRobots)
		}
		cache[s][0] = c
		count += c
	}

	cache[code][robot-1] = count
	return count
}

func press(code string, nb int) (res int) {
	presses := pressPad(code, doorPaths)
	return recurse(presses, nb, 1, make(map[string][]int))
}

func Solve(input []string) (p1 int, p2 int) {
	for _, code := range input {
		num := ToInt(code[:3])
		presses := pressPad(code, doorPaths)
		p1 += num * recurse(presses, 2, 1, make(map[string][]int))
		p2 += num * recurse(presses, 25, 1, make(map[string][]int))
	}
	return
}

func TestDay21(t *testing.T) {
	r := R.New(t)
	r.Equal(68, press("029A", 2), "029A")
	r.Equal(60, press("980A", 2), "980A")
	r.Equal(68, press("179A", 2), "179A")
	r.Equal(64, press("456A", 2), "456A")
	r.Equal(64, press("379A", 2), "379A")
	p1Ex, _ := Solve(ReadInput(example))
	r.Equal(126384, p1Ex, "example p1")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(219366, p1, "input p1")
	r.Equal(271631192020464, p2, "input p2")
}

func BenchmarkDay21(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
