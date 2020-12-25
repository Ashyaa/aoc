package day10

import (
	"io/ioutil"
	"log"
	"sort"
	"strconv"
	"strings"
	"time"
)

var input = "./input.txt"

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}

// ReadInput retrieves the content of the input file
func ReadInput() (res []int) {
	data, _ := ioutil.ReadFile(input)
	res = append(res, 0)
	for _, line := range strings.Split(strings.TrimRight(string(data), "\n"), "\n") {
		n, _ := strconv.Atoi(line)
		res = append(res, n)
	}
	sort.Ints(res)
	res = append(res, res[len(res)-1]+3)
	return
}

// Step1 solves step 1
func Step1(numbers []int) int {
	defer timeTrack(time.Now(), "Step 1")
	jolt1, jolt3 := 0, 0
	for i, n := range numbers {
		if i == 0 {
			continue
		}
		if n-numbers[i-1] == 1 {
			jolt1++
		}
		if n-numbers[i-1] == 3 {
			jolt3++
		}
	}
	return jolt1 * jolt3
}

func parents(numbers []int) map[int][]int {
	res := make(map[int][]int)
	maxIndex := len(numbers) - 1
	for i := range numbers {
		revI := maxIndex - i
		n := numbers[revI]
		j := revI - 1
		res[n] = make([]int, 0)
		for j >= 0 {
			if n-numbers[j] > 3 {
				break
			}
			res[n] = append(res[n], numbers[j])
			j--
		}
	}
	return res
}

// Step2 solves step 2
func Step2(numbers []int) int {
	defer timeTrack(time.Now(), "Step 2")
	p := parents(numbers)
	q := map[int]int{0: 1}
	for _, n := range numbers[1:] {
		q[n] = 0
		for _, m := range p[n] {
			q[n] += q[m]
		}
	}
	return q[numbers[len(numbers)-1]]
}
