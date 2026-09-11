"""Curvature analysis plays a crucial role in navigation, robotics, and motion planning. Understanding how a curve bends at different points 
helps in designing optimal paths for vehicles, drones, and robotic arms.

In this study, we analyze the mathematical curvature of the function y = sin(x) by computing its first and second derivatives. 
Using these derivatives, we determine the radius of curvature, which indicates how sharply the curve bends at different locations.
The radius of curvature is given by the formula:
 R = 1 + (dy/dx**2) ** 1.5  / (d2y/dx2)
 where:
 dy and dx are first order derivative (slope of curve)
 d2y and d2x are second order derivative (rate of change of slope)

Problem Statement:
Understanding the Curve's Behavior:

Identify locations where the curve bends the most.
Observe how the radius of curvature varies along the sine wave.
Impact on Motion Planning:

How does the curvature affect vehicle trajectory in navigation systems?
Can we determine optimal turning points based on curvature?
Applications in Real-World Navigation Systems:

Used in self-driving cars for adjusting steering based on road curvature.
Helps in designing safe flight paths for drones and aircraft.
Used in robotics for smooth and efficient motion control.
"""
import numpy as np
import matplotlib.pyplot as plt

# Define the curve y = sin(x)
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

# Compute derivatives
dy_dx = np.gradient(y, x)  # First derivative
d2y_dx2 = np.gradient(dy_dx, x)  # Second derivative

# Compute the radius of curvature
radius_of_curvature = ((1 + dy_dx**2)**1.5) / np.abs(d2y_dx2)

# Visualize the curve and curvature points
plt.figure(figsize=(10, 6))
plt.plot(x, y, label="Curve (y = sin(x))", color='blue')
plt.scatter(x[::10], y[::10], 
           color='red', label='Curvature Points')

for i in range(0, len(x), 10):
    plt.text(x[i], y[i]-0.1,
            f"R={radius_of_curvature[i]:.2f}",
            fontsize=8, color='green')

plt.title("Curve and Radius of Curvature")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid()
plt.show()