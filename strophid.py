def fact(num):
    if num == 0:
        return 1
    else:
        return num * fact(num-1)

n = int(input("enter a number:\n"))
r = int(input("enter a number which cannot be greater or negative than n"))
if r > n or r < 0:
    print("invalid")
else:
    nCr = fact(n)/(fact(r)*fact(n-r))
    print(nCr)