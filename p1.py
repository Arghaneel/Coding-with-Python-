import numpy as np
import matplotlib.pyplot as plt

# Define the parameter 'a' (scale of the cardioid)
a = 1

# Generate theta values (0 to 2π for a complete cardioid)
theta = np.linspace(0, 2 * np.pi, 500)

# Calculate the radial distance 'r' using the cardioid equation
r = a * (1 + np.cos(theta))

# Convert polar coordinates (r, theta) to Cartesian coordinates (x, y)
x = r * np.cos(theta)
y = r * np.sin(theta)

# Plot the cardioid
plt.figure(figsize=(8, 8))
plt.plot(x, y, color='blue', linewidth=2)

# Add labels and title
plt.title("Cardioid Shape for Optics and Light Applications", fontsize=14)
plt.xlabel("X-axis (Cartesian Coordinates)")
plt.ylabel("Y-axis (Cartesian Coordinates)")
plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')
plt.grid(True, linestyle='--', alpha=0.7)
plt.axis('equal')  # Ensure the plot is not distorted

# Show the plot
plt.show()
