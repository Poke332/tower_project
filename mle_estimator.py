import numpy as np
import json
import math
from tower import generate_tower

def mle(damage_array):
    """
    X = 0 with prob (1-p)
    X ~ N(mu, sigma^2) with prob p
    """
    damage_array = np.array(damage_array)
    n = len(damage_array)
    
    nonzero_dmg = damage_array[damage_array != 0]
    n1 = len(nonzero_dmg)
    
    # MLE estimates
    p_hat = n1 / n

    if n1 > 0:
        mu_hat = np.mean(nonzero_dmg)
        sigma2_hat = np.mean((nonzero_dmg - mu_hat)**2)  # divide by n1 (MLE)
    else:
        mu_hat = 0
        sigma2_hat = 0

    return p_hat, mu_hat, sigma2_hat

if __name__ == "__main__":
    with open("config\\mle_param.json", "r") as file:
        param = json.load(file)
        
    X = generate_tower(**param, n=20)
    p_hat, mu_hat, sigma2_hat = mle(X)
    
    print(f"p_MLE: {p_hat}")
    print(f"mu_MLE: {mu_hat}")
    print(f"sigma_MLE: {math.sqrt(sigma2_hat)}")
    print(f"sigma2_MLE: {sigma2_hat}")
    
    print(f"Estimation Error: {abs(mu_hat-param["mu"])}")