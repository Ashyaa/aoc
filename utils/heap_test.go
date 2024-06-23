package utils

import (
	"testing"

	R "github.com/stretchr/testify/require"
)

type foobar struct {
	name  string
	value int
	valid bool
}

var (
	items = []foobar{
		{
			name:  "foo",
			value: 45,
			valid: true,
		},
		{
			name:  "bar",
			value: -5,
			valid: false,
		},
	}
)

func TestNewPriorityQueue(t *testing.T) {
	r := R.New(t)
	p := NewPriorityQueue[foobar]()
	r.Len((*p.q).data, 0)

	p = NewPriorityQueue[foobar](items...)
	r.Len((*p.q).data, 2)
	for i, it := range items {
		got := (*p.q).data[i]
		r.Equal(it, got.value)
		r.Equal(1, got.priority)
	}
}

func TestPriorityQueuePushPop(t *testing.T) {
	r := R.New(t)
	ref := foobar{"fooboo", 55, true}
	p := NewPriorityQueue[foobar](items...)
	p.Push(ref, -1)
	r.Equal(3, p.Len())
	got := ((*p.q).data)[0]
	r.Equal(ref, got.value)
	r.Equal(-1, got.priority)
	r.Equal(0, got.index)
	elem := p.Pop()
	r.Equal(2, p.Len())
	r.Equal(ref, elem)
}

func TestPriorityReverseOrder(t *testing.T) {
	r := R.New(t)
	ref := foobar{"fooboo", 55, true}
	p := NewPriorityQueue[foobar](items...)
	p.Push(ref, ref.value)
	r.Equal(3, p.Len())
	p.SetOrder(false)
	got := ((*p.q).data)[0]
	r.Equal(ref, got.value)
	r.Equal(ref.value, got.priority)
	r.Equal(0, got.index)
	elem := p.Pop()
	r.Equal(2, p.Len())
	r.Equal(ref, elem)
}
