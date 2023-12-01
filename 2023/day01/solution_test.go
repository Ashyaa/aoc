package day01

import (
	"os"
	"strconv"
	"strings"
	"testing"
	"unicode"

	R "github.com/stretchr/testify/require"
)

const (
	inputFile    = "./input.txt"
	exampleFile  = "./example.txt"
	exampleFile2 = "./example2.txt"
)

var (
	digits = []string{
		"one",
		"two",
		"three",
		"four",
		"five",
		"six",
		"seven",
		"eight",
		"nine",
	}
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) []string {
	data, _ := os.ReadFile(filepath)
	return strings.Split(string(data), "\n")
}

func First(lines []string) int {
	res := 0
	for _, line := range lines {
		tmp := []rune{0, 0}
		runes := []rune(line)
		nbChars := len(runes)
		for i := range runes {
			if tmp[0] == 0 && unicode.IsDigit(runes[i]) {
				tmp[0] = runes[i]
			}
			if tmp[1] == 0 && unicode.IsDigit(runes[nbChars-i-1]) {
				tmp[1] = runes[nbChars-i-1]
			}
			if tmp[0] != 0 && tmp[1] != 0 {
				break
			}
		}
		number, _ := strconv.Atoi(string(tmp))
		res += number
	}
	return res
}

func hasDigit(s string, end bool) int {
	f := strings.HasPrefix
	if end {
		f = strings.HasSuffix
	}
	for idx, digit := range digits {
		if f(s, digit) {
			return idx + 1
		}
	}
	return -1
}

func findDigit(runes, tmp []rune, i int, end bool) []rune {
	var idx, resIdx int
	var subStr string
	if end {
		idx = len(runes) - i - 1
		resIdx = 1
		subStr = string(runes[:len(runes)-i])
	} else {
		idx = i
		resIdx = 0
		subStr = string(runes[i:])
	}
	digit := hasDigit(subStr, end)
	if digit > 0 {
		str := strconv.Itoa(digit)
		tmp[resIdx] = []rune(str)[0]
	} else if unicode.IsDigit(runes[idx]) {
		tmp[resIdx] = runes[idx]
	}
	return tmp
}

func Second(lines []string) interface{} {
	res := 0
	for _, line := range lines {
		tmp := []rune{0, 0}
		runes := []rune(line)
		for i := range runes {
			if tmp[0] == 0 {
				tmp = findDigit(runes, tmp, i, false)
			}
			if tmp[1] == 0 {
				tmp = findDigit(runes, tmp, i, true)
			}
			if tmp[0] != 0 && tmp[1] != 0 {
				break
			}
		}
		number, _ := strconv.Atoi(string(tmp))
		res += number
	}
	return res
}

func TestDay(t *testing.T) {
	r := R.New(t)
	example := ReadInput(exampleFile)
	example2 := ReadInput(exampleFile2)
	input := ReadInput(inputFile)
	r.Equal(142, First(example))
	r.Equal(54667, First(input))
	r.Equal(281, Second(example2))
	r.Equal(54203, Second(input))
}

func BenchmarkDay(b *testing.B) {
	b.Run("day", func(b *testing.B) {
		input := ReadInput(inputFile)
		First(input)
		Second(input)
	})
}
