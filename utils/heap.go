package utils

import "container/heap"

// TODO: Maybe

type queueItem[T any] struct {
	index, priority int
	value           T
}

type pQueue[T any] struct {
	increasing bool
	data       []*queueItem[T]
}

func newPQueue[T any](items ...queueItem[T]) pQueue[T] {
	res := pQueue[T]{
		data:       make([]*queueItem[T], 0),
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
		return pq.data[i].priority < pq.data[j].priority
	}
	return pq.data[i].priority > pq.data[j].priority
}

func (pq pQueue[T]) Swap(i, j int) {
	pq.data[i], pq.data[j] = pq.data[j], pq.data[i]
	pq.data[i].index = i
	pq.data[j].index = j
}

func (pq *pQueue[T]) Push(x any) {
	n := len((*pq).data)
	it := x.(queueItem[T])
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
// priority 1.
func NewPriorityQueue[T any](items ...T) PriorityQueue[T] {
	heapItems := Map(items, func(item T) queueItem[T] {
		return queueItem[T]{
			priority: 1,
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
	heap.Push(p.q, queueItem[T]{
		priority: priority,
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
