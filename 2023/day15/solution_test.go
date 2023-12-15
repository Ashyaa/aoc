package day15

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
	input   = "./input.txt"
	example = "./example.txt"
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []string) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		// parsing here...
		res = strings.Split(sc.Text(), ",")
	}
	return
}

func hash(s string) (res int) {
	for _, c := range s {
		res += int(c)
		res *= 17
		res %= 256
	}
	return
}

func step(boxes [][]string, step string, dict map[string]int) {
	if strings.Contains(step, "-") {
		s := strings.Replace(step, "-", "", 1)
		if _, ok := dict[s]; !ok {
			return
		}
		h := hash(s)
		for idx, lens := range boxes[h] {
			if strings.HasPrefix(lens, s) {
				boxes[h][idx] = ""
				break
			}
		}
		delete(dict, s)
		return
	}
	tmp := strings.Split(step, "=")
	if h, ok := dict[tmp[0]]; ok {
		for idx, lens := range boxes[h] {
			if strings.HasPrefix(lens, tmp[0]) {
				boxes[h][idx] = tmp[0] + " " + tmp[1]
				break
			}
		}
	} else {
		h = hash(tmp[0])
		boxes[h] = append(boxes[h], tmp[0]+" "+tmp[1])
		dict[tmp[0]] = h
	}
}

func score(boxes [][]string) (res int) {
	for idx, b := range boxes {
		slot := 0
		for _, lens := range b {
			if lens == "" {
				continue
			}
			slot++
			tmp := strings.Split(lens, " ")
			focalLength, _ := strconv.Atoi(tmp[1])
			res += (idx + 1) * slot * focalLength
		}
	}
	return
}

func Solve(input []string) (p1 int, p2 int) {
	boxes := make([][]string, 256)
	dict := make(map[string]int)
	for i := 0; i < 256; i++ {
		boxes[i] = []string{}
	}
	for _, l := range input {
		p1 += hash(l)
		step(boxes, l, dict)
	}
	p2 = score(boxes)
	return
}

func TestDay15(t *testing.T) {
	r := R.New(t)
	r.Equal(30, hash("rn=1"))
	r.Equal(253, hash("cm-"))
	r.Equal(97, hash("qp=3"))
	r.Equal(47, hash("cm=2"))
	r.Equal(14, hash("qp-"))
	r.Equal(180, hash("pc=4"))
	r.Equal(9, hash("ot=9"))
	r.Equal(197, hash("ab=5"))
	r.Equal(48, hash("pc-"))
	r.Equal(214, hash("pc=6"))
	r.Equal(231, hash("ot=7"))
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(1320, p1Ex, "example p1")
	r.Equal(145, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(517965, p1, "input p1")
	r.Equal(0, p2, "input p2") // x < 270364
}

func BenchmarkDay15(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
