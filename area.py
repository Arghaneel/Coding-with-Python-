from sympy import *
x = symbols('x')
y = symbols('y')

a = 4
b = 6
w3 = 4 * integrate(1,(y,0,(b/a) * sqrt(a**2 - x**2)) )
print (w3)
