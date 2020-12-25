package day13_test

import (
	"aoc/2020/day13"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	est, buses := day13.ReadInput()
	a.Equal(4782, day13.Step1(est, buses), "step 1")
	a.Equal(1118684865113056, day13.Step2(buses), "step 2")
}
