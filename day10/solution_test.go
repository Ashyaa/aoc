package day10_test

import (
	"aoc/day10"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day10.ReadInput()
	a.Equal(2380, day10.Step1(input), "step 1")
	a.Equal(48358655787008, day10.Step2(input), "step 2")
}
