import numpy as np

class Explorer:
    def __init__(self):
        self._health = 100
        self._hp_capacity = 100
        self._curr_floor = 0
        self._is_blocking = False
        self._block_cd = 0
    
    @property
    def health(self):
        return self._health
    
    @property
    def curr_floor(self):
        return self._curr_floor
    
    def progress_floor(self):
        self._curr_floor += 1
        if self._block_cd > 0:
            self._block_cd -= 1
    
    def take_damage(self, damage):
        if self._is_blocking:
            self._is_blocking = False
        else:
            self._health = self._health - damage
        
            if self._health < 0:
                self._health = 0
            
    def is_block_avail(self):
        return self._block_cd == 0
    
    def skill_block(self):
        if self.is_block_avail():
            self._is_blocking = True
            self._block_cd = 3
            print(f"Damage Blocked on Floor {self.curr_floor}")
        else:
            print(f"Block is on Cooldown for {self._block_cd} Floors")
        
    
    

def generate_tower(p: float, mu: float, sigma: float, n: int, **kwargs):
    """Generates a tower in a form of numpy array filled with damage numbers

    Args:
        p (float): _description_
        mu (float): _description_
        sigma (float): _description_
        n (int): _description_

    Returns:
        np.array: an array of damage for each floor
    """
    M = np.random.binomial(1, p, size=n)
    L = np.random.normal(mu, sigma, size=n)
    
    X = M*L
    
    return X

