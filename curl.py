# To find curl of the specific vector field
# F = x²yz î + xy²z ĵ + xyz² k̂

from sympy.vector import *
from sympy import symbols

# Set up 3D coordinate system
N = CoordSys3D('N')

# Define the vector field F = x²yz î + xy²z ĵ + xyz² k̂
F = (N.x**2*N.y*N.z)*N.i + (N.x*N.y**2*N.z)*N.j + (N.x*N.y*N.z**2)*N.k

print("Given Vector Field:")
print("F =", F)
print("\n" + "="*60)

# Calculate curl using the built-in curl function
from sympy.vector import curl
curlF = curl(F)

print("Curl of F:")
print("∇ × F =", curlF)

s= "Python"
newstring = s[0].lower() + s[1:].upper()
print(newstring)  # Outputs: PytHON