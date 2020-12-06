package day6_test

import (
	"aoc/day6"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day6.ReadInput()
	a.Equal(7027, day6.Step1(input))
	a.Equal(3579, day6.Step2(input))
}
