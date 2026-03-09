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
from matplotlib.widgets import TextBox, Button


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
    """Plot the set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹ with point marking."""
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(hexi_set, extent=[x_min, x_max, y_min, y_max], 
                   cmap='hot', interpolation='bilinear')
    plt.colorbar(im, label='Iteration count')
    ax.set_title(f'Set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹ (z₀ = {z0})\nEnter coordinates and click "Pin Point"')
    ax.set_xlabel('Real axis (c)')
    ax.set_ylabel('Imaginary axis (c)')
    
    # Initialize blue dot (initially hidden)
    blue_dot, = ax.plot([], [], 'bo', markersize=8, markerfacecolor='blue', 
                        markeredgecolor='darkblue', markeredgewidth=2)
    
    # Storage for current coordinates
    current_coords = {'real': 0.0, 'imag': 0.0}
    
    def submit_real(text):
        try:
            current_coords['real'] = float(text)
        except ValueError:
            pass
    
    def submit_imag(text):
        try:
            current_coords['imag'] = float(text)
        except ValueError:
            pass
    
    def pin_point(event):
        # Place the blue dot at the current coordinates
        blue_dot.set_data([current_coords['real']], [current_coords['imag']])
        plt.draw()
    
    # Create text boxes for real and imaginary parts
    ax_real = plt.axes([0.15, 0.02, 0.25, 0.04])
    ax_imag = plt.axes([0.45, 0.02, 0.25, 0.04])
    ax_button = plt.axes([0.75, 0.02, 0.1, 0.04])
    
    text_box_real = TextBox(ax_real, 'Real:', initial='0.0')
    text_box_imag = TextBox(ax_imag, 'Imag:', initial='0.0')
    pin_button = Button(ax_button, 'Pin Point')
    
    text_box_real.on_submit(submit_real)
    text_box_imag.on_submit(submit_imag)
    pin_button.on_clicked(pin_point)
    
    plt.show()


def main():
    """Main function to compute and display the set for f(z) = c(z³ - 3z) + (c(z³ - 3z))⁻¹."""
    # Define the region to explore (zoomed in)
    x_min, x_max = -0.67, 0.67
    y_min, y_max = -0.67, 0.67
    
    # Higher resolution and more iterations for finer detail
    width, height = 1200, 900
    max_iter = 200
    
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
