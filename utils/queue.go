package utils

// A Queue is a container where items are managed usiing FIFO (First In First Out) logic.
type Queue[T any] []T

// NewQueue creates a new queue of given type. Passed items are pushed to the queue in order.
// NewQueue(1,2,3) = Queue{1,2,3}, where 1 is the head of the queue.
func NewQueue[T comparable](init ...T) Queue[T] {
	return append(Queue[T]{}, init...)
}

// Push adds items to the queue. Passed items are pushed to the queue in order.
// NewQueue(1,2,3).Push(4,5,6) == Queue{1,2,3,4,5,6}, where 1 is the head of the queue.
func (s *Queue[T]) Push(items ...T) {
	*s = append(*s, items...)
}

// Len returns the number of elements currently in the queue.
func (s Queue[T]) Len() int {
	return len(s)
}

// IsEmpty returns true if the queue has no elements.
func (s Queue[T]) IsEmpty() bool {
	return s.Len() == 0
}

// Pop takes the element at the top of the queue, removes it from the queue and returns it.
// Panics if the queue is empty.
func (s *Queue[T]) Pop() T {
	if s.Len() == 0 {
		panic("empty queue")
	}
	res := (*s)[0]
	*s = (*s)[1:]
	return res
}

// Peek returns the element at the top of the stack without removing it from the stack.
// Panics if the stack is empty.
func (s *Queue[T]) Peek() T {
	if s.Len() == 0 {
		panic("empty queue")
	}
	return (*s)[0]
}
