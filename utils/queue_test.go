package utils

import (
	"testing"

	R "github.com/stretchr/testify/require"
)

func TestNewQueue(t *testing.T) {
	r := R.New(t)
	r.Equal(Queue[int]{1, 2, 3}, NewQueue(1, 2, 3))
}

func TestQueuePush(t *testing.T) {
	r := R.New(t)
	s := NewQueue(1, 2, 3)
	s.Push(4, 5, 6)
	r.Equal(Queue[int]{1, 2, 3, 4, 5, 6}, s)
}

func TestQueueLen(t *testing.T) {
	r := R.New(t)
	s := NewQueue(1, 2, 3)
	r.Equal(len(s), s.Len())
}

func TestQueueIsEmpty(t *testing.T) {
	r := R.New(t)
	r.True(NewQueue[string]().IsEmpty())
	r.False(NewQueue[string]("lorem", "ipsum").IsEmpty())
}

func TestQueuePop(t *testing.T) {
	t.Run("nominal case 1", func(t *testing.T) {
		r := R.New(t)
		s := NewQueue(1, 2, 3)
		item := s.Pop()
		r.Equal(1, item)
		r.Equal(NewQueue(2, 3), s)
	})
	t.Run("panics if Queue is empty", func(t *testing.T) {
		r := R.New(t)
		r.Panics(func() {
			s := NewQueue[int]()
			s.Pop()
		})
	})
}

func TestQueuePeek(t *testing.T) {
	t.Run("nominal case", func(t *testing.T) {
		r := R.New(t)
		s := NewQueue(1, 2, 3)
		item := s.Peek()
		r.Equal(1, item)
		r.Equal(NewQueue(1, 2, 3), s)
	})
	t.Run("panics if Queue is empty", func(t *testing.T) {
		r := R.New(t)
		r.Panics(func() {
			s := NewQueue[int]()
			s.Peek()
		})
	})
}
