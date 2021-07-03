import pandas as pd
import numpy as np

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
        battle = Battle(combatants, verbose=False)
        result = battle.start_fight()
        winners.append(result['winning_faction'])
    s = pd.Series(winners)

    count = 0
    try:
        count = s.value_counts().loc[faction]
    except KeyError:
        pass
    return count


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    red_team = mob_factory(ZOMBIE, 5)
    blue_team = mob_factory(COMMONER, 15)
    print(count_wins(COMMONER['faction'], 2, red_team + blue_team))

