package day16

import (
	"io/ioutil"
	"log"
	"time"
)

var input = "./input.txt"

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}

// ReadInput retrieves the content of the input file
func ReadInput() string {
	data, _ := ioutil.ReadFile(input)
	return string(data)
}

// Step1 solves step 1
func Step1() {
	defer timeTrack(time.Now(), "Step 1")
}

// Step2 solves step 2
func Step2() {
	defer timeTrack(time.Now(), "Step 2")
}
