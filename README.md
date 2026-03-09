# Julia Set Iterations

Python code to compute iterations of the complex function f(z) = z^2 - 1/(16z^2) with visualization.

## Usage

```bash
python julia_iterations.py a b n
```

Where:
- `a` = real part of the complex number
- `b` = imaginary part of the complex number  
- `n` = number of iterations
- The complex number is z = a + bi

## Examples

```bash
# Compute 5 iterations starting from z = 1+2i
python julia_iterations.py 1 2 5

# Compute 3 iterations starting from z = -1+i
python julia_iterations.py -1 1 3

# Compute 10 iterations starting from z = 0.5-0.5i
python julia_iterations.py 0.5 -0.5 10
```

## Output

The program:
1. Prints f^(0)(z), f^(1)(z), ..., f^(n)(z) where:
   - f^(0)(z) = z (the initial value)
   - f^(k+1)(z) = f(f^(k)(z)) for k ≥ 0
2. Displays a plot showing the path of iterations in the complex plane

## Plot Features

- Blue line with circles showing the iteration path
- Green dot marking the starting point f^(0)(z)
- Red dot marking the ending point f^(n)(z)
- Numbers on each point indicating the iteration count
- Equal aspect ratio for accurate representation

## Function

f(z) = z^2 - 1/(16z^2)

Note: z cannot be 0 due to division by zero.

## Dependencies

- matplotlib
- numpy

Install with: `pip install matplotlib numpy`
