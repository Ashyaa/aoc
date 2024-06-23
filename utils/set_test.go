package utils

import (
	"testing"

	R "github.com/stretchr/testify/require"
)

func TestNew(t *testing.T) {
	tests := []struct {
		name string
		args []int
		want Set[int]
	}{
		{
			name: "Empty",
			args: []int{},
			want: Set[int]{},
		},
		{
			name: "One element",
			args: []int{2},
			want: Set[int]{2: void{}},
		},
		{
			name: "Several elements",
			args: []int{2, 5, 9},
			want: Set[int]{
				5: void{},
				9: void{},
				2: void{},
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			r := R.New(t)
			r.Equal(tt.want, NewSet(tt.args...))
		})
	}
}

func TestAdd(t *testing.T) {
	tests := []struct {
		name string
		args []int
		want Set[int]
	}{
		{
			name: "Empty",
			args: []int{},
			want: Set[int]{},
		},
		{
			name: "One element",
			args: []int{2},
			want: Set[int]{2: void{}},
		},
		{
			name: "Same element several times",
			args: []int{2, 3, 6, 3, 2},
			want: Set[int]{
				2: void{},
				3: void{},
				6: void{},
			},
		},
		{
			name: "Several elements",
			args: []int{2, 5, 9},
			want: Set[int]{
				5: void{},
				9: void{},
				2: void{},
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			r := R.New(t)
			s := NewSet[int]()
			s.Add(tt.args...)
			r.Equal(tt.want, s)
		})
	}
}

func TestCopy(t *testing.T) {
	ref := NewSet(2, 9, 5)
	tests := []struct {
		name string
		want Set[int]
	}{
		{
			name: "Several elements",
			want: Set[int]{
				2: void{},
				5: void{},
				9: void{},
			},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			r := R.New(t)
			s := ref.Copy()
			r.Equal(tt.want, s)
			delete(s, 5)
			r.Equal(NewSet[int](2, 9), s)
			r.Equal(NewSet[int](2, 9, 5), ref)
		})
	}

}

func TestRemove(t *testing.T) {
	ref := NewSet(2, 3, 6, 9, 7, 5)
	tests := []struct {
		name string
		args []int
		want Set[int]
	}{
		{
			name: "Empty",
			args: []int{},
			want: ref,
		},
		{
			name: "One element",
			args: []int{2},
			want: Set[int]{
				3: void{},
				6: void{},
				9: void{},
				7: void{},
				5: void{},
			},
		},
		{
			name: "Several elements",
			args: []int{2, 5, 9},
			want: Set[int]{
				3: void{},
				6: void{},
				7: void{},
			},
		},
		{
			name: "Elements not in the set",
			args: []int{987, 55, 689},
			want: ref,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			r := R.New(t)
			s := ref.Copy()
			s.Remove(tt.args...)
			r.Equal(tt.want, s)
		})
	}
	R.Equal(t, NewSet[int](2, 3, 6, 9, 7, 5), ref, "ref should not be mutated from being copied")
}

func TestContains(t *testing.T) {
	r := R.New(t)
	s := NewSet(1, 2, 5, 6)
	r.True(s.Contains(2))
	r.False(s.Contains(185))
}

func TestIsSubset(t *testing.T) {
	r := R.New(t)
	s := NewSet(2, 5)
	r.True(s.IsSubset(NewSet(1, 2, 5, 6, 98, 100)))
	r.False(s.IsSubset(NewSet(1, 2, 4, 8, 16)))
	r.True(NewSet[int]().IsSubset(s))
	r.True(s.IsSubset(s))
}

func TestAddSet(t *testing.T) {
	r := R.New(t)
	s := NewSet(2, 5)
	s.addSet(NewSet(1, 2, 3, 4))
	r.Equal(NewSet(1, 2, 3, 4, 5), s)
}

func TestUnion(t *testing.T) {
	r := R.New(t)
	s := NewSet(1, 2, 3)
	exp := NewSet(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
	r.Equal(exp, s.Union(
		NewSet(2, 4, 6, 8, 10),
		NewSet(1, 2, 3, 4, 5),
		NewSet(8, 9, 1),
		NewSet(7, 10, 2),
	), "as method")
	r.Equal(exp, Union(
		s,
		NewSet(2, 4, 6, 8, 10),
		NewSet(1, 2, 3, 4, 5),
		NewSet(8, 9, 1),
		NewSet(7, 10, 2),
	), "as function")
}

func TestIntersection(t *testing.T) {
	r := R.New(t)
	s := NewSet(1, 2, 3, 4, 5)
	exp := NewSet(5)
	r.Equal(exp, s.Intersection(
		NewSet(1, 4, 5, 6, 9),
		NewSet(5, 7, 9, 10),
	), "as method")
	r.Equal(exp, Intersection(
		s,
		NewSet(1, 4, 5, 6, 9),
		NewSet(5, 7, 9, 10),
	), "as function")
	r.Equal(NewSet[int](), Intersection[int](), "no sets")
	r.Equal(s, Intersection[int](s), "one set")
}

func TestSubstract(t *testing.T) {
	r := R.New(t)
	s := NewSet(1, 2, 3, 4, 5)
	exp := NewSet(5, 3)
	r.Equal(exp, s.Substract(
		NewSet(2, 4, 6, 8, 10),
		NewSet(8, 9, 1),
		NewSet(7, 10, 2),
	))
}
