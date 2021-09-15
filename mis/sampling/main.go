// Sampling aims at finding a sub-optimal maximum independent set by enumerating
// maximal independent sets and take the largest one.
// Coded to compare the runtime to http://doi.org/10.5281/zenodo.3384133.
package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"regexp"
	"strconv"
)

func ParseGraph(r io.Reader) map[int][]int {
	scanner := bufio.NewScanner(r)

	edges := make(map[int][]int)

	soloVertexRegexp := regexp.MustCompile(`^(\d+)$`)
	edgeRegexp := regexp.MustCompile(`^(\d+) (\d+)$`)

	for scanner.Scan() {
		// First check for a single vertex with no edges, in which case
		// it needs to be in the adjency matrix, but with a nil slice of
		// neighbors.
		if soloVertex := soloVertexRegexp.FindString(scanner.Text()); soloVertex != "" {
			n, err := strconv.Atoi(soloVertex)
			if err != nil {
				panic(err)
			}
			edges[n] = nil
			continue
		}

		// Otherwise, check for an edge, and add them to their
		// respective list of neighbors.
		matches := edgeRegexp.FindAllStringSubmatch(scanner.Text(), -1)
		if matches == nil {
			continue
		}
		left, err := strconv.Atoi(matches[0][1])
		if err != nil {
			panic(err)
		}
		right, err := strconv.Atoi(matches[0][2])
		if err != nil {
			panic(err)
		}
		edges[left] = append(edges[left], right)
		edges[right] = append(edges[right], left)
	}

	return edges
}

const aGraph string = `0 1
0 2
0 3
0 4
1 2`

func main() {
	// adj := ParseGraph(strings.NewReader(aGraph))
	// fmt.Printf("run(adj): %v\n", run(adj))
	data, err := ioutil.ReadFile("big_graph.txt")
	if err != nil {
		panic(err)
	}
	adj := ParseGraph(bytes.NewReader(data))
	nAttempts := 10_000
	misCandidate := sampleParallelMIS(adj, nAttempts, 4)
	fmt.Printf("sampleParallelMIS(adj, %d): %v\nlength: %d\n", nAttempts, misCandidate, len(misCandidate))
}
