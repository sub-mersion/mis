package main

import (
	"math/rand"
	"time"
)

// aMaximalIS computes a single and random maximal independent set on a graph given by
// its adjency map.
func aMaximalIS(adj map[int][]int) []int {
	var vertices []int
	for k := range adj {
		vertices = append(vertices, k)
	}

	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(vertices), func(i, j int) {
		vertices[i], vertices[j] = vertices[j], vertices[i]
	})

	covered := make(map[int]struct{})
	var I []int

	for _, v := range vertices {
		if _, ok := covered[v]; ok {
			continue
		}
		I = append(I, v)
		covered[v] = struct{}{}
		for _, w := range adj[v] {
			covered[w] = struct{}{}
		}
	}

	return I
}

// sampleMIS generates random maximal indepent sets and returns the largest one.
func sampleMIS(adj map[int][]int, n int) (best []int) {
	for i := 0; i < n; i++ {
		a := aMaximalIS(adj)
		if len(a) > len(best) {
			best = a
		}
	}
	return best
}

func worker(adj map[int][]int, jobs <-chan struct{}, result chan<- []int) {
	for range jobs {
		result <- aMaximalIS(adj)
	}
}

// sampleParallelMIS generates random maximal independent sets concurrently via
// a pool of workers and returns the largest one.
func sampleParallelMIS(adj map[int][]int, n, nWorkers int) (best []int) {
	jobs := make(chan struct{}, n)
	result := make(chan []int, n)

	for i := 0; i < nWorkers; i++ {
		go worker(adj, jobs, result)
	}

	for i := 0; i < n; i++ {
		jobs <- struct{}{}
	}

	close(jobs)

	for i := 0; i < n; i++ {
		r := <-result
		if len(r) > len(best) {
			best = r
		}
	}

	return best
}
