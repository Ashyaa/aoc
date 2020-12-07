package day7_test

import (
	"aoc/day7"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day7.ReadInput()
	a.Equal(119, day7.Step1(input))
	a.Equal(155802, day7.Step2(input))
}
