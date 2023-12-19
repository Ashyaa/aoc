package day19

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"testing"
	"time"

	R "github.com/stretchr/testify/require"
)

const (
	input   = "./input.txt"
	example = "./example.txt"
)

var (
	partReplacer = strings.NewReplacer(
		"{", "",
		"}", "",
		"x=", "",
		"m=", "",
		"a=", "",
		"s=", "",
	)
	wfExp = regexp.MustCompile("([a-z]*){(.*)}")
	cmp   = map[string]func(a, b int) bool{
		"<": func(a, b int) bool { return a < b },
		">": func(a, b int) bool { return a > b },
		"":  func(a, b int) bool { return true },
	}
)

func fromStr(s string) int {
	res, _ := strconv.Atoi(s)
	return res
}

func intMin(a, b int) int { return min(a, b) }
func intMax(a, b int) int { return max(a, b) }

type part map[string]int

func (p part) sum() (res int) {
	for _, v := range p {
		res += v
	}
	return
}

type step struct {
	cat, sign, target string
	value             int
}

func (s step) apply(p part) (string, bool) {
	return s.target, cmp[s.sign](p[s.cat], s.value)
}

func (s step) String() string {
	return s.cat + s.sign + strconv.Itoa(s.value)
}

func (s step) NotString() string {
	other := ">"
	v := s.value - 1
	if s.sign == ">" {
		other = "<"
		v = s.value + 1
	}
	return s.cat + other + strconv.Itoa(v)
}

type workflow []step

func (wf workflow) apply(p part) (res string) {
	var ok bool
	for _, s := range wf {
		res, ok = s.apply(p)
		if ok {
			break
		}
	}
	return res
}

type condition map[string]int

func newCondition() condition {
	return condition{
		"x>": 0,
		"x<": 4001,
		"m>": 0,
		"m<": 4001,
		"a>": 0,
		"a<": 4001,
		"s>": 0,
		"s<": 4001,
	}
}

func (c condition) update(cat, sign string, value int) {
	key := cat + sign
	fn := intMax
	if sign == "<" {
		fn = intMin
	}
	c[key] = fn(c[key], value)
}

func (c condition) solutions() int {
	res := 1
	for _, cat := range []string{"x", "m", "a", "s"} {
		if c[cat+"<"] < c[cat+">"] {
			return 0
		}
		res *= c[cat+"<"] - c[cat+">"] - 1
	}
	return res
}

func newWorkflow(line string) (string, workflow) {
	matches := wfExp.FindStringSubmatch(line)
	steps := []step{}
	for _, stepStr := range strings.Split(matches[2], ",") {
		frags := strings.Split(stepStr, ":")
		if len(frags) == 1 {
			steps = append(steps, step{target: frags[0]})
			continue
		}
		cat := frags[0][0:1]
		sign := frags[0][1:2]
		value := fromStr(frags[0][2:])
		steps = append(steps, step{cat, sign, frags[1], value})
	}
	return matches[1], steps
}

func newPart(line string) part {
	tmp := strings.Split(partReplacer.Replace(line), ",")
	return part{
		"x": fromStr(tmp[0]),
		"m": fromStr(tmp[1]),
		"a": fromStr(tmp[2]),
		"s": fromStr(tmp[3]),
	}
}

// ReadInput retrieves the content of the input file
func ReadInput(filepath string) (wfs map[string]workflow, parts []part) {
	s, _ := os.Open(filepath)
	sc := bufio.NewScanner(s)
	wfs = map[string]workflow{}
	for sc.Scan() {
		line := sc.Text()
		if line == "" {
			break
		}
		name, wf := newWorkflow(line)
		wfs[name] = wf
	}
	for sc.Scan() {
		parts = append(parts, newPart(sc.Text()))
	}
	return
}

func getConditions(wfs map[string]workflow, wf, condition string) []string {
	if wf == "A" {
		return []string{condition}
	}
	if wf == "R" {
		return []string{}
	}
	res := []string{}
	newCondition := condition
	for _, s := range wfs[wf] {
		if s.target != "R" {
			res = append(res, getConditions(wfs, s.target, newCondition+" "+s.String())...)
		}
		newCondition += " " + s.NotString()
	}
	return res
}

func Solve(wfs map[string]workflow, parts []part) (p1 int, p2 int) {
	start := "in"
	for _, p := range parts {
		curWF := start
		for {
			wf := wfs[curWF]
			curWF = wf.apply(p)
			if curWF == "A" || curWF == "R" {
				break
			}
		}
		if curWF == "A" {
			p1 += p.sum()
		}
	}
	for _, conds := range getConditions(wfs, start, "") {
		base := newCondition()
		for _, c := range strings.Split(strings.TrimSpace(conds), " ") {
			if c == "0" {
				continue
			}
			base.update(c[0:1], c[1:2], fromStr(c[2:]))
		}
		p2 += base.solutions()
	}
	return
}

func TestDay19(t *testing.T) {
	r := R.New(t)
	p1Ex, p2Ex := Solve(ReadInput(example))
	r.Equal(19114, p1Ex, "example p1")
	r.Equal(167409079868000, p2Ex, "example p2")
	p1, p2 := Solve(ReadInput(input))
	r.Equal(330820, p1, "input p1")
	r.Equal(123972546935551, p2, "input p2")
}

func BenchmarkDay19(b *testing.B) {
	start := time.Now()
	n := 0
	for i := 0; i < b.N; i++ {
		Solve(ReadInput(input))
	}
	elapsed := time.Since(start)
	fmt.Printf("took %s on average (%d)\n", time.Duration(int(elapsed)/b.N), n)
}
