package day07

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	typeFioaK = iota
	typeFooaK
	typeFH
	typeToaK
	type2P
	type1P
	typeHC
	typeCount

	inputFile   = "./input.txt"
	exampleFile = "./example.txt"
)

var (
	values = map[rune]int{
		'2': 2,
		'3': 3,
		'4': 4,
		'5': 5,
		'6': 6,
		'7': 7,
		'8': 8,
		'9': 9,
		'T': 10,
		'J': 11,
		'Q': 12,
		'K': 13,
		'A': 14,
	}
)

func getType(count map[rune]int) int {
	switch len(count) {
	case 1:
		return typeFioaK
	case 2:
		for _, v := range count {
			switch v {
			case 2, 3:
				return typeFH
			default:
				return typeFooaK
			}
		}
		return typeFooaK
	case 3:
		for _, v := range count {
			switch v {
			case 2:
				return type2P
			case 3:
				return typeToaK
			}
		}
		return typeFooaK
	case 4:
		return type1P
	case 5:
		return typeHC
	}
	panic("impossible")
}

func getTypeP2(count map[rune]int) int {
	ogType := getType(count)
	nbJokers, ok := count['J']
	if !ok {
		return ogType
	}
	switch ogType {
	case typeFioaK, typeFooaK, typeFH:
		return typeFioaK
	case typeToaK:
		return typeFooaK
	case type2P:
		if nbJokers == 2 {
			return typeFooaK
		}
		return typeFH
	case type1P:
		return typeToaK
	case typeHC:
		return type1P
	}
	panic("impossible")
}

func splitByType(types []int) (res [][]int) {
	res = make([][]int, typeCount)
	for i := 0; i < typeCount; i++ {
		res[i] = make([]int, 0)
	}
	for i, typ := range types {
		res[typ] = append(res[typ], i)
	}
	return res
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (hands [][]int, types []int, types2 []int, bids []int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		line := sc.Text()
		hand := []int{}
		count := make(map[rune]int)
		for idx, r := range line {
			if idx == 5 {
				break
			}
			count[r] += 1
			hand = append(hand, values[r])
		}
		hands = append(hands, hand)
		bid, _ := strconv.Atoi(line[6:])
		types = append(types, getType(count))
		types2 = append(types2, getTypeP2(count))
		bids = append(bids, bid)
	}
	return
}

func order(x, y []int, p2 bool) int {
	for i := 0; i < 5; i++ {
		if res := cmp(x[i], y[i], p2); res != 0 {
			return res
		}
	}
	panic("impossible")
}

func cmp(a, b int, p2 bool) int {
	if p2 {
		if a == values['J'] {
			a = -1
		}
		if b == values['J'] {
			b = -1
		}
	}
	if a > b {
		return -1
	}
	if a < b {
		return 1
	}
	return 0
}

func Solve(hands [][]int, types, bids []int, p2 bool) int {
	res := 0
	rank := len(bids)
	for _, arr := range splitByType(types) {
		slices.SortFunc(arr, func(i, j int) int {
			return order(hands[i], hands[j], p2)
		})
		for _, idx := range arr {
			res += rank * bids[idx]
			rank -= 1
		}
	}
	return res
}

func TestDay07(t *testing.T) {
	r := R.New(t)
	exHands, exTypes, exTypesP2, exBids := ReadInput(exampleFile)
	hands, types, typesP2, bids := ReadInput(inputFile)
	r.Equal(6440, Solve(exHands, exTypes, exBids, false), "example p1")
	r.Equal(247961593, Solve(hands, types, bids, false), "input p1")
	r.Equal(5905, Solve(exHands, exTypesP2, exBids, true), "example p2")
	r.Equal(248750699, Solve(hands, typesP2, bids, true), "input p2")
}

func BenchmarkDay07(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		hands, types, typesP2, bids := ReadInput(inputFile)
		Solve(hands, types, bids, false)
		Solve(hands, typesP2, bids, true)
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
