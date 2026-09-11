# REGULAR - FALSI METHOD 
from sympy import * 
x = Symbol('x') 
g = input("enter the function") # input the function
f = lambdify(x,g) # convert the function to a lambda function
a = float(input("enter a claue:")) # input the claue
b = float(input("enter b claue:")) 
N = int(input("enter number of iterations:")) # input the number of iterations

for i in range(1,N+1): 
    c = (a*f(b)-b*f(a))/(f(b) - f(a)) # calculate the new claue
    if ((f(a)*f(c)<0)): # if the function is negative at a and positive at c, then there is a root between a
        b = c 
    else:
        a = c # otherwise, there is a root between b
    print("iteration : ",i," x: ",c," f(x): ",f(c)) # print the iteration number, the value of x and the value of the function at x