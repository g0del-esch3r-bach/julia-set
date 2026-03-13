#!/usr/bin/env python3
"""
Construct the set for g_c(z) = z² + c/z² via bare iteration.

This explores the behavior of the function g_c(z) = z² + c/z² where c is a parameter
and we iterate starting from z = c^(1/4).
"""

import cmath
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox, Button


def D8_iteration(c, max_iter):
    """
    Compute iterations of g_c(z) = z² + c/z² starting from z = c^(1/4).
    
    Returns the number of iterations before divergence or max_iter if not diverged.
    """
    # Starting point: z = c^(1/4)
    # Handle c = 0 case
    if abs(c) < 1e-10:
        z = 0.0
    else:
        z = c ** 0.25  # Fourth root of c
    
    for i in range(max_iter):
        if abs(z) > 10:  # Divergence threshold
            return i
        
        # Handle division by zero
        if abs(z) < 1e-10:
            return i  # Treat as divergence
        
        # Apply the function g_c(z) = z² + c/z²
        z = z**2 + c/(z**2)
    
    return max_iter


def compute_D8_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    """
    Compute the set for g_c(z) = z² + c/z² for a given region of c values.
    
    Returns a 2D array where each value represents the iteration count at that point.
    """
    D8_set = np.zeros((height, width))
    
    for py in range(height):
        for px in range(width):
            # Convert pixel coordinates to complex plane coordinates for c
            x = x_min + (x_max - x_min) * px / width
            y = y_min + (y_max - y_min) * py / height
            c = complex(x, y)
            
            # Compute iteration count for this c value
            D8_set[py, px] = D8_iteration(c, max_iter)
    
    return D8_set


def plot_D8_set(D8_set, x_min, x_max, y_min, y_max):
    """Plot the set for g_c(z) = z² + c/z² with point marking."""
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(D8_set, extent=[x_min, x_max, y_min, y_max], 
                   cmap='hot', interpolation='bilinear')
    plt.colorbar(im, label='Iteration count')
    ax.set_title(f'Set for g_c(z) = z² + c/z² (z₀ = c^(1/4))\nEnter coordinates and click "Pin Point"')
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
    """Main function to compute and display the set for g_c(z) = z² + c/z²."""
    # Prompt user for dimension d
    while True:
        try:
            d_input = input("Enter the dimension d for region [-d,d]x[-d,d]: ")
            d = float(d_input)
            if d <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Define the region to explore using user's dimension
    x_min, x_max = -d, d
    y_min, y_max = -d, d
    
    # Higher resolution and more iterations for finer detail
    width, height = 1200, 900
    max_iter = 200
    
    print(f"Computing set for g_c(z) = z² + c/z²")
    print(f"Region: [{x_min}, {x_max}] x [{y_min}, {y_max}]")
    print(f"Resolution: {width}x{height}, Max iterations: {max_iter}")
    print(f"Starting point: z₀ = c^(1/4)")
    
    # Compute the set
    D8_set = compute_D8_set(x_min, x_max, y_min, y_max, 
                            width, height, max_iter)
    
    # Plot the result
    plot_D8_set(D8_set, x_min, x_max, y_min, y_max)


if __name__ == "__main__":
    main()
