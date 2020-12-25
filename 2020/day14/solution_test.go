package day14_test

import (
	"aoc/2020/day14"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day14.ReadInput()
	a.Equal(17765746710228, day14.Step1(input), "step 1")
	a.Equal(4401465949086, day14.Step2(input), "step 2")
}
