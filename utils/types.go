package utils

import "strconv"

// ToInt is an error-free strconv.Atoi
func ToInt(s string) int {
	res, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return res
}

type Coord struct {
	X, Y, Z int
}
