import sys
import string
import os.path
fname = input("Enter the filename : ")
#sample file text.txt is given
if not os.path.isfile(fname):
    print("File", fname, "doesn’t exists")
    sys.exit(0)
infile = open(fname, "r")
filecontents = ""
with open('example.txt', 'r', encoding='utf-8') as infile:
    for line in infile:
        for ch in line:
            if ch not in string.punctuation:
                filecontents = filecontents + ch
        else:
            filecontents = filecontents + ' '#replace punctuations and \n with space
wordFreq = {}
wordList = filecontents.split()
#Calculate word Frequency
for word in wordList:
    word = word.lower()
    if word not in wordFreq.keys():
        wordFreq[word] = 1
else:
    wordFreq[word] += 1
#Sort Dictionary based on values in descending order
sortedWordFreq = sorted(wordFreq.items(), key=lambda x:x[1], reverse=True )
#Display 10 most frequently appearing words with their count
print("\n===================================================")
print("10 most frequently appearing words with their count")
print("===================================================")
for i in range(min(10,len(sortedWordFreq))):
    print(sortedWordFreq[i][0], "occurs", sortedWordFreq[i][1], "times")