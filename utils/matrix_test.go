package utils

import (
	"testing"

	R "github.com/stretchr/testify/require"
)

func TestNewMatrix(t *testing.T) {
	r := R.New(t)
	in := [][]int{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}
	expected := Matrix[int]{
		arr: [][]int{
			{1, 2, 3},
			{4, 5, 6},
			{7, 8, 9},
		},
	}
	r.Equal(expected.arr, NewMatrix(in).arr)
}

func TestNewMatrixFromSlice(t *testing.T) {
	r := R.New(t)
	in := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	expected := Matrix[int]{
		arr: [][]int{
			{1, 2, 3},
			{4, 5, 6},
			{7, 8, 9},
			{10, 0, 0},
		},
	}
	m := NewMatrixFromSlice(in, 3)
	r.Equal(expected.arr, m.arr)
	r.Equal(4, m.Lines())
	r.Equal(3, m.Columns())
}

func TestMatrixAt(t *testing.T) {
	r := R.New(t)
	m := Matrix[int]{
		arr: [][]int{
			{1, 2, 3},
			{4, 5, 6},
			{7, 8, 9},
			{10, 11, 12},
		},
	}
	r.Equal(8, m.At(2, 1))
	r.PanicsWithValue("x=-1 out of bounds [0-4)", func() {
		m.At(-1, 1)
	}, "x < 0")
	r.PanicsWithValue("x=8 out of bounds [0-4)", func() {
		m.At(8, 2)
	}, "x >= nbLines")
	r.PanicsWithValue("y=-10 out of bounds [0-3)", func() {
		m.At(1, -10)
	}, "y < 0")
	r.PanicsWithValue("y=3 out of bounds [0-3)", func() {
		m.At(2, 3)
	}, "y >= nbColumns")
}

func TestMatrixSet(t *testing.T) {
	r := R.New(t)
	in := []int{1, 2, 3, 4, 5, 6, 7, 8, 9}
	expected := Matrix[int]{
		arr: [][]int{
			{1, 2, 3},
			{4, 5, 6},
			{7, 99, 9},
		},
	}
	m := NewMatrixFromSlice(in, 3)
	m.Set(2, 1, 99)
	r.Equal(expected.arr, m.arr)
	r.PanicsWithValue("x=-1 out of bounds [0-3)", func() {
		m.Set(-1, 1, 0)
	}, "x < 0")
	r.PanicsWithValue("x=8 out of bounds [0-3)", func() {
		m.Set(8, 2, 4)
	}, "x >= nbLines")
	r.PanicsWithValue("y=-10 out of bounds [0-3)", func() {
		m.Set(1, -10, 88)
	}, "y < 0")
	r.PanicsWithValue("y=3 out of bounds [0-3)", func() {
		m.Set(2, 3, 1)
	}, "y >= nbColumns")
}

func TestMatrixNeighbours(t *testing.T) {
	r := R.New(t)
	m := NewMatrix([][]int{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	})
	expected1 := []Element[int]{
		{0, 1, 2},
		{1, 2, 6},
		{2, 1, 8},
		{1, 0, 4},
	}
	r.Equal(expected1, m.Neighbours(1, 1))
	expected2 := []Element[int]{
		{0, 1, 2},
		{1, 0, 4},
	}
	r.Equal(expected2, m.Neighbours(0, 0))
	expected3 := []Element[int]{
		{1, 2, 6},
		{2, 1, 8},
	}
	r.Equal(expected3, m.Neighbours(2, 2))

	m.SetNeighboursFunc(func(i, j int) [][2]int {
		return [][2]int{
			{i, j},
			{i, j + 1},
		}
	})
	expected1 = []Element[int]{
		{1, 1, 5},
		{1, 2, 6},
	}
	r.Equal(expected1, m.Neighbours(1, 1))
	expected2 = []Element[int]{
		{0, 0, 1},
		{0, 1, 2},
	}
	r.Equal(expected2, m.Neighbours(0, 0))
	expected3 = []Element[int]{
		{2, 2, 9},
	}
	r.Equal(expected3, m.Neighbours(2, 2))
}
