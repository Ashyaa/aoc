package day07_test

import (
	"aoc/2020/day07"
	"testing"

	A "github.com/stretchr/testify/assert"
)

func TestDay(t *testing.T) {
	a := A.New(t)
	input := day07.ReadInput()
	a.Equal(119, day07.Step1(input))
	a.Equal(155802, day07.Step2(input))
}
