package utils

import "golang.org/x/exp/constraints"

// Filter a slice using a given predicate.
//
//	Filter([]int{1, 2, 3, 4}, func(a int) bool { return a%2 == 0 }) == []int{2, 4}
//
func Filter[T any](arr []T, predicate func(item T) bool) []T {
	res := make([]T, 0)
	for _, item := range arr {
		if predicate(item) {
			res = append(res, item)
		}
	}
	return res
}

// Reduce a slice using a given transformation function.
// If init is not nil, it is used as the initial value for the transformation.
//
//	Reduce([]int{1, 2, 3, 4}, nil, func(a, b int) int { return a + b }) == 10
//
//	Reduce([]int{1, 2, 3, 4}, *seven, func(a, b int) int { return a + b }) == 17
//
func Reduce[T any](arr []T, init *T, transform func(a, b T) T) T {
	value, slice := arr[0], arr[1:]
	if init != nil {
		value, slice = *init, arr[0:]
	}
	for _, item := range slice {
		value = transform(value, item)
	}
	return value
}

// Map applies a transformation function to all elements of the slice and returns a slice
// of the transformed elements.
//
//	Map([]int{1, 2, 3, 4}, strconv.Itoa) == []string{"1", "2", "3", "4"}
//
func Map[T any, U any](arr []T, f func(item T) U) []U {
	res := []U{}
	for _, item := range arr {
		res = append(res, f(item))
	}
	return res
}

// Vectorize converts a transformation function on one item to a function that applies
// to a slice of items. In other terms, it is a syntaxic sugar for repeated Map calls.
//
//	f := Vectorize(strconv.Itoa)
//	f([]int{1, 2, 3, 4}) == []string{"1", "2", "3", "4"}
//
func Vectorize[T any, U any](f func(item T) U) func([]T) []U {
	return func(arr []T) []U {
		return Map(arr, f)
	}
}

// Any returns true if at least one item in the slice verifies the predicate.
func Any[T any](arr []T, predicate func(item T) bool) bool {
	for _, item := range arr {
		if predicate(item) {
			return true
		}
	}
	return false
}

// All returns true if all items in the slice verify the predicate.
func All[T any](arr []T, predicate func(item T) bool) bool {
	for _, item := range arr {
		if !predicate(item) {
			return false
		}
	}
	return true
}

// One returns true if exactly one item in the slice verifies the predicate.
func One[T any](arr []T, predicate func(item T) bool) bool {
	count := 0
	for _, item := range arr {
		if predicate(item) {
			count++
		}
		if count > 1 {
			return false
		}
	}
	return count == 1
}

// Next returns the index of the first item that verifies the predicate. If index
// is above 0, the search starts at index `index`. Returns -1 if no item verifies
// the predicate.
func Next[T any](arr []T, index int, predicate func(item T) bool) int {
	start := 0
	if index > 0 {
		start = index
	}
	for i := start; i < len(arr); i++ {
		if predicate(arr[i]) {
			return i
		}
	}
	return -1
}

type Number interface {
	constraints.Float | constraints.Integer
}

// SumSlice returns the sum of a slice of numbers.
func SumSlice[T Number](arr []T) T {
	var res T
	for _, x := range arr {
		res += x
	}
	return res
}

// SumMap returns the sum of all numeric values of a map.
func SumMap[U comparable, T Number](arr map[U]T) T {
	var res T
	for _, x := range arr {
		res += x
	}
	return res
}
