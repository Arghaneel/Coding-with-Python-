from sympy import *

from tkinter.tix import DisplayStyle
t,r,a,n = symbols('t r a n')
r = a*sin(n*t)
r1 = Derivative(r,t).doit()
r2 = Derivative(r1,t).doit()
rho = (r**2+r1**2)**1.5/(r**2+2*r1**2-r*r2)
rho1= rho.subs(t,pi/2)
rho1= rho1.subs(n,1)
print("the radius of curvature")
DisplayStyle(simpli