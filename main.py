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
    """
    Strategy: Preview next 5 floors and block the highest damage floor
    that's far enough from the last block (respecting 3-floor cooldown)
    """
    # Initialize preview window with first 5 floors
    preview_window = deque(floors[:5])
    
    # Track block planning
    planned_block_floor = None
    last_block_floor = -3
    
    for current_floor, damage in enumerate(floors):
        if explorer.health == 0:
            return explorer.curr_floor
        
        # STEP 1: Plan which future floor to block (if no current plan)
        best_floor = None
        highest_damage = -1
        
        # Look at each floor in the preview window
        for preview_index, preview_damage in enumerate(preview_window):
            candidate_floor = current_floor + preview_index
            
            # Check if this floor is far enough from last block (cooldown = 3 floors)
            floors_since_last_block = candidate_floor - last_block_floor
            if floors_since_last_block >= 3:
                if preview_damage > highest_damage and (planned_block_floor is None or sum(floors[current_floor:candidate_floor+1]) < explorer.health * 0.9):
                    highest_damage = preview_damage
                    best_floor = candidate_floor
        
        # Save the best candidate as our planned block
        planned_block_floor = best_floor
        
        # STEP 2: Execute block if current floor is the planned one
        if planned_block_floor == current_floor and explorer.is_block_avail():
            explorer.skill_block()
            last_block_floor = current_floor
            planned_block_floor = None  # Clear plan after using block
        
        # STEP 3: Take damage from current floor and move up
        explorer.take_damage(damage)
        explorer.progress_floor()
        
        # STEP 4: Slide the preview window forward
        preview_window.popleft()  # Remove current floor from preview
        next_floor_index = current_floor + 5
        if next_floor_index < len(floors):
            preview_window.append(floors[next_floor_index])  # Add next unseen floor

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

    