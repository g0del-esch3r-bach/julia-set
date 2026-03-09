#!/usr/bin/env python3
"""
Construct the Mandelbrot set via bare iteration.

The Mandelbrot set is the set of complex numbers c for which
the function f(z) = z^2 + c does not diverge when iterated from z = 0.
"""

import cmath
import sys
import matplotlib.pyplot as plt
import numpy as np


def mandelbrot_iteration(c, max_iter):
    """
    Compute iterations of f(z) = z^2 + c starting from z = 0.
    
    Returns the number of iterations before divergence or max_iter if not diverged.
    """
    z = 0
    for i in range(max_iter):
        if abs(z) > 2:  # Divergence threshold
            return i
        z = z**2 + c
    return max_iter


def compute_mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    """
    Compute the Mandelbrot set for a given region.
    
    Returns a 2D array where each value represents the iteration count at that point.
    """
    mandelbrot = np.zeros((height, width))
    
    for py in range(height):
        for px in range(width):
            # Convert pixel coordinates to complex plane coordinates
            x = x_min + (x_max - x_min) * px / width
            y = y_min + (y_max - y_min) * py / height
            c = complex(x, y)
            
            # Compute Mandelbrot iteration count
            mandelbrot[py, px] = mandelbrot_iteration(c, max_iter)
    
    return mandelbrot


def plot_mandelbrot(mandelbrot, x_min, x_max, y_min, y_max):
    """Plot the Mandelbrot set."""
    plt.figure(figsize=(10, 8))
    plt.imshow(mandelbrot, extent=[x_min, x_max, y_min, y_max], 
               cmap='hot', interpolation='bilinear')
    plt.colorbar(label='Iteration count')
    plt.title('Mandelbrot Set')
    plt.xlabel('Real axis')
    plt.ylabel('Imaginary axis')
    plt.show()


def main():
    """Main function to compute and display the Mandelbrot set."""
    # Define the region to explore (classic Mandelbrot view)
    x_min, x_max = -2.5, 1.5
    y_min, y_max = -2.0, 2.0
    
    # Resolution and iteration parameters
    width, height = 800, 600
    max_iter = 100
    
    print(f"Computing Mandelbrot set for region [{x_min}, {x_max}] x [{y_min}, {y_max}]")
    print(f"Resolution: {width}x{height}, Max iterations: {max_iter}")
    
    # Compute the Mandelbrot set
    mandelbrot = compute_mandelbrot_set(x_min, x_max, y_min, y_max, 
                                       width, height, max_iter)
    
    # Plot the result
    plot_mandelbrot(mandelbrot, x_min, x_max, y_min, y_max)


if __name__ == "__main__":
    main()
