package utils

import "fmt"

// NeighbourFunc describes a function returning the list of neighbours of point
// (i, j), in the form of a slice of arrays of 2 ints, each representing a neighbour
// coordinate.
type NeighbourFunc func(i int, j int) [][2]int

// CardinalNeighbours is the default neighbour function. It returns, in order:
// (i-1,j), (i,j+1), (i+1,j), (i,j-1).
func CardinalNeighbours(i, j int) [][2]int {
	return [][2]int{
		{i - 1, j},
		{i, j + 1},
		{i + 1, j},
		{i, j - 1},
	}
}

// Element is a convenience struct to describe an element in matrix with its coordinates.
type Element[T any] struct {
	X, Y  int
	Value T
}

// A Matrix a 2 dimension array, along with convenience methods to manipulate is easier.
type Matrix[T any] struct {
	arr           [][]T
	getNeighbours NeighbourFunc
}

// NewMatrix creates a new Matrix of type T from a slice of slices of T.
func NewMatrix[T any](in [][]T) Matrix[T] {
	return Matrix[T]{arr: in, getNeighbours: CardinalNeighbours}
}

// NewMatrixFromSlice creates a new Matrix of type T from a slice of T. The number of
// lines is induced from the provided line length. If the slice is not a multple of
// lineLength, the last row of the matrix is padded with the zero-valuue of type T.
func NewMatrixFromSlice[T any](in []T, lineLength int) Matrix[T] {
	res := Matrix[T]{
		getNeighbours: CardinalNeighbours,
	}
	size := len(in)
	q, r := size/lineLength, size%lineLength
	if r != 0 {
		q++
	}
	for i := 0; i < q; i++ {
		tmp := append([]T{}, in[i*lineLength:min((i+1)*lineLength, size)]...)
		for len(tmp) < lineLength {
			var zeroValue T
			tmp = append(tmp, zeroValue)
		}
		res.arr = append(res.arr, tmp)
	}
	return res
}

// Lines returns the number of lines in the matrix.
func (m Matrix[T]) Lines() int {
	return len(m.arr)
}

// Columns returns the number of lines in the matrix.
func (m Matrix[T]) Columns() int {
	return len(m.arr[0])
}

// Assert that x is a valid x-coordinate.
func (m Matrix[T]) assertX(x int) bool {
	return 0 <= x && x < m.Lines()
}

// Assert that y is a valid y-coordinate.
func (m Matrix[T]) assertY(y int) bool {
	return 0 <= y && y < m.Columns()
}

// Assert that (x,y) are valid coordinates.
func (m Matrix[T]) assertCoords(x, y int) bool {
	return m.assertX(x) && m.assertY(y)
}

// Panics if (x,y) aren't valid coordinates.
func (m Matrix[T]) requireCoords(x, y int) {
	msg := "%s=%d out of bounds [0-%d)"
	if !m.assertX(x) {
		panic(fmt.Sprintf(msg, "x", x, m.Lines()))
	}
	if !m.assertY(y) {
		panic(fmt.Sprintf(msg, "y", y, m.Columns()))
	}
}

// At returns the item at coordinates (x,y).
// Panics if either x or y aren't valid coordinates.
func (m Matrix[T]) At(x, y int) T {
	m.requireCoords(x, y)
	return m.arr[x][y]
}

// Set updates the value at coordinates (x,y).
// Panics if either x or y aren't valid coordinates.
func (m *Matrix[T]) Set(x, y int, value T) {
	m.requireCoords(x, y)
	(*m).arr[x][y] = value
}

// SetNeighboursFunc uupdates the function generating neighbour coordinates.
func (m *Matrix[T]) SetNeighboursFunc(fn NeighbourFunc) {
	(*m).getNeighbours = fn
}

// Neighbours generates the list of neighbours from position (x,y) using the
// currently set neighbour function. Any neighbour coordinates that would be out
// of the matrix are safely skipped.
//
//	m := NewMatrix([][]int{
//		{1, 2, 3},
//		{4, 5, 6},
//		{7, 8, 9},
//	})
//	m.Neighbours(1,1) == []Element[int]{
//		{0, 1, 2},
//		{1, 2, 6},
//		{2, 1, 8},
//		{1, 0, 4},
//	}
//
//	m.Neighbours(0,0) == []Element[int]{
//		{0, 1, 2},
//		{1, 0, 4},
//	}
//
func (m *Matrix[T]) Neighbours(x, y int) (res []Element[T]) {
	m.requireCoords(x, y)
	for _, coords := range m.getNeighbours(x, y) {
		if m.assertCoords(coords[0], coords[1]) {
			res = append(res, Element[T]{
				X:     coords[0],
				Y:     coords[1],
				Value: m.arr[coords[0]][coords[1]],
			})
		}
	}
	return
}
