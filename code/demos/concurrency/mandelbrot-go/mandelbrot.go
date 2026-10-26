package main

import (
	"fmt"
	"image"
	"image/color"
	"image/png"
	"math"
	"os"
	"os/exec"
	"strconv"
	"sync"
	"time"
)

const (
	W = 6400
	H = 6400
)

var pic [W][H]int

func mandelbrot(x, y int) int {
	n := 0
	a, b := 0.0, 0.0
	for a*a+b*b < 4 && n < 880 {
		a, b = a*a-b*b+float64(x)*1024/float64(W)*8e-9+0.356888,
			2*a*b+float64(y)*1024/float64(H)*8e-9-0.645411
		n++
	}
	return n
}

func worker(tid, nthread int, wg *sync.WaitGroup) {
	defer wg.Done()
	xPer := W / nthread
	lo, hi := tid*xPer, (tid+1)*xPer

	for x := lo; x < hi; x++ {
		for y := 0; y < H; y++ {
			pic[x][y] = mandelbrot(x, y)
		}
	}
}

func renderPreview() {
	step := W / 256
	w, h := W/step, H/step

	cmd := exec.Command("img2sixel", "-w", "1024", "-h", "1024", "-")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return
	}
	cmd.Start()

	fmt.Fprintf(stdin, "P6\n%d %d\n255\n", w, h)
	for j := 0; j < H; j += step {
		for i := 0; i < W; i += step {
			n := float64(pic[i][j])
			t := (n - 80) / 800.0
			stdin.Write([]byte{
				byte(clamp(255 * math.Pow(t, 3))),
				byte(clamp(255 * math.Pow(t, 0.7))),
				byte(clamp(255 * math.Pow(t, 0.5))),
			})
		}
	}
	stdin.Close()
	cmd.Wait()
}

func writePNG(path string) {
	f, err := os.Create(path)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	img := image.NewRGBA(image.Rect(0, 0, W, H))
	for x := 0; x < W; x++ {
		for y := 0; y < H; y++ {
			n := float64(pic[x][y])
			t := (n - 80) / 800.0
			img.SetRGBA(x, y, color.RGBA{
				byte(clamp(255 * math.Pow(t, 3))),
				byte(clamp(255 * math.Pow(t, 0.7))),
				byte(clamp(255 * math.Pow(t, 0.5))),
				255,
			})
		}
	}
	png.Encode(f, img)
}

func clamp(v float64) uint8 {
	if v < 0 {
		return 0
	}
	if v > 255 {
		return 255
	}
	return uint8(v)
}

func main() {
	nthread := 1
	if len(os.Args) > 1 {
		if n, err := strconv.Atoi(os.Args[1]); err == nil && n > 0 {
			nthread = n
		}
	}

	var wg sync.WaitGroup
	for i := 0; i < nthread; i++ {
		wg.Add(1)
		go worker(i, nthread, &wg)
	}

	done := make(chan struct{})
	go func() { wg.Wait(); close(done) }()

	ticker := time.NewTicker(500 * time.Millisecond)
	defer ticker.Stop()
	fmt.Print("\033[2J\033[H")

	for {
		select {
		case <-ticker.C:
			fmt.Print("\033[H")
			renderPreview()
		case <-done:
			writePNG("mandelbrot.png")
			fmt.Printf("\nDone. Rendered %dx%d with %d goroutines\n", W, H, nthread)
			return
		}
	}
}
