# beta and gamma functions 
from sympy import beta, gamma
m = 5;
n = 7;

m = float(m);
n = float(n);
# calculate beta function
beta_value = beta(m, n)
# calculate gamma function
gamma_value = (gamma(m)*gamma(n))/gamma(m+n)

print(beta_value,gamma_value)

if (abs(beta_value - gamma_value) <= 0.00001):
    print("Beta and Gamma functions are equal")
else:
    print("Beta and Gamma functions are not equal")