package day9_test

import (
	"aoc/day9"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day9.ReadInput()
	res := day9.Step1(input)
	a.Equal(uint64(14360655), res, "step 1")
	a.Equal(uint64(1962331), day9.Step2(input, res), "step 2")
}
