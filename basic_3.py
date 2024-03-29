# FINAL VERSION

import sys
import math

import time
import psutil

sys.setrecursionlimit(10**6)
inputFilename = sys.argv[1]
outputFilename = sys.argv[2]

inputFile = open(inputFilename, 'r')
lines = inputFile.readlines()

s1 = ''
s2 = ''

memo_array = [[]]

def insertCopyAt(linenum, string):
    linenum = int(linenum)+1
    newString = string[ : int(linenum)] + string + string[int(linenum) : ]
    return newString

delta = 30
alphas = [[0,110,48,94],[110, 0, 118, 48],[48, 118, 0, 110],[94, 48,110, 0]]

# s1 and s2 indexes point to the index of the last letter in string
def findMinCost():

    memo_array = [[0]*(len(s1)+1) for i in range((len(s2)+1))]

    #
    for i in range(len(s1)+1):
        memo_array[0][i] = delta * i

    for i in range(len(s2)+1):
        memo_array[i][0] = delta * i
    
    for s1_index in range(1,len(s1)+1):
        for s2_index in range(1, len(s2)+1):
            matchCost = calculateMatchCost(s1_index, s2_index)
            
            memo_array[s2_index][s1_index] = min(
                matchCost + memo_array[s2_index-1][s1_index-1], # match
                delta + memo_array[s2_index-1][s1_index], # add gap to s2
                delta + memo_array[s2_index][s1_index-1]) # add gap to s1

    return memo_array

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

def calculateMatchCost(i, j):
    char1 = s1[i-1]
    char2 = s2[j-1]

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

def calculate_final_string(memo_array):
    s1_index = len(s1)
    s2_index = len(s2)
    final_s1 = ''
    final_s2 = ''

    while s1_index > 0 or s2_index > 0:
        #opt = memo_array[s2_index][s2_index]
        if s1_index == 0:
            chose = 1
        elif s2_index == 0:
            chose = 2
        else:
            feasible_match = math.inf
            matchCost = calculateMatchCost(s1_index, s2_index)
            totCost = memo_array[s2_index-1][s1_index-1] + matchCost
            if (totCost == memo_array[s2_index][s1_index]):
                feasible_match = memo_array[s2_index-1][s1_index-1]
            chose = chooseMin(feasible_match, memo_array[s2_index-1][s1_index], memo_array[s2_index][s1_index-1])

        if chose == 0:
            final_s1 = s1[s1_index-1] + final_s1
            final_s2 = s2[s2_index-1] + final_s2

            s1_index -= 1
            s2_index -= 1
        elif chose == 1:
            final_s1 = '_' + final_s1
            final_s2 = s2[s2_index-1] + final_s2
            s2_index -= 1
        elif chose == 2:
            final_s2 = '_' + final_s2
            final_s1 = s1[s1_index-1] + final_s1
            s1_index -= 1

    return (final_s1, final_s2)





def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


def time_wrapper():
    start_time = time.time()
    call_algorithm()
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return time_taken

def setup_data():
    global s1
    global s2
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


def call_algorithm():
    setup_data()
    memo_array = findMinCost()
    cost = memo_array[len(s2)][len(s1)]

    final_strings = calculate_final_string(memo_array)

    lines = [str(cost), final_strings[0], final_strings[1]]
    with open(outputFilename,"w") as f:
        for i in range(len(lines)):
                f.writelines(lines[i])
                f.writelines("\n")

def main():
    time = time_wrapper()
    memory = process_memory()
    with open(outputFilename,"a") as f:
        f.write(str(time))
        f.write("\n")
        f.write(str(memory))

if __name__ == '__main__':
    main()