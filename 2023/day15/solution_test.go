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
		res = strings.Split(sc.Text(), ",")
	}
	return
}

func hash(s string) (res int) {
	for _, c := range s {
		res = ((res + int(c)) * 17) % 256
	}
	return
}

func step(boxes [][]string, step string, dict map[string]int) {
	if strings.Contains(step, "-") {
		h, ok := dict[step]
		if !ok {
			return
		}
		for idx, lens := range boxes[h] {
			if strings.HasPrefix(lens, step) {
				boxes[h][idx] = ""
				break
			}
		}
		delete(dict, step)
		return
	}
	tmp := strings.Split(step, "=")
	key := tmp[0] + "-"
	if h, ok := dict[key]; ok {
		for idx, lens := range boxes[h] {
			if strings.HasPrefix(lens, key) {
				boxes[h][idx] = key + tmp[1]
				break
			}
		}
	} else {
		h = hash(tmp[0])
		boxes[h] = append(boxes[h], key+tmp[1])
		dict[key] = h
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
			tmp := strings.Split(lens, "-")
			focalLength, _ := strconv.Atoi(tmp[1])
			res += (idx + 1) * slot * focalLength
		}
	}
	return
}

func Solve(input []string) (p1 int, p2 int) {
	boxes := make([][]string, 256)
	dict := make(map[string]int)
	for _, l := range input {
		p1 += hash(l)
		step(boxes, l, dict)
	}
	p2 = score(boxes)
	return
}

func TestDay15(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(1320, p1Ex, "example p1")
	r.Equal(145, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(517965, p1, "input p1")
	r.Equal(267372, p2, "input p2")
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
