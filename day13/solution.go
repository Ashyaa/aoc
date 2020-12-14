package day13

import (
	"io/ioutil"
	"log"
	"math"
	"strconv"
	"strings"
	"time"
)

var input = "./input.txt"

// Bus represenation
type Bus struct {
	ID, index int
}

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}

// ReadInput retrieves the content of the input file
func ReadInput() (est int, times []Bus) {
	data, _ := ioutil.ReadFile(input)
	lines := strings.Split(string(data), "\n")
	est, _ = strconv.Atoi(lines[0])
	for index, s := range strings.Split(lines[1], ",") {
		if s == "x" {
			continue
		}
		t, _ := strconv.Atoi(s)
		times = append(times, Bus{t, index})
	}
	return
}

// Step1 solves step 1
func Step1(est int, buses []Bus) int {
	defer timeTrack(time.Now(), "Step 1")
	estF := float64(est)
	t0 := float64(buses[0].ID)
	min, ID := math.Ceil(estF/t0)*t0, buses[0].ID
	for _, b := range buses[1:] {
		t := float64(b.ID)
		r := math.Ceil(estF/t) * t
		if r < min {
			min, ID = r, b.ID
		}
	}
	return (int(min) % est) * ID
}

func extendedEuclidian(a, b int) (int, int) {
	if a == 0 {
		return 0, 1
	}
	u1, v1 := extendedEuclidian(b%a, a)
	return v1 - (b/a)*u1, u1
}

func abs(n int) int {
	y := n >> 63
	return (n ^ y) - y
}

// Step2 solves step 2
func Step2(buses []Bus) int {
	defer timeTrack(time.Now(), "Step 2")
	n := 1
	for _, b := range buses {
		b.index = -b.index % b.ID
		n *= b.ID
	}
	res := 0
	for _, b := range buses {
		m := n / b.ID
		_, v := extendedEuclidian(b.ID, m)
		res += v * m * b.index
	}
	return abs(res % n)
}
