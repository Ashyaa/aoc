package day09

import (
	U "aoc/utils"
	"bufio"
	"fmt"
	"os"
	"slices"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
	SPACE   = -1
)

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (res []int) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	for sc.Scan() {
		for _, r := range sc.Text() {
			res = append(res, U.ToInt(string(r)))
		}
	}
	return
}

func nextSpaceIdx(buffer []int, idx int) int {
	i := idx + 1
	for i < len(buffer) {
		if buffer[i] == SPACE {
			break
		}
		i++
	}
	return i
}

func checksum(buffer []int) (res int) {
	for idx, n := range buffer {
		if n == SPACE {
			continue
		}
		res += idx * n
	}
	return res
}

func p1(buffer, files []int) int {
	lastIndex := len(buffer) - 1
	spaceIndex := nextSpaceIdx(buffer, 0)
	slices.Reverse(files)
	fileIndex := 0
	file := files[fileIndex]
	for spaceIndex < lastIndex {
		if buffer[lastIndex] == SPACE {
			lastIndex--
			continue
		}
		if buffer[lastIndex] != file {
			fileIndex += 1
			file = files[fileIndex]
			continue
		}
		buffer[spaceIndex] = file
		buffer[lastIndex] = SPACE
		spaceIndex = nextSpaceIdx(buffer, spaceIndex)
		lastIndex--
	}

	return checksum(buffer)
}

type space struct {
	idx, size int
}

func getSpaces(buffer []int) (res []space) {
	spaceSize := 0
	for i, n := range buffer {
		if n != SPACE {
			if spaceSize != 0 {
				res = append(res, space{i - spaceSize, spaceSize})
				spaceSize = 0
			}
			continue
		}
		spaceSize++
	}
	return
}

func getNewLocation(spaces []space, size int) (int, space) {
	for idx, space := range spaces {
		if space.size >= size {
			return idx, space
		}
	}
	return -1, space{}
}

func p2(buffer []int) int {
	index := len(buffer) - 1
	file := buffer[index]
	spaces := getSpaces(buffer)
	fileSize := 0
	for index > 0 {
		if fileSize == 0 {
			if buffer[index] != SPACE && buffer[index] <= file {
				file = buffer[index]
				fileSize = 1
			}
			index--
			continue
		}
		if buffer[index] == file {
			fileSize++
			index--
			continue
		}
		idx, avaialbleSpace := getNewLocation(spaces, fileSize)
		if idx < 0 { // file cannot be moved
			fileSize = 0
			continue
		}
		for i := range fileSize {
			buffer[avaialbleSpace.idx+i] = file
			buffer[index+i+1] = SPACE
		}
		spaces = getSpaces(buffer[:index])
		fileSize = 0
	}

	return checksum(buffer)
}

func Solve(input []int) (int, int) {
	size := U.SumSlice(input)
	buffer := make([]int, size)
	id := 0
	index := 0
	files := []int{}
	for i, n := range input {
		if i%2 == 0 {
			files = append(files, id)
			for range n {
				buffer[index] = id
				index++
			}
			id++
		} else {
			for range n {
				buffer[index] = SPACE
				index++
			}
		}
	}

	return p1(append([]int{}, buffer...), files), p2(buffer)
}

func TestDay09(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(1928, p1Ex, "example p1")
	r.Equal(2858, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(6241633730082, p1, "input p1")
	r.Equal(6265268809555, p2, "input p2")
}

func BenchmarkDay09(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
