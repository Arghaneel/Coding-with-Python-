"""The matrix representation for pollutant concentration is given by:
   A =  (4,-1,0)    B = (20,15,10)
        (-1,3,1)
        (0,1,2)

Each equation in this system represents the balance of pollutants at a specific location, accounting for emissions, absorption, and dispersion.

Problem Statement:
Interpret the given system of equations:
If emissions at a particular site increase, how does it affect the overall concentration levels?
Adjust the matrix to simulate a decrease in pollution at a particular location and observe the changes.
Optimization and Real-World Application:

The method helps in designing pollution control strategies by predicting pollutant levels in different regions.
Authorities can implement measures such as emission reduction or air purification based on these predictions.
"""

import numpy as np
#DEFINE THE SYSTEM FOR POLLUTANT CONCENTRATION 
A = np.array([[4,-1,0],[-1,3,1],[0,1,2]],dtype=float)
B = np.array([20,15,10],dtype=float)
#INITIAL GAUSS
x0 = np.zeros_like(B)
#GAUSS-SEIDEL METHOD
def guass_seidel(A,B,x0,max_tier=100):
    n=len(B)
    x=x0.copy()
    for _ in range(max_tier):
        for i in range(n):
# INDENTED THIS LINE TO BE INSIDE THE FOR LOOP
            sum_ = np.dot(A[i,:],x)-A[i,i]*x[i]
            x[i] = (B[i] - sum_)/A[i,i]
    return x
#SOLVE FOR POLLUTANT CONCENTRATIONS
concentration = guass_seidel(A,B,x0)
print("POLLUTANT CONCENTRATION AT DIFFERENT LOCATION:\n",concentration)    

