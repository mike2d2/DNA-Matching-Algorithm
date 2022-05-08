import sys
import math

sys.setrecursionlimit(10**6)
inputFilename = 'input.txt' #sys.argv[1]
#outputFilename = sys.argv[2]

inputFile = open(inputFilename, 'r')
lines = inputFile.readlines()

s1 = ''
s2 = ''

memo_array = [[]]

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
def findMinCost(x, y):

    memo_array = [[0]*(len(x)+1) for i in range((len(y)+1))]

    for i in range(len(x)+1):
        memo_array[0][i] = delta * i

    for i in range(len(y)+1):
        memo_array[i][0] = delta * i
    
    for s1_index in range(1,len(x)+1):
        for s2_index in range(1, len(y)+1):
            matchCost = calculateMatchCost(x[s1_index-1], y[s2_index-1])
            
            memo_array[s2_index][s1_index] = min(
                matchCost + memo_array[s2_index-1][s1_index-1], # match
                delta + memo_array[s2_index-1][s1_index], # add gap to s2
                delta + memo_array[s2_index][s1_index-1]) # add gap to s1

    #memo[(s1_index, s2_index)] = chosenMin
    return memo_array

def find_min_match(x,y):
    index = 0
    min_cost = math.inf
    for i in range(len(y)):
        cost = calculateMatchCost(x, y[i])
        if cost < min_cost:
            index = i
            min_cost = cost
    return (min_cost, index)

def calculate_final_string(memo_array, x, y):
    s1_index = len(x)
    s2_index = len(y)
    final_s1 = ''
    final_s2 = ''

    while s1_index > 0 or s2_index > 0:
        #opt = memo_array[s2_index][s2_index]
        if s1_index == 0:
            chose = 1
        elif s2_index == 0:
            chose = 2
        else:
            chose = chooseMin(memo_array[s2_index-1][s1_index-1], memo_array[s2_index-1][s1_index], memo_array[s2_index][s1_index-1])

        if chose == 0:
            final_s1 = x[s1_index-1] + final_s1
            final_s2 = y[s2_index-1] + final_s2

            s1_index -= 1
            s2_index -= 1
        elif chose == 1:
            final_s1 = '_' + final_s1
            final_s2 = y[s2_index-1] + final_s2
            s2_index -= 1
        elif chose == 2:
            final_s2 = '_' + final_s2
            final_s1 = x[s1_index-1] + final_s1
            s1_index -= 1

    # if len(final_s1) > len(final_s2):
    #     final_s1 = final_s1[:-1]
    # else:
    #     final_s2 = final_s2[:-1]

    return (final_s1, final_s2)

def find_min_cost_recursive(x, y):
    if len(x) < 2 or len(y) < 2:
        memo_array = findMinCost(x,y)
        (x_string,y_string) = calculate_final_string(memo_array, x, y)
        return (x_string, y_string, memo_array[len(y)][len(x)])
    
    x_l, x_r = x[:math.floor(len(x)/2)], x[math.floor(len(x)/2):]

    memo_array_x_l = findMinCost(x_l, y)
    y_rev = y[::-1]
    x_r_rev = x_r[::-1]
    memo_array_x_r = findMinCost(x_r_rev, y_rev)
    
    min_opt_val = math.inf
    for i in range(len(y)+1):
        opt_val_sum = memo_array_x_l[i][len(x_l)] + memo_array_x_r[len(y)-i][len(x_r)]
        
        if opt_val_sum < min_opt_val:
            min_opt_val = opt_val_sum
            index_opt = i

    y_l, y_r = y[:index_opt], y[index_opt:]
        
    left_tuple = find_min_cost_recursive(x_l, y_l)
    right_tuple = find_min_cost_recursive(x_r, y_r)

    return (left_tuple[0] + right_tuple[0], left_tuple[1] + right_tuple[1], left_tuple[2] + right_tuple[2])



def chooseMin(first, second, third):
    chosen = 0
    min = first
    if third < min:
        min = third
        chosen = 2
    if second < min:
        min = second
        chosen = 1

    return chosen

def calculateMatchCost(x, y):
    if len(x) != 1 or len(y) != 1:
        asdfl = 0

    char1 = x
    char2 = y

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

    tuple = find_min_cost_recursive(s1, s2)
    print(tuple[0])
    print(tuple[1])
    print(tuple[2])

if __name__ == '__main__':
    main()