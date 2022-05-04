import sys
 
inputFilename = 'input.txt' #sys.argv[1]
#outputFilename = sys.argv[2]

inputFile = open(inputFilename, 'r')
lines = inputFile.readlines()

s1 = ''
s2 = ''

memo = {}

def insertCopyAt(linenum, string):
    linenum = int(linenum)+1
    newString = string[ : int(linenum)] + string + string[int(linenum) : ]
    return newString

# checks if line is number and inserts copy there if it is
# otherwise populates s1 and s2 strings
for line in lines:
    line = line.strip()
    if line.isdigit():
        if s2 == '':
            s1 = insertCopyAt(line, s1)
        else:
            s2 = insertCopyAt(line, s2)
    else:
        if s1 == '':
            s1 = line
        else:
            s2 = line

delta = 30
alphas = [[0,110,48,94],[110, 0, 118, 48],[48, 118, 0, 110],[94, 48,110, 0]]

# s1 and s2 indexes point to the index of the last letter in string
def findMinCost(s1_index, s2_index):
    if (s1_index, s2_index) in memo:
        return memo[(s1_index, s2_index)]
    if s1_index == -1:
        return delta * (s2_index+1)
    elif s2_index == -1:
        return delta * (s1_index+1)

    matchCost = calculateMatchCost(s1_index, s2_index)
    minCost = min(
        matchCost + findMinCost(s1_index-1, s2_index-1),
        delta + findMinCost(s1_index-1, s2_index),
        delta + findMinCost(s1_index, s2_index-1)
    )

    memo[(s1_index, s2_index)] = minCost
    return minCost

def calculateMatchCost(i, j):
    char1 = s1[i]
    char2 = s2[j]

    index1 = convertLetterToAlpha(char1)
    index2 = convertLetterToAlpha(char2)

    matchCost = alphas[index1][index2]
    return matchCost

def convertLetterToAlpha(letter):
    if letter == 'A':
        return 0
    if letter == 'C':
        return 1
    if letter == 'G':
        return 2
    if letter == 'T':
        return 3
    else:
        return -1

def main():
    s1_index = len(s1)-1
    s2_index = len(s2)-1

    minCost = findMinCost(s1_index, s2_index)
    print(minCost)

if __name__ == '__main__':
    main()