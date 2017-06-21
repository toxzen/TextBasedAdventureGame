from random import randint

class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self):
        return self.name

class Rock(Weapon):
    def __init__(self):
        self.name = 'Rock'
        self.description = 'A fist-sized rock, suitable for bludgeoning.'
        self.damage = randint(3, 7)
        self.value = 1

class Dagger(Weapon):
    def __init__(self):
        self.name = "Dagger"
        self.description = "A small dagger with some rust. " \
                           "Somewhat more dangerous than a rock."
        self.damage = randint(7, 12)
        self.value = 20


class BroadSword(Weapon):
    def __init__(self):
        self.name = "BroadSword"
        self.description = "A large BroadSword with some rust. " \
                           "Much more dangerous than a rock."
        self.damage = randint(30, 50)
        self.value = 200

class Consumable():
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)

class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing_value = 10
        self.value = 12

class RedApple(Consumable):
    def __init__(self):
        self.name = "Red Apple"
        self.healing_value = 15
        self.value = 16

class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Healing Potion"
        self.healing_value = 50
        self.value = 60

class Armor():
    def __init__(self):
        raise NotImplementedError("Do not create raw Armor objects.")

    def __str__(self):
        return self.name

class ChestPlate(Armor):
    def __init__(self):
        self.name = "Chest Plate"
        self.hp = 100
        self.value = 60
