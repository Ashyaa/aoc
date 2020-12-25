package day08_test

import (
	"aoc/2020/day08"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day08.ReadInput()
	a.Equal(1749, day08.Step1(input))
	a.Equal(515, day08.Step2(input))
}
