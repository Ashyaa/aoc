package day06

import (
	"io/ioutil"
	"strings"
)

var input = "./input.txt"

// ReadInput retrieves the content of the input file
func ReadInput() []string {
	data, _ := ioutil.ReadFile(input)
	return strings.Split(string(data), "\r\n\r\n")
}

func containMap(s string) map[rune]bool {
	res := make(map[rune]bool)
	for _, char := range s {
		res[char] = true
	}
	return res
}

// Step1 solves step 1
func Step1(surveys []string) (res int) {
	for _, survey := range surveys {
		res += len(containMap(strings.ReplaceAll(survey, "\r\n", "")))
	}
	return
}

// Step2 solves step 2
func Step2(surveys []string) (res int) {
	for _, survey := range surveys {
		merged := strings.Join(strings.Split(survey, "\r\n"), "")
		maps := make([]map[rune]bool, 0)
		for _, entry := range strings.Split(survey, "\r\n") {
			maps = append(maps, containMap(entry))
		}
		votes := ""
		checked := make(map[rune]bool)
		for _, char := range merged {
			if _, ok := checked[char]; ok {
				continue
			}
			intersection := true
			for _, charMap := range maps {
				if _, ok := charMap[char]; !ok {
					intersection = false
					break
				}
			}
			if intersection {
				votes += string(char)
			}
			checked[char] = true
		}
		res += len(votes)
	}
	return
}
