package day05_test

import (
	"aoc/2020/day05"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day05.ReadInput()
	a.Equal(913, day05.Step1(input))
	a.Equal(717, day05.Step2(input))
}
