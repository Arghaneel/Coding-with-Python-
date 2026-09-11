#Simpsons 1/3rd method 
def y(x):
    return 1 / (1 + x**2)

#defining simpsons method 
def simpsons_1_3(x0,xn,n):
    h = (xn - x0) / n
    I = y(x0) + y(xn)
    for i in range(1,n):
        xi = x0 + i*h
        if i % 2 == 0:
            I = I + 2*y(xi)
        else:
            I = I + 4*y(xi)
    I = I * ( h / 3)
    return I

#inputing the values of a,b and n 
result = simpsons_1_3(0,6,6)
print("the result by simpsons 1/3rd method is",result)