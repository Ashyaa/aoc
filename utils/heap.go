package utils

import "container/heap"

// TODO: Maybe

type HeapItem[T any] struct {
	index, Priority int
	value           T
}

type pQueue[T any] struct {
	increasing bool
	data       []*HeapItem[T]
}

func newPQueue[T any](items ...HeapItem[T]) pQueue[T] {
	res := pQueue[T]{
		data:       make([]*HeapItem[T], 0),
		increasing: true,
	}
	for _, item := range items {
		res.Push(item)
	}

	heap.Init(&res)
	return res
}

func (pq pQueue[T]) Len() int { return len(pq.data) }

func (pq pQueue[T]) Less(i, j int) bool {
	if pq.increasing {
		return pq.data[i].Priority < pq.data[j].Priority
	}
	return pq.data[i].Priority > pq.data[j].Priority
}

func (pq pQueue[T]) Swap(i, j int) {
	pq.data[i], pq.data[j] = pq.data[j], pq.data[i]
	pq.data[i].index = i
	pq.data[j].index = j
}

func (pq *pQueue[T]) Push(x any) {
	n := len((*pq).data)
	it := x.(HeapItem[T])
	it.index = n
	(*pq).data = append((*pq).data, &it)
}

func (pq *pQueue[T]) Pop() any {
	old := (*pq).data
	n := len(old)
	it := old[n-1]
	old[n-1] = nil
	it.index = -1
	(*pq).data = old[0 : n-1]
	return it.value
}

// PriorityQueue encapsulates the typical use of the heap package into a ready-to-use
// structure. See https://pkg.go.dev/container/heap#example-package-PriorityQueue for the code
// it is based on.
// By default, priority is in the natural integer order: a lower value means
// an item has more priority.
type PriorityQueue[T any] struct {
	q *pQueue[T]
}

// NewPriorityQueue creates a PriorityQueue for the wanted type. All items are given
// priority 0.
func NewPriorityQueue[T any](items ...T) PriorityQueue[T] {
	heapItems := Map(items, func(item T) HeapItem[T] {
		return HeapItem[T]{
			Priority: 0,
			value:    item,
		}
	})
	q := newPQueue(heapItems...)
	return PriorityQueue[T]{q: &q}
}

// SetOrder sets the priority order. If false is passed, a higher value means
// a higher priority. If true is passed, a lower value means
// a higher priority.
// The PriorityQueue is then re-sorted with the new order.
func (p *PriorityQueue[T]) SetOrder(increasing bool) {
	p.q.increasing = increasing
	heap.Init(p.q)
}

// Push an item to the queue with given priority.an item has more
func (p *PriorityQueue[T]) Push(x T, priority int) {
	heap.Push(p.q, HeapItem[T]{
		Priority: priority,
		value:    x,
	})
}

// Pop an item from the priority queue.
func (p *PriorityQueue[T]) Pop() T {
	item := heap.Pop(p.q)
	return item.(T)
}

// Len returns the number of items in the priority queue.
func (p *PriorityQueue[T]) Len() int {
	return p.q.Len()
}

// Priority returns the current 'highest' priority, where 'highest' is relative
// to the currently set priority order
func (p *PriorityQueue[T]) Priority() int {
	if p.q.Len() == 0 {
		return 0
	}
	return p.q.data[0].Priority
}
