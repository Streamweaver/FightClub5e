import numpy as np

def roll(d, num, is_crit=False):
    """
    Simulates a total dice roll for num of d
    :param d: int of sides of dice.
    :param num: int of number of fice
    :param is_crit: bool to set critical.
    :return: 
    """
    if is_crit:
        num = num * 2
    result = [np.random.randint(1, d+1) for _ in range(num)]
    return sum(result)
