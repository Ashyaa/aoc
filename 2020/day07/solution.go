package day07

import (
	"io/ioutil"
	"strconv"
	"strings"
)

const input = "./input.txt"
const myBag = "shiny gold bag"

type item struct {
	quantity int
	bag      string
}

type bag []item

// Rules is a reprensation of the puzzle input
type Rules map[string]bag

func parseBags(raw string) (res bag) {
	if strings.HasPrefix(raw, "no") {
		return
	}
	for _, str := range strings.Split(raw, ", ") {
		elmts := strings.SplitN(str, " ", 2)
		quantity, _ := strconv.Atoi(elmts[0])
		res = append(res, item{
			quantity: quantity,
			bag:      elmts[1],
		})
	}
	return
}

// ReadInput retrieves the content of the input file
func ReadInput() Rules {
	data, _ := ioutil.ReadFile(input)
	tmp := strings.ReplaceAll(string(data), "bags", "bag")
	tmp = strings.ReplaceAll(tmp, ".", "")
	res := make(Rules)
	for _, str := range strings.Split(tmp, "\r\n") {
		elements := strings.Split(str, " contain ")
		res[elements[0]] = parseBags(elements[1])
	}
	return res
}

func contains(bag, wanted string, rules Rules) bool {
	for _, item := range rules[bag] {
		if item.bag == wanted {
			return true
		}
		if contains(item.bag, wanted, rules) {
			return true
		}
	}
	return false
}

// Step1 solves step 1
func Step1(rules Rules) (count int) {
	for bag := range rules {
		if contains(bag, myBag, rules) {
			count++
		}
	}
	return
}

func quantityIn(bag string, rules Rules) int {
	if len(rules[bag]) == 0 {
		return 0
	}
	count := 0
	for _, item := range rules[bag] {
		count += item.quantity + item.quantity*quantityIn(item.bag, rules)
	}
	return count
}

// Step2 solves step 2
func Step2(rules Rules) int {
	return quantityIn(myBag, rules)
}
