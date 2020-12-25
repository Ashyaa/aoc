package day06_test

import (
	"aoc/2020/day06"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day06.ReadInput()
	a.Equal(7027, day06.Step1(input))
	a.Equal(3579, day06.Step2(input))
}
