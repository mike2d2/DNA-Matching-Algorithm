import sys
import math

#from resource import *
import time
import psutil

sys.setrecursionlimit(10**8)

inputFilename = sys.argv[1]
outputFilename = sys.argv[2]

s1 = ''
s2 = ''
output_string_1 = ""
output_string_2 = ""

memo_array = [[]]

def insertCopyAt(linenum, string):
    linenum = int(linenum)+1
    newString = string[ : int(linenum)] + string + string[int(linenum) : ]
    return newString

delta = 30
alphas = [[0,110,48,94],[110, 0, 118, 48],[48, 118, 0, 110],[94, 48,110, 0]]

# s1 and s2 indexes point to the index of the last letter in string
def findMinCost(x, y):

    memo_list1 = []
    memo_list2 = []
    memo_list_final = []

    for i in range(len(y)+1):
        memo_list1.append(delta * i)
        memo_list2.append(0)
        memo_list_final.append(0)
    
    for s1_index in range(1, len(x)+1):

        memo_list2[0] = memo_list1[0] + 30

        for s2_index in range(1, len(y)+1):
            matchCost = calculateMatchCost(x[s1_index-1], y[s2_index-1])
            
            memo_list2[s2_index] = min(
                matchCost + memo_list1[s2_index-1], # match
                delta + memo_list2[s2_index-1], # add gap to s2
                delta + memo_list1[s2_index]) # add gap to s1
        
        memo_list_final = [i for i in memo_list1]
        memo_list1 = [i for i in memo_list2]

    return (memo_list_final, memo_list2)

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

    return (final_s1, final_s2)



def find_min_cost_recursive(x, y):
    global output_string_1
    global output_string_2

    if len(x) <= 1 or len(y) <= 1:
        basic = Basic('','')
        x_str, y_str = basic.basic_alg(x, y)
        output_string_1 += x_str
        output_string_2 += y_str
        return
    
    x_l, x_r = x[:math.floor(len(x)/2)], x[math.floor(len(x)/2):]

    trash_list, memo_list_x_l = findMinCost(x_l, y)
    y_rev = y[::-1]
    x_r_rev = x_r[::-1]
    trash_list, memo_list_x_r = findMinCost(x_r_rev, y_rev)
    
    min_opt_val = math.inf
    for i in range(len(y)+1):
        opt_val_sum = memo_list_x_l[i] + memo_list_x_r[len(y)-i]
        
        if opt_val_sum < min_opt_val:
            min_opt_val = opt_val_sum
            index_opt = i

    y_l, y_r = y[:index_opt], y[index_opt:]
    
    find_min_cost_recursive(x_l, y_l)
    find_min_cost_recursive(x_r, y_r)
    return


def chooseMin(first, second, third):
    chosen = 0
    min = first
    if second < min:
        min = second
        chosen = 1
    if third < min:
        min = third
        chosen = 2

    return chosen

def calculateMatchCost(x, y):

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

def calc_cost(o1, o2):
    total_cost = 0
    for i in range(len(o1)):
        if o1[i] == '_' or o2[i] == '_':
            total_cost += 30
        else:
            total_cost += calculateMatchCost(o1[i], o2[i])

    return total_cost 

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

def call_algorithm():
    create_data()
    find_min_cost_recursive(s1, s2)
    cost = calc_cost(output_string_1, output_string_2)
    lines = [str(cost), output_string_1, output_string_2]
    with open(outputFilename,"w") as f:
        for i in range(len(lines)):
                f.writelines(lines[i])
                f.writelines("\n")


def create_data():
    global output_string_1
    global output_string_2
    global s1
    global s2
    inputs = ["input.txt"]
    arr = []
    for i in inputs:
        output_string_1 = ''
        output_string_2 = ''
        s1 = ''
        s2 = ''

        inputFile = open(inputFilename, 'r')
        lines = inputFile.readlines()

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


def main():
    # a, b = findMinCost(s1,s2)
    # print(b[len(s2)])
    time = time_wrapper()
    memory = process_memory()

    with open(outputFilename,"a") as f:
        
        f.write(str(time))
        f.write("\n")
        f.write(str(memory))

################################
# THIS IS BASIC ALG CODE USED IN BASE CASE
class Basic:
    def __init__(self, basic_s1, basic_s2):
        self.basic_s1 = basic_s1
        self.basic_s2 = basic_s2

    def basic_alg(self, x, y):
        self.basic_s1 = x
        self.basic_s2 = y
        basic_memo_array = self.basic_findMinCost()
        cost = basic_memo_array[len(self.basic_s2)][len(self.basic_s1)]

        fs1, fs2 = self.basic_calculate_final_string(basic_memo_array)

        return (fs1, fs2)

    # s1 and s2 indexes point to the index of the last letter in string
    def basic_findMinCost(self):

        basic_memo_array = [[0]*(len(self.basic_s1)+1) for i in range((len(self.basic_s2)+1))]

        #
        for i in range(len(self.basic_s1)+1):
            basic_memo_array[0][i] = delta * i

        for i in range(len(self.basic_s2)+1):
            basic_memo_array[i][0] = delta * i
        
        for s1_index in range(1,len(self.basic_s1)+1):
            for s2_index in range(1, len(self.basic_s2)+1):
                matchCost = self.basic_calculateMatchCost(s1_index, s2_index)
                
                basic_memo_array[s2_index][s1_index] = min(
                    matchCost + basic_memo_array[s2_index-1][s1_index-1], # match
                    delta + basic_memo_array[s2_index-1][s1_index], # add gap to s2
                    delta + basic_memo_array[s2_index][s1_index-1]) # add gap to s1

        return basic_memo_array

    def basic_chooseMin(self, first, second, third):
        chosen = 0
        min = first
        if third < min:
            min = third
            chosen = 2
        if second < min:
            min = second
            chosen = 1

        return chosen

    def basic_calculateMatchCost(self, i, j):
        char1 = self.basic_s1[i-1]
        char2 = self.basic_s2[j-1]

        index1 = self.basic_convertLetterToAlpha(char1)
        index2 = self.basic_convertLetterToAlpha(char2)

        matchCost = alphas[index1][index2]
        return matchCost

    def basic_convertLetterToAlpha(self, letter):
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

    def basic_calculate_final_string(self, basic_memo_array):
        s1_index = len(self.basic_s1)
        s2_index = len(self.basic_s2)
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
                matchCost = self.basic_calculateMatchCost(s1_index, s2_index)
                totCost = basic_memo_array[s2_index-1][s1_index-1] + matchCost
                if (totCost == basic_memo_array[s2_index][s1_index]):
                    feasible_match = basic_memo_array[s2_index-1][s1_index-1]
                chose = self.basic_chooseMin(feasible_match, basic_memo_array[s2_index-1][s1_index], basic_memo_array[s2_index][s1_index-1])

            if chose == 0:
                final_s1 = self.basic_s1[s1_index-1] + final_s1
                final_s2 = self.basic_s2[s2_index-1] + final_s2

                s1_index -= 1
                s2_index -= 1
            elif chose == 1:
                final_s1 = '_' + final_s1
                final_s2 = self.basic_s2[s2_index-1] + final_s2
                s2_index -= 1
            elif chose == 2:
                final_s2 = '_' + final_s2
                final_s1 = self.basic_s1[s1_index-1] + final_s1
                s1_index -= 1

        return (final_s1, final_s2)

if __name__ == '__main__':
    main()