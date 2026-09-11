# TO FIND THE GRADIENT OF SCALAR POINT FUNCTION
import sympy as sp
from sympy import symbols, diff, pprint

# Define coordinate system and symbols
x, y, z = symbols('x y z')

# Define the scalar function W
W = y*z + z*x + x*y

# Calculate the gradient using diff for each component
gradW_x = diff(W, x)  # ∂U/∂x
gradW_y = diff(W, y)  # ∂U/∂y  
gradW_z = diff(W, z)  # ∂U/∂z

# Create gradient vector
gradW = [gradW_x, gradW_y, gradW_z]

print("Scalar function W =", W)
print(f"Gradient of W is: [{gradW_x}, {gradW_y}, {gradW_z}]")
print("∇W =", gradW)

# Pretty print the result
print("\nFormatted gradient:")
pprint(gradW)
