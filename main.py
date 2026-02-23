import numpy as np
from scipy import stats
import json
from tower import generate_tower, Explorer
from collections import deque

def method_a(floors, explorer):
    for damage in floors:
        if explorer.health == 0:
            return explorer.curr_floor
        
        if damage >= 15:
            explorer.skill_block()
        
        explorer.take_damage(damage)
        explorer.progress_floor()
    
    return explorer.curr_floor
        
def method_b(floors, explorer):
    damage_preview = deque(floors[:5])
    planned_block_index = None
    last_block_floor = -3
    
    for i, damage in enumerate(floors):
        if explorer.health == 0:
            return explorer.curr_floor
        
        if planned_block_index is None:
            
            best_index = None
            best_damage = -1
            
            for j, preview in enumerate(damage_preview):
                real_floor = i + j
                
                if real_floor - last_block_floor >= 3:
                    if preview > best_damage:
                        best_damage = preview
                        best_index = real_floor
            
            planned_block_index = best_index
        
        if planned_block_index == i and explorer.is_block_avail():
            explorer.skill_block()
            last_block_floor = i
            planned_block_index = None
        
        explorer.take_damage(damage)
        explorer.progress_floor()
        
        # Slides damage preview window
        damage_preview.popleft()
        if (i + 5) < len(floors):
            damage_preview.append(floors[i + 5])

    return explorer.curr_floor
        
if __name__ == "__main__":
    with open("config\\tower_b_param.json", "r") as file:
        params = json.load(file)

    method_a_res = np.array([])
    method_b_res = np.array([])
    
    for i in range(params["num_attempts"]):
        print("="*30)
        print(f"Running {i+1}/{params["num_attempts"]} Attempts")
        print("="*30)
        
        floors = generate_tower(**params)
        
        print(f"Method A Logs:")
        explorer = Explorer()
        method_a_res = np.append(method_a_res, method_a(floors, explorer))
        
        print(f"Method B Logs:")
        explorer = Explorer()
        method_b_res = np.append(method_b_res, method_b(floors, explorer))
    
    t_stat, p_val = stats.ttest_ind(method_a_res, method_b_res)

    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_val:.4f}")

    