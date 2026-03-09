#!/usr/bin/env python3
"""
Generate Julia set for f(z) = z^2 - 1/(16z^2)

The Julia set consists of all starting points z where the iterations remain bounded.
Points that diverge to infinity are colored based on how quickly they escape.

Usage: python julia_set_generator.py [re_min] [re_max] [im_min] [im_max]
Example: python julia_set_generator.py -1 1 -1 1
"""

import cmath
import numpy as np
import matplotlib.pyplot as plt
import sys

def f(z):
    """Compute f(z) = z^2 - 1/(16z^2)"""
    if abs(z) < 1e-10:  # Handle points very close to zero
        # For z ≈ 0, f(z) ≈ -∞, so treat as escaped
        return complex(1000, 1000)  # Large value to trigger escape
    return z**2 - 1/(16*z**2)

def compute_escape_time(z, max_iterations=100, escape_radius=50):
    """
    Compute how many iterations it takes for z to escape.
    Returns max_iterations if the point doesn't escape (belongs to Julia set).
    """
    current = z
    
    for i in range(max_iterations):
        if abs(current) > escape_radius:
            return i  # Escaped at iteration i
        current = f(current)
    
    return max_iterations  # Didn't escape (belongs to Julia set)

def generate_julia_set(xmin=-3, xmax=3, ymin=-3, ymax=3, 
                       width=800, height=800, max_iterations=100):
    """
    Generate Julia set data
    Returns a 2D array where each value represents escape time
    """
    # Create coordinate grids
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    
    # Compute escape times directly without meshgrid to avoid indexing confusion
    escape_times = np.zeros((height, width), dtype=int)
    
    for i in range(height):
        for j in range(width):
            # y[i] is the imaginary part, x[j] is the real part
            z = complex(x[j], y[i])
            escape_times[i, j] = compute_escape_time(z, max_iterations)
    
    # Create X, Y for plotting (but we won't use them for extent)
    X, Y = np.meshgrid(x, y)
    
    return escape_times, X, Y

def plot_julia_set(escape_times, X, Y, max_iterations=100, xmin=-2, xmax=2, ymin=-2, ymax=2):
    """Plot the Julia set"""
    plt.figure(figsize=(12, 10))
    
    # Create custom colormap
    # Points that don't escape (Julia set) are black
    # Points that escape are colored by escape time
    im = plt.imshow(escape_times, extent=[xmin, xmax, ymin, ymax],
                   cmap='hot', origin='lower', interpolation='bilinear')
    
    # Add colorbar
    cbar = plt.colorbar(im, label='Escape time (iterations)')
    cbar.set_ticks([0, max_iterations//4, max_iterations//2, 3*max_iterations//4, max_iterations])
    cbar.set_ticklabels(['0', f'{max_iterations//4}', f'{max_iterations//2}', 
                        f'{3*max_iterations//4}', f'No escape'])
    
    plt.title(f'Julia Set for f(z) = z² - 1/(16z²)', 
              fontsize=14)
    plt.xlabel('Real part', fontsize=12)
    plt.ylabel('Imaginary part', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='white', linestyle='-', alpha=0.5, linewidth=0.5)
    plt.axvline(x=0, color='white', linestyle='-', alpha=0.5, linewidth=0.5)
    plt.tight_layout()
    plt.show()

def main():
    """Main function to generate and plot Julia set"""
    # Parse command line arguments
    if len(sys.argv) == 5:
        try:
            re_min = float(sys.argv[1])
            re_max = float(sys.argv[2])
            im_min = float(sys.argv[3])
            im_max = float(sys.argv[4])
            
            if re_min >= re_max or im_min >= im_max:
                raise ValueError("Invalid range: min must be less than max")
                
        except ValueError as e:
            print(f"Error parsing arguments: {e}")
            print("Usage: python julia_set_generator.py [re_min] [re_max] [im_min] [im_max]")
            print("Example: python julia_set_generator.py -1 1 -1 1")
            sys.exit(1)
    else:
        # Default ranges
        re_min, re_max = -2, 2
        im_min, im_max = -2, 2
        print("Using default range: Re[-2,2], Im[-2,2]")
        print("To specify custom range: python julia_set_generator.py [re_min] [re_max] [im_min] [im_max]")
    
    print(f"Generating Julia set for f(z) = z^2 - 1/(16z^2)...")
    print(f"Range: Real[{re_min}, {re_max}], Imaginary[{im_min}, {im_max}]")
    print("This may take a moment...")
    
    # Generate Julia set
    escape_times, X, Y = generate_julia_set(
        xmin=re_min, xmax=re_max, ymin=im_min, ymax=im_max,
        width=800, height=800, max_iterations=100
    )
    
    print("Plotting Julia set...")
    plot_julia_set(escape_times, X, Y, max_iterations=100, 
                  xmin=re_min, xmax=re_max, ymin=im_min, ymax=im_max)
    
    # Also show some example iterations within the range
    print("\nExample iterations for different starting points:")
    print("-" * 50)
    
    # Generate test points within the specified range
    test_points = [
        complex((re_min + re_max)/2, (im_min + im_max)/2),  # Center
        complex(re_min + 0.1*(re_max-re_min), im_min + 0.1*(im_max-im_min)),  # Bottom-left area
        complex(re_max - 0.1*(re_max-re_min), im_max - 0.1*(im_max-im_min)),  # Top-right area
        complex((re_min + re_max)/2, im_min + 0.1*(im_max-im_min)),  # Bottom-center
        complex(re_min + 0.1*(re_max-re_min), (im_min + im_max)/2),  # Left-center
    ]
    
    for z in test_points:
        escape_time = compute_escape_time(z, max_iterations=100)
        if escape_time == 100:
            print(f"z = {z:.3f}: Bounded (belongs to Julia set)")
        else:
            print(f"z = {z:.3f}: Escaped after {escape_time} iterations")

if __name__ == "__main__":
    main()
