import numpy as np
import matplotlib.pyplot as plt

def calculate_angle(curve_func, x_point, h=1e-5):
    """
    Calculate the angle between a curve and the horizontal line at a specific point.

    Parameters:
        curve_func (callable): The curve function, y = f(x).
        x_point (float): The x-coordinate of the point.
        h (float): A small step size for numerical differentiation.

    Returns:
        float: The angle in degrees.
    """
    # Numerical differentiation (slope of the tangent)
    slope = (curve_func(x_point + h) - curve_func(x_point - h)) / (2 * h)
    
    # Calculate the angle in radians and convert to degrees
    angle_radians = np.arctan(slope)
    angle_degrees = np.degrees(angle_radians)
    
    return angle_degrees

# Example curve function
def example_curve(x):
    return x**2  # Example: y = x^2

# Test parameters
x_point = 1.0  # Point of interest on the curve

# Calculate angle
angle = calculate_angle(example_curve, x_point)
print(f"The angle between the curve and the horizontal at x = {x_point} is {angle:.2f} degrees.")

# Optional plotting
plot = True
if plot:
    x_values = np.linspace(-2, 2, 500)
    y_values = example_curve(x_values)
    
    # Tangent line
    slope = (example_curve(x_point + 1e-5) - example_curve(x_point - 1e-5)) / (2 * 1e-5)
    tangent_y = slope * (x_values - x_point) + example_curve(x_point)
    
    plt.plot(x_values, y_values, label="Curve")
    plt.plot(x_values, tangent_y, label="Tangent", linestyle="--")
    plt.scatter([x_point], [example_curve(x_point)], color="red", label="Point of Interest")
    plt.axhline(y=example_curve(x_point), color="gray", linestyle=":")
    plt.title("Curve and Tangent Line")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
