s = "If you import the pprint module into your programs, you’ll have access to the pprint() and pformat() functions that will “pretty print” a dictionary’s values. This is helpful when you want a cleaner display of the items in a dictionary than what print() provides. Modify the previous characterCount.py"
count={}
for i in s:
    count.setdefault(i,0)
    count[i] = count[i] + 1

print(count) 
a = " "
print(a.join(["helllo ","hi"," how are you"]))

B = "If you import the pprint module into your programs, you’ll have access to the pprint() and pformat() functions that will “pretty print” a dictionary’s values. This is helpful when you want a cleaner display of the items in a dictionary than what print() provides. Modify the previous characterCount.py"
l = list()
for i in B:
    l.append([i,B.count(i)])
print(l)