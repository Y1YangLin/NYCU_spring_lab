import numpy as np
import random
import itertools
from numpy.linalg import solve
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
    # return rpvalues : dict
    def calculateRpValues(self):
        rho = self.calculateRhoValues()
        permutations_dict, _ = self.jobPermutations()
        rpvalues = {}

        for perm in permutations_dict.values():
            for i in range(len(perm) - 1):
                j1, j2 = perm[i] - 1, perm[i + 1] - 1
                rho_j1, rho_j2 = rho[j1], rho[j2]

                rpvalues[(perm[i], perm[i + 1])] = round(rho_j2 / (rho_j1 + rho_j2), 3)
                rpvalues[(perm[i + 1], perm[i])] = round(rho_j1 / (rho_j1 + rho_j2), 3)  
        return rpvalues 
    
    def calculate_rankings(self):
        permutations_dict, _ = self.jobPermutations()
        rp_values = self.calculateRpValues()
        result = {}
        
        for i in range(self.numOfPlayers):
            for j in range(self.numOfPlayers):
                if i != j:
                    valid_keys = []
                    # 檢查每個排列
                    for key, perm in permutations_dict.items():
                        # 如果i的排名在j前面
                        if perm.index(i + 1) < perm.index(j + 1):
                            valid_keys.append(key)
                            
                    # 儲存結果
                    result[(i+1, j+1)] = {
                        'valid_keys': valid_keys,
                        'rp': rp_values[(i+1, j+1)]
                    }
        
        return result
        
    def solve_permutation_equations(self):
        permutations_dict, _ = self.jobPermutations()
        total_perms =len(permutations_dict)

        rankings = self.calculate_rankings()
        A = np.zeros((len(rankings), total_perms))
        b = [] 

        for i, ((p1, p2), info) in enumerate(rankings.items()):
            valid_keys = info['valid_keys']
            rp_value = info['rp']

            for key in valid_keys:
                A[i][key] = 1

            b.append(rp_value)

        print("\n原始擴增矩陣:")
        augmented_matrix = np.column_stack((A, np.array(b)))
        np.set_printoptions(precision=3, suppress=True)  # 設定小數點位數和抑制科學記號
        print(augmented_matrix)

        # rank_A = np.linalg.matrix_rank(A)
        # rank_Aug = np.linalg.matrix_rank(augmented_matrix)
        # print(f"\n矩陣A的Rank: {rank_A}")
        # print(f"擴增矩陣的Rank: {rank_Aug}")

        try:
            # 使用最小二乘法求解
            x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
            
            # 檢查解的品質
            print("\n最小二乘法解:")
            print(x)
            
            if len(residuals) > 0:
                print(f"\n殘差平方和: {residuals[0]:.6f}")
            
            # 驗證解是否滿足約束條件
            # print("\n驗證解:")
            # print(f"Ax 的結果:")
            # print(np.dot(A, x))
            # print(f"實際 b 值:")
            # print(b)
            # print(f"誤差 (Ax - b):")
            # print(np.dot(A, x) - b)

            # 檢查解是否為合理的機率分佈
            x_normalized = np.where(x < 0, 0, x)  # 將負值設為0
            x_normalized = x_normalized / np.sum(x_normalized)  # 正規化使總和為1
            
            result = {i: round(float(x_normalized[i]), 6) for i in range(total_perms)}
            return result

        except Exception as e:
            print(f"計算過程中發生錯誤: {str(e)}")
            return None
        
    def print_solution(self):
        solution = self.solve_permutation_equations()
        validate = 0
        if solution:
            print("\n最終解 (經過正規化):")
            permutations_dict, _ = self.jobPermutations()
            for key, value in solution.items():
                # if value > 1e-6:  # 只印出非零解
                print(f"排列 {key} {permutations_dict[key]}: {value}")
                validate += value
        print(f"驗證機率變數總合是否趨近為 1: {validate}")
                
        

#Main code
players = int(input("Please enter the number of players :")) 
p = []
w = []
for i in range(players) :
    p.append(random.randint(1, 10))
    w.append(random.randint(1, 10))
data = Single_Job_players(players, p, w)
permutations_dict, letter_dict = data.jobPermutations()
rho = data.calculateRhoValues()
rp_values = data.calculateRpValues()

# print(data.numOfPlayers)
# print(data.P)
# print(data.W)
# print(rho)
# print("Job Permutations : ")
# for key, value in permutations_dict.items():
#     print(f"{key} : {value} -> {letter_dict[key]}")

rankings = data.calculate_rankings()
for (i, j), info in rankings.items():
    print(f"({i}, {j}) -> {info['valid_keys']}, RP: {info['rp']}")

data.print_solution()

