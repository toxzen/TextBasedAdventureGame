class Enemy:
    def __init__(self):
        raise NotImplementedError('Do not create raw Enemy objects.')

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0

class GiantSpider(Enemy):
    def __init__(self):
        self.name = "Giant Spider"
        self.hp = 10
        self.damage = 2

class Ogre(Enemy):
    def __init__(self):
        self.name = "Ogre"
        self.hp = 30
        self.damage = 10

class BatColony(Enemy):
    def __init__(self):
        self.name = "Colony of bats"
        self.hp = 15
        self.damage = 4

class StoneGolem(Enemy):
    def __init__(self):
        self.name = "Stone Golem"
        self.hp = 80
        self.damage = 15

class Dragon(Enemy):
    def __init__(self):
        self.name = "Dragon"
        self.hp = 40
        self.damage = 10
