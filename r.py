import numpy as np 
import matplotlib.pyplot as plt 
# Example data: Years and corresponding sales 
x = np.array([1, 2, 3, 4, 5]) # Years 
y = np.array([1, 2, 2.5, 4, 5]) # Sales 
# Construct matrix for linear system (Ax = b) 
A = np.vstack([x, np.ones_like(x)]).T 
b = y 
# Solve the system using Gaussian elimination 
def gauss_elimination(A, b): 
    n = len(b) 
    for i in range(n): 
        max_row = max(range(i, n), key=lambda r: abs(A[r][i])) 
        A[[i, max_row]] = A[[max_row, i]] 
        b[i], b[max_row] = b[max_row], b[i] 
        for j in range(i+1, n): 
            factor = A[j, i] / A[i, i] 
            A[j, i:] -= factor * A[i, i:] 
            b[j] -= factor * b[i] 
            x = np.zeros(n) 
            for i in range(n-1, -1, -1): 
                x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i] 
                return x 
coefficients = gauss_elimination(A, b) 
plt.plot(x, y, 'bo', label='Data points') 
plt.plot(x, coefficients[0] * x + coefficients[1], 'r-', label='Fitted line') 
plt.xlabel('Years') 
plt.ylabel('Sales') 
plt.legend() 
plt.show()