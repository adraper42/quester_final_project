from character_creation import Character
import random

##########TODO
#NEED TO REDO ACTIONS...

class Item:
    """The blueprint for things a Player can find in environments and pick up and use.
    Has an identifying name(class var)
    and an action method to carry out the action of the item.
    All subclasses will be representations of different items and have a name(class var),
    an action method(each one will do something specific to the item),
    and possibly instance attributes that will not be accessed by outsiders."""
    name = "Item"
    def __init__(self,env):
        self.environment = env
    def action(self):
        return True
    def add_to_inventory(self):
        print(f"You have obtained a {self.name}!")
        self.environment.player.add_to_inventory(self)
        self.environment.remove_item(self)

class Torch(Item):
    """Reveals hidden deatils about an environment, especially dark places."""
    name = "Torch"
    def __init__(self,env):
        super().__init__(env)
        self.fuel = 10
    def action(self):
        self.fuel -= 1
        print("You turn the light on so you can see better.")
        self.environment.inspect()
        if self.fuel == 0:
            self.player.remove_from_inventory(self)
        
class Key(Item):
    """Opens secret doors, chests, etc., unlocking treasure or more places to explore."""
    name = "Key" 
    def action(self):
        print("You turn the key into the lock.")
        if self.environment.unlock(): #returns true if successfully unlocked
            self.player.remove_from_inventory(self)
        else:
            print("That doesn't do anything here.")

class Enemy:
    """A primitive creature that can engage in battle with the Player and party.
    Its type, maximum hp, and attack are the same for all objects of the class, but change with the type of enemy (represented by subclasses).
    Name and position depend on the instance and current_hp changes during runtime."""

    creature = "Enemy"
    max_hp = 12
    attack_stat = 6

    def __init__(self,position):
        self.name = Character.generate_name().split(" ")[0]
        self.current_hp = self.max_hp
        self.position = position
    
    def attack(self):
        return self.attack_stat

    def is_hurt(self,damage_taken):
        self.current_hp -= damage_taken
        if self.current_hp <= 0:
            return self.die()

    def die(self):
        return True

    def fight(self):
        return self.attack() #incase there ever needs to be a more advanced enemy
                             #that can heal or some other action

class Goblin(Enemy):

    creature = "Goblin"
    max_hp = 7
    attack_stat = 3

class Dragon(Enemy):

    creature = "Dragon"
    max_hp = 100
    attack_stat = 15

    def attack(self):
        if random.randint(1,5) == 5:
            return self.attack_stat + random.randint(-3,3)
        else:
            return super().attack()
