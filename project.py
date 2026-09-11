import matplotlib.pyplot as plt
import numpy as np

def simpsons_one_third_area(y_values, h):
    """
    Calculate area using Simpson's 1/3 Rule
    
    Parameters:
    y_values: list of y-coordinates
    h: step size (uniform spacing between x-coordinates)
    
    Returns:
    area: calculated area under the curve
    """
    n = len(y_values) - 1
    if n % 2 != 0:
        raise ValueError("Number of intervals must be even for Simpson's 1/3 Rule.")
    
    result = y_values[0] + y_values[-1]
    
    for i in range(1, n):
        if i % 2 == 0:
            result += 2 * y_values[i]
        else:
            result += 4 * y_values[i]
    
    area = (h / 3) * result
    return area

# Example usage
y_vals = [3.0, 4.5, 5.0, 6.0, 4.5, 3.5, 2.0]  # Sample y-values
h = 1
x_vals = [i * h for i in range(len(y_vals))]

# Compute area
area = simpsons_one_third_area(y_vals, h)
print(f"Area of the irregular lamina: {area}")

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, 'bo-', linewidth=2, markersize=8, label='Data points')
plt.fill_between(x_vals, y_vals, color='skyblue', alpha=0.5, label="Approximate area")
plt.title("Irregular Lamina Area Using Simpson's 1/3 Rule", fontsize=14)
plt.xlabel("x", fontsize=12)
plt.ylabel("y", fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Additional analysis
print(f"\nAnalysis:")
print(f"Number of data points: {len(y_vals)}")
print(f"Number of intervals: {len(y_vals) - 1}")
print(f"Step size (h): {h}")
print(f"x-range: [{x_vals[0]}, {x_vals[-1]}]")
print(f"y-range: [{min(y_vals)}, {max(y_vals)}]")