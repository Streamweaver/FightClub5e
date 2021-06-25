from entity import Size, Attack, DamageType

BUGBEAR = {
    'ac': 16,
    'max_hp': 27,
    'size': Size.MEDIUM,
    'attack': Attack('Morningstar', 2, 8, 2, DamageType.PIERCING),
    'name': 'Bugbear',
    'faction': 'monster',
    # 'type': 'Bugbear'
}

COMMONER = {
    'ac': 10,
    'max_hp': 4,
    'size': Size.MEDIUM,
    'attack': Attack('Club', 1, 6, 0, DamageType.BLUDGEONING),
    'name': 'Commoner',
    'faction': 'villager',
    # 'type': 'Commoner'
}

