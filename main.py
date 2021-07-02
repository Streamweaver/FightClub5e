from mobs import BUGBEAR, COMMONER, SKELETON, ZOMBIE, VETERAN
from combat import Battle
from entity import mob_factory, UndeadForitude


def get_fighters(m_data, m_num, c_data, c_num):
    monsters = mob_factory(m_data, m_num)
    commoners = mob_factory(c_data, c_num)
    return monsters + commoners

def monster_attack(m_data, m_num, c_data, c_num):
    battle = Battle(get_fighters(m_data, m_num, c_data, c_num))
    battle.start_fight()


def bugbear_attack(n_bugbear, n_commoners):
    monster_attack(BUGBEAR, n_bugbear, COMMONER, n_commoners)


def skeleton_attack(n_skeleton, n_commoners):
    monster_attack(SKELETON, n_skeleton, COMMONER, n_commoners)

def zombie_attack(n_zombies, n_commoners):
    monster_attack(ZOMBIE, n_zombies, COMMONER, n_commoners)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    monster_attack(ZOMBIE, 25, VETERAN, 5)

