package utils

import (
	"testing"

	R "github.com/stretchr/testify/require"
)

func TestCounter(t *testing.T) {
	r := R.New(t)
	c := NewCounter[string]()
	r.Equal(Counter[string](map[string]int{}), c)
	c.Add("lorem ipsum dolor sit amet")
	r.Equal(1, c.Len(), "string counter len")
	r.Equal(1, c.Total(), "string counter total")

	c2 := NewCounter[rune]()
	c2.Add([]rune("lorem ipsum dolor sit amet")...)
	r.Equal(13, c2.Len(), "rune counter len")
	r.Equal(26, c2.Total(), "rune counter total")
	r.Equal(0, c2.Count('!'), "'!' rune count")
	r.Equal(3, c2.Count('m'), "'m' rune count")
	c2.Clear()
	r.Equal(0, c2.Len(), "rune counter len after clear")
	r.Equal(0, c2.Total(), "rune counter total after clear")
}
