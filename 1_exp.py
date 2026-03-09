#!/usr/bin/env python3
"""
Construct the set for f(z) = cz - c/z via bare iteration.

This explores the behavior of the function f(z) = cz - c/z where c is a parameter
and we iterate starting from z = 1 (or another initial value).
"""

import cmath
import sys
import matplotlib.pyplot as plt
import numpy as np


def exp_iteration(c, max_iter, z0=1.0):
    """
    Compute iterations of f(z) = cz - c/z starting from z = z0.
    
    Returns the number of iterations before divergence or max_iter if not diverged.
    """
    z = z0
    for i in range(max_iter):
        if abs(z) > 10:  # Divergence threshold
            return i
        if abs(z) < 1e-10:  # Handle division by zero
            return i  # Treat as divergence
        z = c*z - c/z
    return max_iter


def compute_exp_set(x_min, x_max, y_min, y_max, width, height, max_iter, z0=1.0):
    """
    Compute the set for f(z) = cz - c/z for a given region of c values.
    
    Returns a 2D array where each value represents the iteration count at that point.
    """
    exp_set = np.zeros((height, width))
    
    for py in range(height):
        for px in range(width):
            # Convert pixel coordinates to complex plane coordinates for c
            x = x_min + (x_max - x_min) * px / width
            y = y_min + (y_max - y_min) * py / height
            c = complex(x, y)
            
            # Compute iteration count for this c value
            exp_set[py, px] = exp_iteration(c, max_iter, z0)
    
    return exp_set


def plot_exp_set(exp_set, x_min, x_max, y_min, y_max, z0=1.0):
    """Plot the set for f(z) = cz - c/z."""
    plt.figure(figsize=(10, 8))
    plt.imshow(exp_set, extent=[x_min, x_max, y_min, y_max], 
               cmap='hot', interpolation='bilinear')
    plt.colorbar(label='Iteration count')
    plt.title(f'Set for f(z) = cz - c/z (z₀ = {z0})')
    plt.xlabel('Real axis (c)')
    plt.ylabel('Imaginary axis (c)')
    plt.show()


def main():
    """Main function to compute and display the set for f(z) = cz - c/z."""
    # Define the region to explore (may need adjustment based on behavior)
    x_min, x_max = -3.0, 3.0
    y_min, y_max = -3.0, 3.0
    
    # Resolution and iteration parameters
    width, height = 800, 600
    max_iter = 100
    
    # Use z₀ = 1 + i as the initial value
    z0 = complex(1, 1)
    
    print(f"Computing set for f(z) = cz - c/z with z₀ = {z0}")
    print(f"Region: [{x_min}, {x_max}] x [{y_min}, {y_max}]")
    print(f"Resolution: {width}x{height}, Max iterations: {max_iter}")
    
    # Compute the set
    exp_set = compute_exp_set(x_min, x_max, y_min, y_max, 
                             width, height, max_iter, z0)
    
    # Plot the result
    plot_exp_set(exp_set, x_min, x_max, y_min, y_max, z0)


if __name__ == "__main__":
    main()
