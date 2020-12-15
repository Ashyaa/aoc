package day15_test

import (
	"aoc/day15"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day15.ReadInput()
	a.Equal(257, day15.Step1(input), "step 1")
	a.Equal(8546398, day15.Step2(input), "step 2")
}
