#!/usr/bin/env python3
"""
Construct the set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹ via bare iteration.

This explores the behavior of the function f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹ where c is a parameter
and we iterate starting from z = 1.
"""

import cmath
import sys
import matplotlib.pyplot as plt
import numpy as np


def hexi_iteration(c, max_iter, z0=1.0):
    """
    Compute iterations of f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹ starting from z = z0.
    
    Returns the number of iterations before divergence or max_iter if not diverged.
    """
    z = z0
    for i in range(max_iter):
        if abs(z) > 10:  # Divergence threshold
            return i
        
        # Compute c(z³ - 3z)
        inner = c * (z**3 - 3*z)
        
        # Handle division by zero
        if abs(inner) < 1e-10:
            return i  # Treat as divergence
        
        # Apply the function f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹
        z = inner + 1/inner
    
    return max_iter


def compute_hexi_set(x_min, x_max, y_min, y_max, width, height, max_iter, z0=1.0):
    """
    Compute the set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹ for a given region of c values.
    
    Returns a 2D array where each value represents the iteration count at that point.
    """
    hexi_set = np.zeros((height, width))
    
    for py in range(height):
        for px in range(width):
            # Convert pixel coordinates to complex plane coordinates for c
            x = x_min + (x_max - x_min) * px / width
            y = y_min + (y_max - y_min) * py / height
            c = complex(x, y)
            
            # Compute iteration count for this c value
            hexi_set[py, px] = hexi_iteration(c, max_iter, z0)
    
    return hexi_set


def plot_hexi_set(hexi_set, x_min, x_max, y_min, y_max, z0=1.0):
    """Plot the set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹."""
    plt.figure(figsize=(10, 8))
    plt.imshow(hexi_set, extent=[x_min, x_max, y_min, y_max], 
               cmap='hot', interpolation='bilinear')
    plt.colorbar(label='Iteration count')
    plt.title(f'Set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹ (z₀ = {z0})')
    plt.xlabel('Real axis (c)')
    plt.ylabel('Imaginary axis (c)')
    plt.show()


def main():
    """Main function to compute and display the set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹."""
    # Define the region to explore (may need adjustment based on behavior)
    x_min, x_max = -2.0, 2.0
    y_min, y_max = -2.0, 2.0
    
    # Resolution and iteration parameters
    width, height = 800, 600
    max_iter = 100
    
    # Use z₀ = 1 as the initial value
    z0 = 1.0
    
    print(f"Computing set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹")
    print(f"Region: [{x_min}, {x_max}] x [{y_min}, {y_max}]")
    print(f"Resolution: {width}x{height}, Max iterations: {max_iter}")
    print(f"Initial value z₀ = {z0}")
    
    # Compute the set
    hexi_set = compute_hexi_set(x_min, x_max, y_min, y_max, 
                                width, height, max_iter, z0)
    
    # Plot the result
    plot_hexi_set(hexi_set, x_min, x_max, y_min, y_max, z0)


if __name__ == "__main__":
    main()
