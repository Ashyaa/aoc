package day14

import (
	"fmt"
	"io/ioutil"
	"log"
	sc "strconv"
	st "strings"
	"time"
)

type memory map[uint64]uint64

func (m memory) sum() (res uint64) {
	for _, v := range m {
		res += v
	}
	return
}

// Line of the input
type Line struct {
	addr, value uint64
	mask        string
}

var input = "./input.txt"

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}

// ReadInput retrieves the content of the input file
func ReadInput() (res []Line) {
	data, _ := ioutil.ReadFile(input)
	s := st.TrimRight(st.ReplaceAll(string(data), " ", ""), "\n")
	for _, l := range st.Split(s, "\n") {
		if st.HasPrefix(l, "mask") {
			res = append(res, Line{mask: l[5:]})
			continue
		}
		words := st.Split(l, "=")
		addr, _ := sc.ParseUint(words[0][4:len(words[0])-1], 10, 36)
		val, _ := sc.ParseUint(words[1], 10, 36)
		res = append(res, Line{addr, val, ""})
	}
	return
}

func getMasks(s string) (uint64, uint64) {
	mask0, _ := sc.ParseUint(st.ReplaceAll(s, "X", "1"), 2, 36)
	mask1, _ := sc.ParseUint(st.ReplaceAll(s, "X", "0"), 2, 36)
	return mask0, mask1
}

// Step1 solves step 1
func Step1(lines []Line) int {
	defer timeTrack(time.Now(), "Step 1")
	m0, m1, mem := uint64(0), uint64(0), make(memory)
	for _, l := range lines {
		if l.mask != "" {
			m0, m1 = getMasks(l.mask)
			continue
		}
		v := l.value | m1
		mem[l.addr] = v & m0
	}
	return int(mem.sum())
}

func getMasksList(s string) []uint64 {
	if !st.Contains(s, "X") {
		mask, _ := sc.ParseUint(s, 2, 36)
		return []uint64{mask}
	}
	res := append([]uint64{}, getMasksList(st.Replace(s, "X", "1", 1))...)
	res = append(res, getMasksList(st.Replace(s, "X", "0", 1))...)
	return res
}

// Step2 solves step 2
func Step2(lines []Line) int {
	defer timeTrack(time.Now(), "Step 2")
	maskStr, m1, mem := "", uint64(0), make(memory)
	for _, l := range lines {
		if l.mask != "" {
			maskStr = l.mask
			m1, _ = sc.ParseUint(st.ReplaceAll(l.mask, "X", "0"), 2, 36)
			continue
		}
		protoAddr := []rune(fmt.Sprintf("%036b", l.addr|m1))
		for index, c := range maskStr {
			if c == 'X' {
				protoAddr[index] = 'X'
			}
		}
		for _, endAddr := range getMasksList(string(protoAddr)) {
			mem[endAddr] = l.value
		}
	}
	return int(mem.sum())
}
