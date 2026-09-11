from sympy import*
r,t = symbols('r,t')
r1=4*(1+cos(t))
r2=5*(1-cos(t))
dr1=diff(r1,t)
dr2=diff(r2,t)
t1=r1/dr1
t2=r2/dr2
q=solve(r1-r2,t)

w1=t1.subs({t:float(q[1])})
w2=t2.subs({t:float(q[1])})
y1=atan(w1)
y2=atan(w2)
w=abs(y1-y2)
print('ANGLE BETWEEN CURVES IN RADIUS IS %0.3f'%(w))

import numpy as np
import matplotlib.pyplot as plt
t_values=np.linspace(0,2*np.pi,100)
r1_values=[r1.subs(t, val).evalf() for val in t_values]
r2_values=[r2.subs(t, val).evalf() for val in t_values]
x1_values=[r*cos(t) for r,t in zip(r1_values, t_values)]
y1_values=[r*sin(t) for r,t in zip(r1_values, t_values)]
x2_values=[r*cos(t) for r,t in zip(r2_values, t_values)]
y2_values=[r*sin(t) for r,t in zip(r2_values, t_values)]
plt.plot(x1_values,y1_values,label='curve 1')
plt.plot(x2_values,y2_values,label='curve 2')
plt.legend()
plt.title("PLOT OF TWO CURVES")
plt.xlabel('X AXIS')
plt.ylabel('Y AXIS')
plt.show()