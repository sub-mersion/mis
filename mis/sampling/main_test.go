package main

import (
	"bytes"
	"io/ioutil"
	"testing"
)

func benchmarkSampleParallelMIS(n int, b *testing.B) {
	data, err := ioutil.ReadFile("big_graph.txt")
	if err != nil {
		panic(err)
	}
	adj := ParseGraph(bytes.NewReader(data))
	for i := 1; i < b.N; i++ {
		sampleParallelMIS(adj, 100, n)
	}
}

func BenchmarkSPMIS1(b *testing.B)  { benchmarkSampleParallelMIS(1, b) }
func BenchmarkSPMIS2(b *testing.B)  { benchmarkSampleParallelMIS(2, b) }
func BenchmarkSPMIS4(b *testing.B)  { benchmarkSampleParallelMIS(4, b) }
func BenchmarkSPMIS8(b *testing.B)  { benchmarkSampleParallelMIS(8, b) }
func BenchmarkSPMIS20(b *testing.B) { benchmarkSampleParallelMIS(20, b) }
func BenchmarkSPMIS40(b *testing.B) { benchmarkSampleParallelMIS(40, b) }
