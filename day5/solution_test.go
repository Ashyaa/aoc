package day5_test

import (
	"aoc/day5"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day5.ReadInput()
	a.Equal(913, day5.Step1(input))
	a.Equal(717, day5.Step2(input))
}
