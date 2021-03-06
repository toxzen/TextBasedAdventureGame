import random
import enemies
import npc
import items
from collections import OrderedDict

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError('Create a subclass instead!')

    def modify_player(self, player):
        pass



class StartTile(MapTile):
    def intro_text(self):
        return """
        You find yourself in a forest with a flickering torch in hand.
        You can make out for paths, each equally as dark and foreboding.
        """

class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x,y)

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("invalid choice!")

    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Trade complete!")

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Here's what is available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("invalid choice!")

    def intro_text(self):
        return """
        A frail not-quite-human, not-quite-creature squats in the corner
        clinking his gold coins together.  He looks willing to trade.
        """

class BossTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.plunder_claimed = False
        self.sword = items.BroadSword()
        self.enemy = enemies.Dragon()
        self.alive_text = "A huge dragon steps from out the trees. " \
                          "It gives a deafening roar!"

        self.dead_text = "The stinking carcass of a dead dragon " \
                         "fills the air of the forest."



        super().__init__(x,y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text

        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage.  You have {} HP remaining.".
                  format(self.enemy.damage, player.hp))
        # ClAIM PLUNDER
        else:
            if not self.plunder_claimed:
                self.plunder_claimed = True
                player.gold = player.gold + self.gold
                print('You plundered {} gold from the dragon!'.format(self.gold))
                self.sword = player.inventory.append(self.sword)
                print('You recieved a Broadsword!')




class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from " \
                              "its web in front of you!"
            self.dead_text = "The corpse of a dead spider " \
                             "rots on the ground."
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An ogre is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumph."
        elif r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squaking noise growing louder" \
                              "...suddenly you are lost in a swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground."
        else:
            self.enemy = enemies.StoneGolem()
            self.alive_text = "You've disturbed a stone golem " \
                              " from his slumber!"
            self.dead_text = "Defeated, the golem has reverted " \
                             "into an ordinary rock."

        super().__init__(x,y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage.  You have {} HP remaining.".
                  format(self.enemy.damage, player.hp))

class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print('+{} gold added.'.format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """
            Another unremarkable part of the forest.  You must forge onwards.
            """
        else:
            return """
            Someone dropped some gold.  You pick it up.
            """

class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer!  An open valley appears.
        You found your way from out of the forest.

        Victory is yours!
        """




# world_map = [
#     [None, VictoryTile(1,0), None],
#     [None, EnemyTile(1,1), None],
#     [EnemyTile(0,2), StartTile(1,2), EnemyTile(2,2)],
#     [None, EnemyTile(1,3), None]
# ]

world_map = []

def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    return True

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
                  "BB": BossTile,
                  " ": None}

start_tile_location = None

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)

world_dsl = """
|EN|FG|FG|EN|EN|EN|EN|
|EN|FG|FG|EN|EN|BB|EN|
|EN|EN|VT|EN|EN|TT|EN|
|EN|FG|FG|EN|EN|EN|EN|
|EN|FG|EN|EN|TT|FG|EN|
|TT|BB|ST|FG|EN|FG|EN|
|FG|EN|EN|EN|FG|FG|EN|
"""



def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
