from entity import Size, Attack, DamageType, AbilityType

BUGBEAR = {
    'ac': 16,
    'max_hp': 27,
    'size': Size.MEDIUM,
    # 'attack': Attack('Morningstar', 2, 8, 2, DamageType.PIERCING),
    'attacks': [
        Attack('Morningstar', 2, 8, 2, DamageType.PIERCING),
    ],
    'name': 'Bugbear',
    'faction': 'monster',
    'abilities': {'str': 15, 'dex': 14, 'con': 13, 'int': 8, 'wis': 11, 'cha': 9}
}

SKELETON = {
    'ac': 13,
    'max_hp': 13,
    'size': Size.MEDIUM,
    'attacks': [Attack('Shortsword', 1, 6, 2, DamageType.PIERCING, AbilityType.DEX), ],
    'name': 'Skeleton',
    'faction': 'monster',
    'abilities': {'str': 10, 'dex': 14, 'con': 15, 'int': 6, 'wis': 8, 'cha': 5}
}

ZOMBIE = {
    'ac': 8,
    'max_hp': 22,
    'size': Size.MEDIUM,
    'attacks': [Attack('Slam', 1, 6, 1, DamageType.BLUDGEONING), ],
    'name': 'Zombie',
    'faction': 'monster',
    'abilities': {'str': 13, 'dex': 6, 'con': 16, 'int': 3, 'wis': 6, 'cha': 5}
}

GOBLIN = {
    'ac': 15,
    'max_hp': 7,
    'size': Size.SMALL,
    'attacks': [Attack('Scimitar', 1, 6, 2, DamageType.SLASHING, AbilityType.DEX), ],
    'name': 'Goblin',
    'faction': 'monster',
    'abilities': {'str': 8, 'dex': 14, 'con': 10, 'int': 10, 'wis': 8, 'cha': 8}
}

LIZARDFOLK = {
    'ac': 15,
    'max_hp': 22,
    'size': Size.MEDIUM,
    'attacks': [
        Attack('Heavy Club', 1, 8, 3, DamageType.BLUDGEONING),
        Attack('Spiked Shield', 1, 8, 3, DamageType.PIERCING)
    ],
    'name': 'Lizardfolk',
    'faction': 'monster',
    'abilities': {'str': 15, 'dex': 10, 'con': 13, 'int': 7, 'wis': 12, 'cha': 7}
}

# Villagers

COMMONER = {
    'ac': 10,
    'max_hp': 4,
    'size': Size.MEDIUM,
    'attacks': [Attack('Club', 1, 6, 0, DamageType.BLUDGEONING),],
    'name': 'Commoner',
    'faction': 'villager',
}

VETERAN = {
    'ac': 17,
    'max_hp': 58,
    'size': Size.MEDIUM,
    'attacks': [
        Attack('Longsword', 1, 8, 3, DamageType.SLASHING),
        Attack('Longsword', 1, 8, 3, DamageType.SLASHING),
        Attack('Shortsword', 1, 6, 3, DamageType.SLASHING),
    ],
    'name': 'Veteran',
    'faction': 'villager',
    'abilities': {'str': 16, 'dex': 13, 'con': 14, 'int': 10, 'wis': 11, 'cha': 10}
}

GUARD = {
    'ac': 16,
    'max_hp': 11,
    'size': Size.MEDIUM,
    'attacks': [
        Attack('Spear', 1, 6, 1, DamageType.SLASHING),
    ],
    'name': 'Guard',
    'faction': 'villager',
    'abilities': {'str': 13, 'dex': 12, 'con': 12, 'int': 10, 'wis': 11, 'cha': 10}
}