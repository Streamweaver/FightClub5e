import pandas as pd
import numpy as np
from copy import deepcopy

from mobs import BUGBEAR, COMMONER, SKELETON, ZOMBIE, VETERAN
from combat import Battle
from entity import mob_factory


def get_fighters(m_data, m_num, c_data, c_num):
    monsters = mob_factory(m_data, m_num)
    commoners = mob_factory(c_data, c_num)
    return monsters + commoners


def monster_attack(m_data, m_num, c_data, c_num, verbose=True):
    battle = Battle(get_fighters(m_data, m_num, c_data, c_num), verbose)
    return battle.start_fight()


def bugbear_attack(n_bugbear, n_commoners):
    monster_attack(BUGBEAR, n_bugbear, COMMONER, n_commoners)


def skeleton_attack(n_skeleton, n_commoners):
    monster_attack(SKELETON, n_skeleton, COMMONER, n_commoners)


def zombie_attack(n_zombies, n_commoners):
    monster_attack(ZOMBIE, n_zombies, COMMONER, n_commoners)


def count_wins(faction, iterations, combatants):
    winners = []
    for _ in range(iterations):
        battle = Battle(deepcopy(combatants), verbose=False)
        result = battle.start_fight()
        winners.append(result['winning_faction'])
    s = pd.Series(winners)
    return s.value_counts(normalize=True).to_dict()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    max_zombies = 3
    max_commoners = 15
    for num_z in range(max_zombies):
        for num_c in range(max_commoners):
            red_team = mob_factory(ZOMBIE, max_zombies + 1)
            blue_team = mob_factory(COMMONER, max_zombies + 2)
            print(count_wins(COMMONER['faction'], 1000, red_team + blue_team))
            # TODO add all this to a list of dicts, write out to CSV.

