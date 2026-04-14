#!/usr/bin/env python3

"""
Julia set generator for g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2)))

This explores the behavior of the complex rational function 
g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2)))
and iterates starting from various z values.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox, Button


def julia_iteration(z, max_iter):
    """
    Compute iterations of g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2))) starting from z.
    
    Returns the number of iterations before divergence or max_iter if not diverged.
    """
    for i in range(max_iter):
        if abs(z) > 50:  # Moderate divergence threshold
            return i
        
        # Check for poles early to avoid expensive computations
        z_sq = z * z
        if abs(z_sq - 1) < 1e-4 or abs(z_sq - 0.25) < 1e-4:  # Moderate pole detection
            return i
        
        # Compute the rational function g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2)))
        numerator = -2 * z**3 * (-1 + 3*z_sq)
        denominator = (z_sq - 1)**2 * (z_sq - 0.25)
        
        # Handle division by zero (poles)
        if abs(denominator) < 1e-8:
            return i  # Treat as divergence at pole
        
        # Apply the function
        z = numerator / denominator
    
    return max_iter


def normalize_to_square(x1, x2, y1, y2):
    """Expand user's rectangle to the smallest containing square."""
    xmid = 0.5 * (x1 + x2)
    ymid = 0.5 * (y1 + y2)
    span = max(x2 - x1, y2 - y1)
    return (
        xmid - span / 2,
        xmid + span / 2,
        ymid - span / 2,
        ymid + span / 2,
    )


def compute_julia_set(x_min, x_max, y_min, y_max, width, height, max_iter):
    """
    Compute the Julia set for g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2))) for a given region.
    
    Returns a 2D array where each value represents the iteration count at that point.
    """
    julia_set = np.zeros((height, width))
    
    # Pre-compute coordinate transformations for efficiency
    x_step = (x_max - x_min) / width
    y_step = (y_max - y_min) / height
    
    for py in range(height):
        # Progress indicator
        if py % 50 == 0:
            print(f"Progress: {py}/{height} rows ({100*py/height:.1f}%)")
            
        y = y_max - (py + 0.5) * y_step  # Invert y-coordinate
        
        for px in range(width):
            # Convert pixel coordinates to complex plane coordinates for z
            x = x_min + (px + 0.5) * x_step
            z = complex(x, y)
            
            # Compute iteration count for this z value
            julia_set[py, px] = julia_iteration(z, max_iter)
    
    return julia_set


def plot_julia_set(julia_set, x_min, x_max, y_min, y_max):
    """Plot the Julia set for g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2))) with point marking."""
    fig, ax = plt.subplots(figsize=(10, 10))

    im = ax.imshow(
        julia_set,
        extent=[x_min, x_max, y_min, y_max],
        origin='upper',
        cmap='hot',
        interpolation='nearest'
    )

    ax.set_aspect('equal')
    ax.set_box_aspect(1)

    fig.colorbar(im, ax=ax, label='Iteration count')
    ax.set_title(
        r'Julia set for g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2)))' + '\n' +
        'Enter coordinates and click "Pin Point"'
    )
    ax.set_xlabel('Real axis (z)')
    ax.set_ylabel('Imaginary axis (z)')
    
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
    """Main function to compute and display the Julia set for g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2)))."""
    # Prompt user for window boundaries
    while True:
        try:
            x1_input = input("Enter x1 (left boundary): ")
            x2_input = input("Enter x2 (right boundary): ")
            y1_input = input("Enter y1 (bottom boundary): ")
            y2_input = input("Enter y2 (top boundary): ")
            
            x1, x2 = float(x1_input), float(x2_input)
            y1, y2 = float(y1_input), float(y2_input)
            
            if x1 >= x2 or y1 >= y2:
                print("Invalid range. Ensure x1 < x2 and y1 < y2.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter numbers.")
    
    # Use user's rectangle, but expand to a square viewing window
    x_min, x_max, y_min, y_max = normalize_to_square(x1, x2, y1, y2)
    
    # Use square resolution
    size = 900
    width = height = size
    max_iter = 200
    
    print(f"Computing Julia set for g(z) = -((2 z^3 (-1 + 3 z^2))/((-1 + z^2)^2 (-1 + 4 z^2)))")
    print(f"Region: [{x_min}, {x_max}] x [{y_min}, {y_max}]")
    print(f"Resolution: {width}x{height}, Max iterations: {max_iter}")
    
    # Compute the Julia set
    julia_set = compute_julia_set(x_min, x_max, y_min, y_max, 
                                  width, height, max_iter)
    
    # Plot the result
    plot_julia_set(julia_set, x_min, x_max, y_min, y_max)


if __name__ == "__main__":
    main()
