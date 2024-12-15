package utils

import (
	"strconv"
	"strings"
)

var (
	Directions = []Coord{
		{X: -1, Y: 0},
		{X: 0, Y: 1},
		{X: 1, Y: 0},
		{X: 0, Y: -1},
	}
)

// ToInt is an error-free strconv.Atoi
func ToInt(s string) int {
	res, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return res
}

func ToCoords(s, sep string) (res Coord) {
	ints := Map(strings.Split(s, sep), ToInt)
	res.X = ints[0]
	res.Y = ints[1]
	if len(ints) > 2 {
		res.Z = ints[2]
	}
	return
}

type Coord struct {
	X, Y, Z int
}
