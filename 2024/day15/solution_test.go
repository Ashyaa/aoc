package day15

import (
	. "aoc/utils"
	"fmt"
	"os"
	"slices"
	"sort"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input    = "./input.txt"
	example  = "./example.txt"
	example2 = "./example2.txt"
	example3 = "./example3.txt"
)

var runeToDir = []rune{'^', '>', 'v', '<'}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string, p2 bool) (robot Coord, walls, boxes Set[Coord], moves []int) {
	walls, boxes = Set[Coord]{}, Set[Coord]{}
	raw, _ := os.ReadFile(filepath)
	parts := strings.Split(string(raw), "\n\n")
	for i, line := range strings.Split(parts[0], "\n") {
		for j, char := range line {
			switch char {
			case '#':
				if p2 {
					walls.Add(Coord{X: i, Y: 2 * j})
					walls.Add(Coord{X: i, Y: 2*j + 1})
				} else {
					walls.Add(Coord{X: i, Y: j})
				}
			case 'O':
				if p2 {
					boxes.Add(Coord{X: i, Y: 2 * j})
				} else {
					boxes.Add(Coord{X: i, Y: j})
				}
			case '@':
				if p2 {
					robot = Coord{X: i, Y: 2 * j}
				} else {
					robot = Coord{X: i, Y: j}
				}
			}
		}
	}

	for _, m := range strings.ReplaceAll(parts[1], "\n", "") {
		moves = append(moves, slices.Index(runeToDir, m))
	}
	return
}

func answer(boxes Set[Coord]) (res int) {
	bxs := boxes.ToSlice()
	sort.Slice(bxs, func(i, j int) bool {
		if bxs[i].X == bxs[j].X {
			return bxs[i].Y < bxs[j].Y
		}
		return bxs[i].X < bxs[j].X
	})
	for b := range boxes {
		res += 100*b.X + b.Y
	}
	return
}

func movingBox(walls, boxes Set[Coord], pos, dir Coord) (toMove Coord, canMove bool) {
	for boxes.Contains(pos) {
		pos.X += dir.X
		pos.Y += dir.Y
	}
	return pos, !walls.Contains(pos)
}

func movingBoxP2(walls, boxes Set[Coord], pos Coord, mv int) (toMove Set[Coord], canMove bool) {
	toMove = Set[Coord]{}
	q := Queue[Coord]{pos}
	for !q.IsEmpty() {
		box := q.Pop()
		toMove.Add(box)
		switch mv {
		case 0:
			cell1 := Coord{X: box.X - 1, Y: box.Y - 1}
			cell2 := Coord{X: box.X - 1, Y: box.Y}
			cell3 := Coord{X: box.X - 1, Y: box.Y + 1}
			if walls.Contains(cell2) || walls.Contains(cell3) { // box is blocked by at least 1 wall
				return
			}
			if !boxes.Contains(cell1) && !boxes.Contains(cell2) && !boxes.Contains(cell3) { // box is free to move
				continue // proceed with other boxes that may be blocking
			} // else at least one other box is moving
			if boxes.Contains(cell2) { // box only pushed one box centered the same way
				q.Push(cell2)
				continue
			} // box pushes one or two boxes, shifted to the left and right
			if boxes.Contains(cell1) {
				q.Push(cell1)
			}
			if boxes.Contains(cell3) {
				q.Push(cell3)
			}
		case 1:
			newPos := Coord{X: box.X, Y: box.Y + 2}
			if walls.Contains(newPos) { // next cell is a wall
				return
			}
			if !boxes.Contains(newPos) { // next cell is empty
				return toMove, true
			} // else it is a box
			q.Push(newPos)
		case 2:
			cell1 := Coord{X: box.X + 1, Y: box.Y - 1}
			cell2 := Coord{X: box.X + 1, Y: box.Y}
			cell3 := Coord{X: box.X + 1, Y: box.Y + 1}
			if walls.Contains(cell2) || walls.Contains(cell3) { // box is blocked by at least 1 wall
				return
			}
			if !boxes.Contains(cell1) && !boxes.Contains(cell2) && !boxes.Contains(cell3) { // box is free to move
				continue // proceed with other boxes that may be blocking
			} // else at least one other box is moving
			if boxes.Contains(cell2) { // box only pushed one box centered the same way
				q.Push(cell2)
				continue
			} // box pushes one or two boxes, shifted to the left and right
			if boxes.Contains(cell1) {
				q.Push(cell1)
			}
			if boxes.Contains(cell3) {
				q.Push(cell3)
			}
		case 3:
			newPos := Coord{X: box.X, Y: box.Y - 1}
			otherBox := Coord{X: box.X, Y: box.Y - 2}
			if walls.Contains(newPos) { // next cell is a wall
				return
			}
			if !boxes.Contains(otherBox) { // next cell is empty
				return toMove, true
			} // else it is a box
			q.Push(otherBox)
		}
	}
	return toMove, true
}

func Solve(robot Coord, walls, boxes Set[Coord], moves []int) int {
	for _, mv := range moves {
		offset := Directions[mv]
		newPos := Coord{X: robot.X + offset.X, Y: robot.Y + offset.Y}
		if walls.Contains(newPos) { // newPos is a wall: no op
			continue
		} else if !boxes.Contains(newPos) { // newPos is an empty space: move
			robot = newPos
			continue
		} // else newPos is a box
		dest, canMove := movingBox(walls, boxes, newPos, offset)
		if !canMove {
			continue
		}
		boxes.Remove(newPos)
		boxes.Add(dest)
		robot = newPos
	}
	return answer(boxes)
}

func SolveP2(robot Coord, walls, boxes Set[Coord], moves []int) int {
	for _, mv := range moves {
		offset := Directions[mv]
		vertical := mv%2 == 0
		left := mv == 3
		newPos := Coord{X: robot.X + offset.X, Y: robot.Y + offset.Y}
		pushesLeft := boxes.Contains(newPos)
		newPos2 := Coord{X: newPos.X, Y: newPos.Y - 1} // box whose right part is at newPos
		pushesRight := boxes.Contains(newPos2)
		pushesABox := (mv == 1 && pushesLeft) || (left && pushesRight) || (vertical && (pushesLeft || pushesRight))
		if walls.Contains(newPos) { // newPos is a wall: no op
			continue
		} else if !pushesABox { // newPos is an empty space: move
			robot = newPos
			continue
		} // else robot pushes a box
		var box Coord
		if left || (vertical && pushesRight) {
			box = newPos2
		} else {
			box = newPos
		}
		dest, canMove := movingBoxP2(walls, boxes, box, mv)
		if !canMove {
			continue
		}
		boxes = boxes.Substract(dest)
		for box := range dest {
			boxes.Add(Coord{X: box.X + offset.X, Y: box.Y + offset.Y})
		}
		robot = newPos
	}
	return answer(boxes)
}

func TestDay15(t *testing.T) {
	r := R.New(t)
	r.Equal(2028, Solve(ReadInput(example, false)), "example1 p1")
	r.Equal(10092, Solve(ReadInput(example2, false)), "example2 p1")
	r.Equal(618, SolveP2(ReadInput(example3, true)), "example3 p2")
	r.Equal(9021, SolveP2(ReadInput(example2, true)), "example2 p2")
	r.Equal(1438161, Solve(ReadInput(input, false)), "input p1")
	r.Equal(1437981, SolveP2(ReadInput(input, true)), "input p2")
}

func BenchmarkDay15(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input, false))
		SolveP2(ReadInput(input, true))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
