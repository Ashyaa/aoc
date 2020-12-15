package day15

import (
	"io/ioutil"
	"log"
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
	for _, n := range strings.Split(string(data), ",") {
		val, _ := strconv.Atoi(n)
		res = append(res, val)
	}
	return
}

func play(numbers []int, maxTurn int) int {
	game := make(map[int]int)
	for index, n := range numbers {
		game[n] = index
	}
	lastSaid := numbers[len(numbers)-1]
	for turn := len(numbers) - 1; turn < maxTurn-1; turn++ {
		v := 0
		if n, ok := game[lastSaid]; ok {
			v = turn - n
		}
		game[lastSaid] = turn
		lastSaid = v
	}
	return lastSaid
}

// Step1 solves step 1
func Step1(numbers []int) int {
	defer timeTrack(time.Now(), "Step 1")
	return play(numbers, 2020)
}

// Step2 solves step 2
func Step2(numbers []int) int {
	defer timeTrack(time.Now(), "Step 2")
	return play(numbers, 30000000)
}
