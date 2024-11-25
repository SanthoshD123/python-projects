
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter):
    """Determine if a complex number belongs to the Mandelbrot set."""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**2 + c
    return max_iter

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    """Generate a Mandelbrot set for given coordinates and resolution."""
    real = np.linspace(xmin, xmax, width)
    imag = np.linspace(ymin, ymax, height)
    fractal = np.zeros((height, width))
    for i, im in enumerate(imag):
        for j, re in enumerate(real):
            c = complex(re, im)
            fractal[i, j] = mandelbrot(c, max_iter)
    return fractal

# Parameters for the Mandelbrot set
xmin, xmax, ymin, ymax = -2.5, 1.5, -2, 2
width, height = 1000, 1000
max_iter = 100

# Generate the Mandelbrot set and display it
fractal = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
plt.figure(figsize=(10, 10))
plt.imshow(fractal, extent=[xmin, xmax, ymin, ymax], cmap="hot")
plt.colorbar(label="Iterations")
plt.title("Mandelbrot Set")
plt.xlabel("Real")
plt.ylabel("Imaginary")
plt.show()





