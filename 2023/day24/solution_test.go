package day24

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
	"time"

	S "github.com/golang-collections/collections/set"
	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

var (
	lineReplacer = strings.NewReplacer("@", "", ",", "")
)

func fromStr(s string) float64 {
	res, _ := strconv.ParseFloat(s, 64)
	return res
}

type Vector struct {
	x, y, z float64
}

type Line struct {
	pt   Vector
	v    Vector
	a, b float64
}

// func (h Line) At(t float64) Vector {
// 	return Vector{
// 		h.pt.x + t*h.v.x,
// 		h.pt.y + t*h.v.y,
// 		h.pt.z + t*h.v.z,
// 	}
// }

func (l *Line) Affine(mi, ma float64) (float64, float64) {
	if l.a != 0 && l.b != 0 {
		return l.a, l.b
	}
	var n, rx, ry, _ float64
	if l.v.x > 0 {
		n = (ma - l.pt.x) / l.v.x
	} else {
		n = (mi - l.pt.x) / l.v.x
	}
	if l.v.y > 0 {
		n = min(n, (ma-l.pt.y)/l.v.y)
	} else {
		n = min(n, (mi-l.pt.y)/l.v.y)
	}
	rx = l.pt.x + n*l.v.x
	ry = l.pt.y + n*l.v.y
	var dx, dy float64
	if l.v.x > 0 {
		dx = rx - l.pt.x
		dy = ry - l.pt.y
	} else {
		dx = l.pt.x - rx
		dy = l.pt.y - ry
	}
	l.a = dy / dx
	l.b = l.pt.y - l.a*l.pt.x
	return l.a, l.b
}

// func DotProduct(a, b Vector) float64 {
// 	return a.x*b.x + a.y*b.y + a.z*b.z
// }

// func CrossProduct(a, b Vector) Vector {
// 	return Vector{
// 		a.y*b.z - a.z*b.y,
// 		a.z*b.x - a.x*b.z,
// 		a.x*b.y - a.y*b.x,
// 	}
// }

func NewStraightLine(line string) Line {
	fields := strings.Fields(lineReplacer.Replace(line))
	return Line{
		pt: Vector{
			fromStr(fields[0]),
			fromStr(fields[1]),
			fromStr(fields[2]),
		},
		v: Vector{
			fromStr(fields[3]),
			fromStr(fields[4]),
			fromStr(fields[5]),
		},
	}
}

// func (h Line) Intersects(other Line) bool {
// 	a := CrossProduct(h.v, other.v)
// 	dot := DotProduct(a, a)
// 	if dot == 0 {
// 		return false
// 	}
// 	b := CrossProduct(Vector{
// 		other.pt.x - h.pt.x,
// 		other.pt.y - h.pt.y,
// 		other.pt.z - h.pt.z,
// 	}, other.v)
// 	t := DotProduct(b, a) / dot
// 	return float64(int(t)) == t
// }

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []Line) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		res = append(res, NewStraightLine(sc.Text()))
	}
	return
}

func candidates(dx, pos int) *S.Set {
	candidates := S.New()
	for c := -500; c < 500; c++ {
		if c != pos && dx%(c-pos) == 0 {
			candidates.Insert(c)
		}
	}
	return candidates
}

func Solve(stones []Line) (p1 int, p2 float64) {
	minPos, maxPos := 200000000000000., 400000000000000.
	if len(stones) == 5 {
		minPos, maxPos = 7, 27
	}
	xCandidates, yCandidates, zCandidates := S.New(), S.New(), S.New()
	for i, s1 := range stones {
		a, b := s1.Affine(minPos, maxPos)
		for j := i + 1; j < len(stones); j++ {
			s2 := stones[j]
			if s1.v.x == s2.v.x {
				cs := candidates(int(s2.pt.x-s1.pt.x), int(s1.v.x))
				if xCandidates.Len() == 0 {
					xCandidates = cs
				} else {
					xCandidates = xCandidates.Intersection(cs)
				}
			}
			if s1.v.y == s2.v.y {
				cs := candidates(int(s2.pt.y-s1.pt.y), int(s1.v.y))
				if yCandidates.Len() == 0 {
					yCandidates = cs
				} else {
					yCandidates = yCandidates.Intersection(cs)
				}
			}
			if s1.v.z == s2.v.z {
				cs := candidates(int(s2.pt.z-s1.pt.z), int(s1.v.z))
				if zCandidates.Len() == 0 {
					zCandidates = cs
				} else {
					zCandidates = zCandidates.Intersection(cs)
				}
			}
			// P1
			c, d := s2.Affine(minPos, maxPos)
			if a == c {
				continue
			}
			x := (d - b) / (a - c)
			if x < minPos || x > maxPos ||
				(s1.v.x > 0 && (x < s1.pt.x)) || (s1.v.x < 0 && (x > s1.pt.x)) ||
				(s2.v.x > 0 && (x < s2.pt.x)) || (s2.v.x < 0 && (x > s2.pt.x)) {
				continue
			}
			y := a*x + b
			if y < minPos || y > maxPos ||
				(s1.v.y > 0 && (y < s1.pt.y)) || (s1.v.y < 0 && (y > s1.pt.y)) ||
				(s2.v.y > 0 && (y < s2.pt.y)) || (s2.v.y < 0 && (y > s2.pt.y)) {
				continue
			}
			p1++
		}
	}
	rawVector := []int{}
	xCandidates.Do(func(i interface{}) {
		rawVector = append(rawVector, i.(int))
	})
	yCandidates.Do(func(i interface{}) {
		rawVector = append(rawVector, i.(int))
	})
	zCandidates.Do(func(i interface{}) {
		rawVector = append(rawVector, i.(int))
	})
	if len(rawVector) == 3 {
		rock := Line{v: Vector{float64(rawVector[0]), float64(rawVector[1]), float64(rawVector[2])}}
		s1, s2 := stones[0], stones[1]
		// get affine transformation for s1
		a1 := (s1.v.y - rock.v.y) / (s1.v.x - rock.v.x)
		b1 := s1.pt.y - (a1 * s1.pt.x)
		// get affine transformation for s2
		a2 := (s2.v.y - rock.v.y) / (s2.v.x - rock.v.x)
		b2 := s2.pt.y - (a2 * s2.pt.x)
		// by construction (a1-a2) * x + (b1-b2) = 0
		rock.pt.x = (b2 - b1) / (a1 - a2)
		// deduce time from x
		time := (rock.pt.x - s1.pt.x) / (s1.v.x - rock.v.x)
		// compute remaining coordinates
		rock.pt.y = (s1.v.y-rock.v.y)*time + s1.pt.y
		rock.pt.z = (s1.v.z-rock.v.z)*time + s1.pt.z
		p2 = rock.pt.x + rock.pt.y + rock.pt.z
	}
	return
}

func TestDay24(t *testing.T) {
	r := R.New(t)
	p1Ex, _ := Solve(ReadInput(example))
	r.Equal(2, p1Ex, "example p1")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(16018, p1, "input p1")
	r.Equal(1004774995964534., p2, "input p2")
}

func BenchmarkDay24(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
