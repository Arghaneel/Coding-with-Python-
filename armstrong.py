num = 153
n = num
result= 0
powr = len(str(num))
while n>0:
    ld = n%10
    result = result + (ld ** powr)
    n = n//10
print(num == result)