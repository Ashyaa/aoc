package utils

type void struct{}

type Set[T comparable] map[T]void

func NewSet[T comparable](init ...T) Set[T] {
	res := Set[T]{}
	for _, item := range init {
		res[item] = void{}
	}
	return res
}

func (s Set[T]) Add(items ...T) {
	for _, item := range items {
		s[item] = void{}
	}
}

func (s Set[T]) Copy() Set[T] {
	res := Set[T]{}
	for k := range s {
		res[k] = void{}
	}
	return res
}

func (s Set[T]) Remove(items ...T) {
	for _, item := range items {
		if !s.Contains(item) {
			continue
		}
		delete(s, item)
	}
}

func (s Set[T]) Contains(item T) bool {
	_, ok := s[item]
	return ok
}

func (s Set[T]) IsSubset(other Set[T]) bool {
	for k := range s {
		if !other.Contains(k) {
			return false
		}
	}
	return true
}

func (s Set[T]) addSet(other Set[T]) {
	for item := range other {
		s.Add(item)
	}
}

func (s Set[T]) Union(others ...Set[T]) Set[T] {
	res := s.Copy()
	for _, other := range others {
		res.addSet(other)
	}
	return res
}

func Union[T comparable](sets ...Set[T]) Set[T] {
	res := NewSet[T]()
	for _, set := range sets {
		res.addSet(set)
	}
	return res
}

func (s Set[T]) Intersection(others ...Set[T]) Set[T] {
	res := NewSet[T]()
	for k := range s {
		in := true
		for _, other := range others {
			if !other.Contains(k) {
				in = false
				break
			}
		}
		if in {
			res.Add(k)
		}
	}
	return res
}

func Intersection[T comparable](sets ...Set[T]) Set[T] {
	if len(sets) == 0 {
		return NewSet[T]()
	}
	if len(sets) == 1 {
		return sets[0].Copy()
	}
	res := sets[0].Copy()
	return res.Intersection(sets[1:]...)
}

func (s Set[T]) Substract(others ...Set[T]) Set[T] {
	b := Union(others...)
	res := NewSet[T]()
	for k := range s {
		if b.Contains(k) {
			continue
		}
		res.Add(k)
	}
	return res
}

func (s Set[T]) ToSlice() (res []T) {
	for item := range s {
		res = append(res, item)
	}
	return
}
