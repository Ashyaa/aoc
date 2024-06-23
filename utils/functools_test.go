package utils

import (
	"strconv"
	"testing"

	R "github.com/stretchr/testify/require"
)

func TestFilter(t *testing.T) {
	r := R.New(t)
	r.Equal([]int{2, 4}, Filter([]int{1, 2, 3, 4}, func(a int) bool { return a%2 == 0 }))
}

func TestReduce(t *testing.T) {
	r := R.New(t)
	r.Equal(10, Reduce([]int{1, 2, 3, 4}, nil, func(a, b int) int { return a + b }))
	base := 2
	r.Equal(120, Reduce([]int{3, 4, 5}, &base, func(a, b int) int { return a * b }))
}

func TestMap(t *testing.T) {
	r := R.New(t)
	in := []int{1, 2, 3, 4}
	r.Equal([]string{"1", "2", "3", "4"}, Map(in, strconv.Itoa))
	addX := func(x int) func(int) int { return func(a int) int { return a + x } }
	r.Equal([]int{11, 12, 13, 14}, Map(in, addX(10)))
}

func TestVectorize(t *testing.T) {
	r := R.New(t)
	in := []int{1, 2, 3, 4}
	f := Vectorize(strconv.Itoa)
	r.Equal([]string{"1", "2", "3", "4"}, f(in))
}

func TestAny(t *testing.T) {
	r := R.New(t)
	in := []string{"lorem", "ipsum", "dolor", "sit", "amet"}
	r.True(
		Any(in, func(item string) bool { return len(item) == 3 }),
		"one match",
	)
	r.True(
		Any(in, func(item string) bool { return len(item) == 5 }),
		"several matches",
	)
	r.False(
		Any(in, func(item string) bool { return len(item) > 10 }),
		"no matches",
	)
}

func TestAll(t *testing.T) {
	r := R.New(t)
	r.True(
		All([]float64{3.14, 1.147964, 2.685e10}, func(x float64) bool { return x != 0 }),
		"all matches",
	)
	r.False(
		All([]float64{0.0, -5, 895.2547485, 1e-38}, func(x float64) bool { return x < 0 }),
		"one doesn't match",
	)
}

func TestOne(t *testing.T) {
	r := R.New(t)
	in := []string{"lorem", "ipsum", "dolor", "sit", "amet"}
	r.True(
		One(in, func(item string) bool { return item == "amet" }),
		"one match",
	)
	r.False(
		One(in, func(item string) bool { return item == "foobar" }),
		"no match",
	)
	r.False(
		One(in, func(item string) bool { return len(item) == 5 }),
		"several matches",
	)
}

func TestNext(t *testing.T) {
	r := R.New(t)
	in := []int{2, 4, 6, 8, 10, 12}
	r.Equal(1, Next(in, 0, func(item int) bool { return item%4 == 0 }))
	r.Equal(5, Next(in, 3, func(item int) bool { return item%3 == 0 }))
	r.Equal(-1, Next(in, -1, func(item int) bool { return item%11 == 0 }))
}

func TestSumSlice(t *testing.T) {
	r := R.New(t)
	in := []int{1, 2, 4, 8}
	r.Equal(15, SumSlice(in))
}

func TestSumMap(t *testing.T) {
	r := R.New(t)
	in := map[string]float64{
		"one":   1,
		"two":   2,
		"four":  4,
		"eight": 8,
	}
	r.Equal(15., SumMap(in))
}
