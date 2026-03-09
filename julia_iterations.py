#!/usr/bin/env python3
"""
Compute iterations of f(z) = z^2 - 1/(16z^2) over complex numbers.

Input: a b n (where z = a + bi)
Output: f^(0)(z), f^(1)(z), ..., f^(n)(z) where z = a+bi
"""

import cmath
import sys
import matplotlib.pyplot as plt
import numpy as np


def f(z):
    """Compute f(z) = z^2 - 1/(16z^2)"""
    if z == 0:
        raise ValueError("z cannot be 0 (division by zero)")
    return z**2 - 1/(16*z**2)

def compute_iterations(z, n):
    """Compute iterations f^(0)(z) through f^(n)(z)"""
    iterations = []
    current = z
    
    for i in range(n + 1):
        iterations.append(current)
        if i < n:  # Don't compute f for the last iteration
            current = f(current)
    
    return iterations

def format_complex(z):
    """Format complex number for output"""
    real = z.real
    imag = z.imag
    
    if abs(real) < 1e-10:
        real = 0
    if abs(imag) < 1e-10:
        imag = 0
    
    if imag == 0:
        return f"{real}"
    elif real == 0:
        return f"{imag}i"
    elif imag > 0:
        return f"{real}+{imag}i"
    else:
        return f"{real}{imag}i"

def plot_iterations(iterations, z, n):
    """Plot the path of iterations in the complex plane"""
    real_parts = [z.real for z in iterations]
    imag_parts = [z.imag for z in iterations]
    
    plt.figure(figsize=(10, 8))
    
    # Plot the path
    plt.plot(real_parts, imag_parts, 'b-o', linewidth=2, markersize=6, label='Iteration path')
    
    # Mark the start and end points
    plt.plot(real_parts[0], imag_parts[0], 'go', markersize=10, label=f'Start: f^(0)(z)')
    plt.plot(real_parts[-1], imag_parts[-1], 'ro', markersize=10, label=f'End: f^({n})(z)')
    
    # Add iteration numbers
    for i, (real, imag) in enumerate(zip(real_parts, imag_parts)):
        plt.annotate(f'{i}', (real, imag), xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.xlabel('Real part')
    plt.ylabel('Imaginary part')
    plt.title(f'Iterations of f(z) = z² - 1/(16z²)\nStarting from z = {format_complex(z)}')
    plt.legend()
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def main():
    """Main function to handle input and output"""
    if len(sys.argv) != 4:
        print("Usage: python julia_iterations.py a b n")
        print("Example: python julia_iterations.py 1 2 5")
        print("Where z = a + bi")
        sys.exit(1)
    
    try:
        a = float(sys.argv[1])
        b = float(sys.argv[2])
        n = int(sys.argv[3])
        if n < 0:
            raise ValueError("n must be non-negative")
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        print("a and b must be numbers, n must be a non-negative integer")
        sys.exit(1)
    
    z = complex(a, b)
    
    try:
        iterations = compute_iterations(z, n)
        
        print(f"Computing f(z) = z^2 - 1/(16z^2) for z = {format_complex(z)}, n = {n}")
        print()
        
        for i, result in enumerate(iterations):
            print(f"f^({i})(z) = {format_complex(result)}")
        
        print()
        print("Plotting iteration path...")
        plot_iterations(iterations, z, n)
            
    except ValueError as e:
        print(f"Error during computation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
