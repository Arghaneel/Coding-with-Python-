from sympy import *
x , y , z = symbols('x y z')
w3 = integrate(x**2 + y**2,y,x)
pprint(w3)

w4 = integrate(x**2 + y**2 , x,y)
pprint(w4)

if w3 == w4:
    print("BOTH ARE EQUAL")
else:
    print("BOTH ARE NOT EQUAL")