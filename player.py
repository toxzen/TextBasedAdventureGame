import items
import world
from random import randint

class Player:
    def __init__(self):
        self.inventory = [items.Rock(),
                          items.Dagger(),
                          items.CrustyBread(),
                          items.ChestPlate()]

        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.gold = 5
        self.victory = False


    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print('* ' + str(item))
        print("Gold: {}".format(self.gold))
        best_weapon = self.most_powerful_weapon()
        print('You are currently wielding a {}'.format(best_weapon))
        best_armor = self.most_powerful_armor()
        print('You are currently wearing a {}'.format(best_armor))
        print('Your current hp is {}'.format(self.hp))

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                  best_weapon = item
                  max_damage = item.damage
            except AttributeError:
                pass

        return best_weapon

    def most_powerful_armor(self):
        max_health = 0
        best_armor = None
        for armor in self.inventory:
            try:
                if armor.hp > max_health:
                  best_armor = armor
                  max_health = armor.hp
            except AttributeError:
                pass

        self.hp = self.hp + best_armor.hp

        return best_armor



    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print("You use {} against {} and do {} damage!".format(best_weapon.name,
                                                               enemy.name,
                                                               best_weapon.damage))

        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any items to heal you!")
            return

        for i, item in enumerate(consumables, 1):
            print("Choose an item to use to heal: ")
            print("{}. {}".format(i, item))

        valid = False
        while not valid:
            choice = input("")
            try:
                to_eat = consumables[int(choice) - 1]
                self.hp = min(self.hp, self.hp + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("Current HP: {}".format(self.hp))
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again. ")


    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print(self.x, '', self.y)


    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
