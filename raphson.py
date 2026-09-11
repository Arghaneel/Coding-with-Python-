# NEWTON RAPHSON METOD 
from sympy import *
x = symbols('x')
g = input("enter a function:") # input a function
f = lambdify(x,g) # convert the function to a lambda function
dg = diff(g);   # calculate the derivative of the function 

df = lambdify(x,dg) # convert the derivative to a lambda function
x0 = float(input("enter the initial approximation:")); # input the initial approximation
n = int(input("enter the number of iterations:")); # input the number of iterations
for i in range(1,n+1): # loop for the number of iterations
    x1 = (x0 - f(x0)/df(x0)) # calculate the new approximation
    print("iteration %d: x1 = %f" % (i,x1), "function value =", f(x1)) # print the new approximation and the function value

    x0 = x1 # update the initial approximation