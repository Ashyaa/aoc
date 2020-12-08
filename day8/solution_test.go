package day8_test

import (
	"aoc/day8"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day8.ReadInput()
	a.Equal(1749, day8.Step1(input))
	a.Equal(515, day8.Step2(input))
}
