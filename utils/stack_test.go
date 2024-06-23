package utils

import (
	"testing"

	R "github.com/stretchr/testify/require"
)

func TestNewStackReverse(t *testing.T) {
	r := R.New(t)
	r.Equal(Stack[int]{3, 2, 1}, NewStack(1, 2, 3))
}

func TestNewStack(t *testing.T) {
	r := R.New(t)
	r.Equal(Stack[int]{1, 2, 3}, NewStackReverse(1, 2, 3))
}

func TestStackPushReverse(t *testing.T) {
	r := R.New(t)
	s := NewStackReverse(1, 2, 3)
	s.Push(4, 5, 6)
	r.Equal(NewStackReverse(6, 5, 4, 1, 2, 3), s)
}

func TestStackPush(t *testing.T) {
	r := R.New(t)
	s := NewStackReverse(1, 2, 3)
	s.PushReverse(4, 5, 6)
	r.Equal(Stack[int]{4, 5, 6, 1, 2, 3}, s)
}

func TestStackLen(t *testing.T) {
	r := R.New(t)
	s := NewStack(1, 2, 3)
	r.Equal(len(s), s.Len())
}

func TestStackIsEmpty(t *testing.T) {
	r := R.New(t)
	r.True(NewStack[string]().IsEmpty())
	r.False(NewStack[string]("lorem", "ipsum").IsEmpty())
}

func TestStackPop(t *testing.T) {
	t.Run("nominal case 1", func(t *testing.T) {
		r := R.New(t)
		s := NewStack(1, 2, 3)
		item := s.Pop()
		r.Equal(3, item)
		r.Equal(NewStack(1, 2), s)
	})
	t.Run("nominal case 2", func(t *testing.T) {
		r := R.New(t)
		s := NewStackReverse(1, 2, 3)
		item := s.Pop()
		r.Equal(1, item)
		r.Equal(NewStackReverse(2, 3), s)
	})
	t.Run("panics if stack is empty", func(t *testing.T) {
		r := R.New(t)
		r.Panics(func() {
			s := NewStack[int]()
			s.Pop()
		})
	})
}

func TestStackPeek(t *testing.T) {
	t.Run("nominal case 1", func(t *testing.T) {
		r := R.New(t)
		s := NewStack(1, 2, 3)
		item := s.Peek()
		r.Equal(3, item)
		r.Equal(NewStack(1, 2, 3), s)
	})
	t.Run("nominal case 2", func(t *testing.T) {
		r := R.New(t)
		s := NewStackReverse(1, 2, 3)
		item := s.Peek()
		r.Equal(1, item)
		r.Equal(NewStackReverse(1, 2, 3), s)
	})
	t.Run("panics if stack is empty", func(t *testing.T) {
		r := R.New(t)
		r.Panics(func() {
			s := NewStack[int]()
			s.Peek()
		})
	})
}
