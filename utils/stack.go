package utils

// A Stack is a container where items are managed usiing LIFO (Last In First Out) logic.
type Stack[T any] []T

// Returns a reversed copy of arr.
func reversed[T any](arr []T) []T {
	res := append([]T{}, arr...)
	for i := len(res)/2 - 1; i >= 0; i-- {
		opp := len(res) - 1 - i
		res[i], res[opp] = res[opp], res[i]
	}
	return res
}

// NewStack creates a new stack of given type. Passed items are pushed to the stack in order.
// NewStack(1,2,3) = Stack{3,2,1}, where 3 is the top of the stack.
func NewStack[T comparable](init ...T) Stack[T] {
	return append(Stack[T]{}, reversed(init)...)
}

// NewStackReverse creates a new stack of given type. Passed items are pushed to the stack in reverse order.
// NewStackReverse(1,2,3) = Stack{1,2,3}, where 1 is the top of the stack.
func NewStackReverse[T comparable](init ...T) Stack[T] {
	return append(Stack[T]{}, init...)
}

// Push adds items to the stack. Passed items are pushed to the stack in order.
// NewStack(1,2,3).Push(4,5,6) == Stack{6,5,4,1,2,3}, where 6 is the top of the stack.
func (s *Stack[T]) Push(items ...T) {
	*s = append(reversed(items), *s...)
}

// PushReverse adds items to the stack. Passed items are pushed to the stack in reverse order.
// NewStack(1,2,3).PushReverse(4,5,6) == Stack{4,5,6,1,2,3}, where 1 is the top of the stack.
func (s *Stack[T]) PushReverse(items ...T) {
	*s = append(items, *s...)
}

// Len returns the number of elements currently in the stack.
func (s Stack[T]) Len() int {
	return len(s)
}

// IsEmpty returns true if the stack has no elements.
func (s Stack[T]) IsEmpty() bool {
	return s.Len() == 0
}

// Pop takes the element at the top of the stack, removes it from the stack and returns it.
// Panics if the stack is empty.
func (s *Stack[T]) Pop() T {
	if s.Len() == 0 {
		panic("empty stack")
	}
	res := (*s)[0]
	*s = (*s)[1:]
	return res
}

// Peek returns the element at the top of the stack without removing it from the stack.
// Panics if the stack is empty.
func (s *Stack[T]) Peek() T {
	if s.Len() == 0 {
		panic("empty stack")
	}
	return (*s)[0]
}
