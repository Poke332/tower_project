import numpy as np
import scipy as stats
import json
from tower import generate_tower, Explorer
from collections import deque

explorer = Explorer()
num_floors = 100
num_attempts = 1000

def method_a(floors):
    for damage in floors:
        if explorer.health == 0:
            return explorer.curr_floor
        
        if damage >= 15:
            explorer.skill_block()
        
        explorer.take_damage(damage)
        explorer.progress_floor()
        
def method_b(floors):
    damage_preview = deque(floors[:5])
    for damage in floors:
        if explorer.health == 0:
            return explorer.curr_floor
        
        # TODO: Implement Block Logic
        
        # Slides damage preview window
        damage_preview.popleft()
        damage_preview.append(damage)
        
if __name__ == "__main__":
    with open("config\\tower_b_paran.json", "r") as file:
        params = json.load(file)
    
    floors = generate_tower(**params, n=num_floors)
    method_a_res = np.array()
    method_b_res = np.array()
    
    for _ in range(num_attempts):
        method_a_res = np.append(method_a_res, method_a(floors))
        method_b_res = np.append(method_b_res, method_b(floors))
        
    t_stat, p_val = stats.ttest_ind(method_a_res, method_b_res)

    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_val:.4f}")

    