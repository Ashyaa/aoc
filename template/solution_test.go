package template_test

import "testing"

func TestDay(t *testing.T) {
	a := A.New(t)
	input := dayXX.ReadInput()
	a.Equal("", dayXX.Step1(input))
	a.Equal("", dayXX.Step2(input))
}
