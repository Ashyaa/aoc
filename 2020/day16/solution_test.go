package day16_test

import (
	"aoc/2020/day16"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day16.ReadInput()
	a.Equal("", day16.Step1(input), "step 1")
	a.Equal("", day16.Step2(input), "step 2")
}
