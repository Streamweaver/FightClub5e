from mobs import BUGBEAR, COMMONER
from combat import Battle
from entity import mob_factory


def bugbear_attack(n_bugbear, n_commoners):
    bugbears = mob_factory(BUGBEAR, n_bugbear)
    commoners = mob_factory(COMMONER, n_commoners)
    battle = Battle(bugbears + commoners)
    battle.start_fight()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bugbear_attack(12, 400)

