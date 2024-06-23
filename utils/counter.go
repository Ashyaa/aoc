package utils

type Counter[T comparable] map[T]int

func NewCounter[T comparable]() Counter[T] {
	return make(Counter[T])
}

func (c Counter[T]) Add(items ...T) {
	for _, item := range items {
		if _, ok := c[item]; !ok {
			c[item] = 1
		} else {
			c[item]++
		}
	}
}

func (c Counter[T]) Count(item T) int {
	count, ok := c[item]
	if !ok {
		return 0
	}
	return count
}

func (c Counter[T]) Len() int {
	return len(c)
}

func (c Counter[T]) Total() int {
	return SumMap(c)
}

func (c Counter[T]) Clear() {
	clear(c)
}
