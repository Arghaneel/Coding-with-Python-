num = int(input("enter the number length for the fibonacci series\n"))
firstTerm = 0
secondTerm = 1
print("the fibonacci series for the number length",num,"having firstTerm and secondTerm as\n",firstTerm,"\n",secondTerm)
for i in range (2,num):
    curTerm = firstTerm + secondTerm
    print(curTerm,end="")
    firstTerm = secondTerm
    secondTerm = curTerm
    print()
    