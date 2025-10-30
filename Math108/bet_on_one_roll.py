import numpy as np

def bet_on_one_roll():
    # x = np.random.choice(np.arange(1,7))
    x = 3
    if x<= 2:
        return -1
    elif x <= 4:
        return 0
    else:
        return 1

print(bet_on_one_roll())