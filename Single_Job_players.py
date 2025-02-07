import numpy as np
import random
import itertools
from Trie import Trie
class Single_Job_players:
    
    def __init__(self, numOfPlayers:int, P:list, W:list):
        self.numOfPlayers = numOfPlayers
        self.P = P
        self.W = W

    def calculateRhoValues(self):
        return [round(self.P[i] / self.W[i], 3) for i in range(self.numOfPlayers)]
    
    def jobPermutations(self):
        permutations = list(itertools.permutations(range(self.numOfPlayers))) 
        perm_dict = { i : tuple(j + 1 for j in perm) for i, perm in enumerate(permutations)}
        letter_dict = {i: chr(97 + i) for i in range(len(permutations))} #不一定要
        return perm_dict, letter_dict
    
    # 計算Rho prime values
    # return rpvalues : list[]
    def calculateRpValues(self):
        pass


# Main code
players = int(input("Please enter the number of players :")) 
p = []
w = []

for i in range(players) :
    p.append(random.randint(1, 10))
    w.append(random.randint(1, 10))

data = Single_Job_players(players, p, w)
permutations_dict, letter_dict = data.jobPermutations()
rho = data.calculateRhoValues()


print(data.numOfPlayers)
print(data.P)
print(data.W)
print(rho)
print("Job Permutations : ")
for key, value in permutations_dict.items():
    print(f"{key} : {value} -> {letter_dict[key]}")

    
trie = Trie()
for value in permutations_dict.values():
    str_value = "" . join(map(str, value))
    trie.insert(str_value)
    
# 測試是否可以依照設定 print 出 Job i 在 Job j 前的可能排列
print(trie.search_valid_permutations("3", "1"))