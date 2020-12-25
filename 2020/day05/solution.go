package day05

import (
	"io/ioutil"
	"sort"
	"strings"
)

var input = "./input.txt"

// ReadInput retrieves the content of the input file
func ReadInput() []string {
	data, _ := ioutil.ReadFile(input)
	return strings.Split(string(data), "\r\n")
}

func readBinary(raw string) (res int) {
	for _, c := range raw {
		bit := 0
		if c == 'B' || c == 'R' {
			bit = 1
		}
		res <<= 1
		res |= bit
	}
	return
}

// seatIDs for the list of boarding passes
func seatIDs(input []string) (res []int) {
	for _, raw := range input {
		res = append(res, readBinary(raw[:7])*8+readBinary(raw[7:]))
	}
	sort.Ints(res)
	return
}

// Step1 solves step 1
func Step1(input []string) int {
	ids := seatIDs(input)
	return ids[len(ids)-1]
}

// Step2 solves step 2
func Step2(input []string) int {
	ids := seatIDs(input)
	for i, id := range ids {
		if i == len(ids)-1 {
			break
		}
		if id+2 == ids[i+1] {
			return id + 1
		}
	}
	return -1
}
