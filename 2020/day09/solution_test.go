package day09_test

import (
	"aoc/2020/day09"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day09.ReadInput()
	res := day09.Step1(input)
	a.Equal(uint64(14360655), res, "step 1")
	a.Equal(uint64(1962331), day09.Step2(input, res), "step 2")
}
