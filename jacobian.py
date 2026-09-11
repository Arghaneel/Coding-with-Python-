from sympy import*
def phirho,theta:

x=rho*cos(phi)*sin(theta);
y=rho*cos(phi)*cos(theta);
z=rho*sin(phi);
dx=diff(x,rho)
dy=diff(y,rho)
dz=diff(z,rho)
dx1=diff(x,phi)
dy1=diff(y,phi)
dz1=diff(z,phi)
dx2=diff(x,theta)
dy2=diff(y,theta)
dz2=diff(z,theta)
J=Matrix([[dx,dy,dz],[dx1,dy1,dz1],[dx2,dy2,dz2]]);
print("THE JACOBIAN MATRIX IS\n")
print(J)
print('\n\n J=',Jac)
print(simplify (det(J)))




