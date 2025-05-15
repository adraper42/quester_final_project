import random , math
from character_aspects import *
from party import Party

class Character:
    """The base template for any character in the game,
    to be used only for NPCs (for player characters, see Player subclass),
    generates as a randomly generated character when instantiated.
    Names are used as identifiers for characters, but duplicates CAN be created and MUST be checked later
    with a Party object and the change_name() method."""

    CONSONANTS = "B C D F G H J K L M N P Q R S T V W X Y Z".split()
    VOWELS = "A E I O U Y".split()
    ALPHABET = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
    #conversation choices for npcs...
    PERSONALITIES = [["My favorite fruit is oranges.","Have you heard the story about the jackrabbit and the fly? I always liked that one.","I'm really liking the sunlight today.","Now would be a great time for some crafts.","I'm really enjoying spending time with you.","I admire your courageousness.","I've always liked the plains.","My mother must be waiting for a letter... I should write her."],
                     []]

    def __init__(self,env=None):
        """Generates a random character. No inputs.
        name = random and an ID, species and type are subclasses of Species and Type,
        level and xp and needed_xp and friendliness and action are set to defaults,
        attack_stat and magic_stat and max_h and backstory are random based on species and type,
        current_hp is set to default based on max_hp, party is set to None to be added later when the NPC joins the party"""
        self.name = Character.generate_name()
        self.species = random.choice(Species.__subclasses__())
        self.type = random.choice(Type.__subclasses__())
        self.level = 1
        self.xp = 0
        self.needed_xp = int(50 * math.sqrt(self.level * 1.5))
        self.attack_stat = random.randint(1,6) + self.type.base_attack + self.species.base_attack
        self.magic_stat = random.randint(1,6) + self.type.base_magic + self.species.base_magic
        self.max_hp = random.randint(7,12) + self.type.base_hp + self.species.base_hp
        self.current_hp = self.max_hp
        self.backstory = random.choice(self.species.backstories + self.type.backstories)
        self.actions = ["attack","heal","talk"]

        self.friendliness = random.randint(1,3) #score out of 10 of how close their bond is with player
                                                # - mainly affects dialogue choices
                                                # - set random to simulate innate friendliness vs. loneliness (personality)
        self.conversation_choices = random.choice(Character.PERSONALITIES)
        self.party = None #Party object of current game
        self.environment = env

    def level_up(self):
        """Adds 1 to level, fixes the needed xp stat automatically, and gets user input to increase a stat every 3rd level"""
        self.level += 1
        self.xp = 0
        self.needed_xp = int(50 * math.sqrt(self.level * 1.5))
        print(f"You have leveled up! You are now level {self.level}.")
        if self.level % 3 == 0:
            while True:
                print(f"You can increase one of your stats!\nattack: {self.attack_stat}\nmagic: {self.magic_stat}\nhp: {self.max_hp}")
                choice = input("Which stat would you like to increase?\n> ").lower()
                if choice in ["magic","attack","hp"]:
                    if choice == "hp":
                        self.max_hp += 1
                    elif choice == "magic":
                        self.magic_stat += 1
                    else:
                        self.attack_stat += 1
                    break

    def gain_xp(self,xp_gained):
        """Adds xp and levels up if needed"""
        self.xp += xp_gained
        extra_xp = self.xp - self.needed_xp
        if extra_xp >= 0:
            self.level_up()
            self.gain_xp(extra_xp) #technically recursive but should not run more than two times from one call

    def attack(self):
        """Returns the damage it deals"""
        if self.attack_stat + 5 <= self.magic_stat:
            return self.magic_stat
        return self.attack_stat
    
    def heal(self):
        """Automatically heals self"""
        self.current_hp += self.magic_stat
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def is_hurt(self,damage_taken):
        """Subtracts damage from self, dies if hp goes below 0"""
        self.current_hp -= damage_taken
        if self.current_hp <= 0:
            return self.die()

    def die(self):
        """everytime is_hurt() is called, it must be checked whether it returns True or not, death conditions to be figured out"""
        return True

    def fight(self):
        """Automatically decides what to do in a fight and acts"""
        if self.current_hp <= 5 and random.randint(1,2) == 1:
            self.heal()
        else:
            return self.attack()
        
    def talk(self):
        if not self.party:
            if input(f"\"Hello! My name is {self.name} and I would like to join your party!\"\nWill you let them join your party?\n> ").lower()[0] == "y":
                self.environment.add_NPC_to_party()
                return
        if self.friendliness == 10 and random.randint(1,3) == 1:
            print(self.backstory)
        else:
            for _ in range(math.ceil(self.friendliness/2)):
                print(random.choice(self.backstory.split() + self.conversation_choices))
            if self.friendliness < 10:
                self.friendliness += 0.25

    def change_name(self):
        """Used when checking if party member has same first name"""
        self.name = Character.generate_name()

    def generate_name():
        """Generates a random full name for a character"""
        syllables = random.choices([2,3,4],weights=[3,2,1])[0]
        first_name = ""
        for _ in range(syllables):
            new_letter = random.choice(Character.ALPHABET)
            if new_letter not in Character.VOWELS:
                first_name += new_letter + random.choice(Character.VOWELS)
            else:
                first_name += new_letter
        if random.randint(1,10) != 10:
            first_name += random.choice(Character.CONSONANTS)
        first_name = first_name.title()

        syllables = random.choices([2,3,4],weights=[1,3,2])[0]
        last_name = ""
        for _ in range(syllables):
            new_letter = random.choice(Character.ALPHABET)
            if new_letter not in Character.VOWELS:
                last_name += new_letter + random.choice(Character.VOWELS)
            else:
                last_name += new_letter
        if random.randint(1,10) != 10:
            last_name += random.choice(Character.CONSONANTS)
        last_name = last_name.title()

        if random.randint(1,5) == 5:
            middle_name = ""
            syllables = random.choices([1,2],weights=[1,2])[0]
            for _ in range(syllables):
                new_letter = random.choice(Character.ALPHABET)
                if new_letter not in Character.VOWELS:
                    middle_name += new_letter + random.choice(Character.VOWELS)
                else:
                    middle_name += new_letter
            if random.randint(1,2) != 2:
                middle_name += random.choice(Character.CONSONANTS)
            middle_name = middle_name.title()
            full_name = " ".join([first_name,middle_name,last_name])
        else:
            full_name = " ".join([first_name,last_name])

        return full_name


class Player(Character):
    """The base template for the one player character in the game,
    to be used only for the user, takes user input to create a player upon instantiation."""

    def __init__(self,game_instance):
        """Tkaes user input to create the player character. Takes a Game object to be able to refer to map etc.
        name, species, and type are gotten from user or randomly generated,
        level, xp, needed_xp, actions, and combat_actions are set to defaults,
        attack_stat, magic_stat, and max_hp and backstory are assigned by user and ajdusted based on species and type,
        current_hp is set to default based on max_hp, party is generated by the player as it needs a Player"""
        #ask for name, species, type
        self.game = game_instance
        self.level = 1
        self.xp = 0
        self.needed_xp = int(50 * math.sqrt(self.level * 1.5))
        self.inventory = []
        self.money = 0
        self.combat_actions = {"attack":self.attack,"heal":self.heal,"actions":lambda g = None : print("You can:"+self.combat_actions.keys()+"\n")}
        self.eternal_actions = {"help" : self.game.print_help , "pause" : self.game.pause_menu , "actions" : self.print_actions , "inventory" : self.print_inventory}
            # actions available to the user while in combat, also do not count as a choice/turn in combat
        self.actions = {}
        self.environment = None

        while True:
            print("What will your character be named? (Enter \"RANDOM\" to get a randomly generated name.)")
            new_name = input("> ")
            if new_name == "RANDOM":
                new_name = Character.generate_name()
            print(f"Your character will be named {new_name}. Is this correct?")
            if input("> ").upper().strip()[0] == "Y":
                print("Great!\n")
                break
        self.name = new_name

        while True:
            print(f"What species will {self.name} be? (Enter \"RANDOM\" to get a randomly generated species.)")
            species_dict = {}
            for subspecies in Species.__subclasses__():
                species_dict[subspecies.name] = subspecies
            print(f"List of species:")
            for species_name in species_dict.keys():
                print(f"{species_name} - {species_dict.get(species_name).description}")
            new_species = input("> ")
            if new_species == "RANDOM":
                new_species = random.choice(Species.__subclasses__())
                print(f"Your character will be a {new_species.name}. Is this okay?")
                if input("> ").upper().strip()[0] == "Y":
                    print("Great!\n")
                    break
            elif new_species.title() in species_dict.keys():
                new_species = species_dict.get(new_species.title())
                print(f"Your character will be a {new_species.name}. Is this okay?")
                if input("> ").upper().strip()[0] == "Y":
                    print("Great!\n")
                    break
            else:
                print("Sorry, that isn't a species.")
        self.species = new_species

        while True:
            print(f"What type will {self.name} be? (Enter \"RANDOM\" to get a randomly generated type.)")
            type_dict = {}
            for subtype in Type.__subclasses__():
                type_dict[subtype.name] = subtype
            print(f"List of types:")
            for type_name in type_dict.keys():
                print(f"{type_name} - {type_dict.get(type_name).description}")
            new_type = input("> ")
            if new_type == "RANDOM":
                new_type = random.choice(Type.__subclasses__())
                print(f"Your character will be a {new_type.name}. Is this okay?")
                if input("> ").upper().strip()[0] == "Y":
                    print("Great!\n")
                    break
            elif new_type.title() in type_dict.keys():
                new_type = type_dict.get(new_type.title())
                print(f"Your character will be a {new_type.name}. Is this okay?")
                if input("> ").upper().strip()[0] == "Y":
                    print("Great!\n")
                    break
            else:
                print("Sorry, that isn't a type.")
        self.type = new_type

        print("Would you like to distribute your stats randomly or distribute them yourself?") #stats a random d6 and can be assigned in any order
        choice = input("> ").strip().lower()
        try:
            if choice[0:6] == "random":
                self.attack_stat = random.randint(1,6) + self.type.base_attack + self.species.base_attack
                self.magic_stat = random.randint(1,6) + self.type.base_magic + self.species.base_magic
                self.max_hp = random.randint(7,12) + self.type.base_hp + self.species.base_hp
                self.current_hp = self.max_hp
            else:
                pass
        except IndexError:
            pass
        try:
            self.max_hp
        except AttributeError:
            random_numbers = [random.randint(1,6) for _ in range(3)]
            print(f"You can allot the numbers {random_numbers[0]}, {random_numbers[1]}, and {random_numbers[2]} to attack, magic, and HP stats in whichever order you would like.")
            print(f"You will have {self.type.base_attack + self.species.base_attack} added to the number you choose for your attack stat, {self.type.base_magic + self.species.base_magic} added to the number you choose for your magic stat, and {self.type.base_hp + self.species.base_hp} plus six added to the number you choose for your HP.")
            while True:
                print("Which number would you like your attack stat to be?")
                num_choice = input("> ")
                try:
                    num_choice = int(num_choice)
                    if num_choice in random_numbers:
                        random_numbers.remove(num_choice)
                        self.attack_stat = num_choice + self.type.base_attack + self.species.base_attack
                        break
                    else:
                        print("Please input a number from the list.")
                except TypeError:
                    print("Please input a number from the list as it appears.")
            while True:
                print(f"Which number would you like your magic stat to be?\nThe numbers {random_numbers[0]} and {random_numbers[1]} are left.")
                num_choice = input("> ")
                try:
                    num_choice = int(num_choice)
                    if num_choice in random_numbers:
                        random_numbers.remove(num_choice)
                        self.magic_stat = num_choice + self.type.base_magic + self.species.base_magic
                        break
                    else:
                        print("Please input a number from the list.")
                except TypeError:
                    print("Please input a number from the list as it appears.")
            print(f"Your HP stat will be assigned {random_numbers[0]}.")
            self.max_hp = random_numbers[0] + 6 + self.type.base_hp + self.species.base_hp
            self.current_hp = self.max_hp
        print(f"\nYour final stats are:\nattack: {self.attack_stat}\nmagic: {self.magic_stat}\nHP: {self.max_hp}\n")
                    
        self.party = Party(self)

        print(f"You are {self.name}, a {self.species.name.lower()} {self.type.name.lower()} who is level {self.level} with {self.max_hp} HP, {self.attack_stat} attack, and {self.magic_stat} magic.\n")
        
    # def level_up(self):
    #     super().level_up()
    # def gain_xp(self,xp_gained):
    #     super().gain_xp(xp_gained)
    # def attack(self):
    #     return super().attack()
    # def heal(self):
    #     super().heal()
    # def is_hurt(self,damage_taken):
    #     super().is_hurt(damage_taken)
    # def die(self):
    #     return True

    #why... why did i have these..........

    def add_to_inventory(self,item_to_add):
        self.inventory.append(item_to_add)
        self.actions[item_to_add.name.lower()] = item_to_add.action
        print(f"{item_to_add.name.title()} has been added to your inventory!")
    
    def remove_from_inventory(self,item_to_remove):
        self.inventory.remove(item_to_remove)
        self.actions.remove(item_to_remove.name.lower())
        print(f"You have used up {item_to_remove.name.lower()} and it has been removed from your inventory.")

    def print_inventory(self):
        print("In your inventory, you have: ")
        for thing in self.inventory:
            print(thing.name.title())
    
    def fight(self,enemy_team):
        """Gets choice of what to do from the user and does that thing"""
        print(f"Your current hp is {self.current_hp}.  What would you like to do?")
        while True:
            choice = input("> ").lower().strip()
            if choice not in self.combat_actions.keys() or choice not in self.eternal_actions.keys():
                print("You cannot do that right now.")
                print(f"Your current hp is {self.current_hp}.  What would you like to do?")
            else:
                break
        if choice in self.eternal_actions.keys():
            if choice == "actions":
                self.print_actions(True) # don't know how to get around this
            else:
                self.eternal_actions.get(choice)()
        else:
            if choice == "attack":
                #they get to choose who to attack
                while True:
                    print("Which enemy do you want to attack?")
                    self.environment.print_combat_team(enemy_team)
                    num = input("> ")
                    try:
                        if int(num) >= 1 and int(num) <= len(enemy_team):
                            return (self.attack(),enemy_team[int(num)-1])
                    except ValueError:
                        print("Please input the number of the enemy you want to attack.")
            self.combat_actions.get(choice)()
            return

    def print_actions(self,combat=False):
        text = "You can: "
        if combat:
            for thing in self.combat_actions.keys():
                text += thing + ", "
            for thing in self.eternal_actions.keys():
                text += thing + ", "
        else:
            for thing in self.actions.keys():
                text += thing + ", "
            for thing in self.eternal_actions.keys():
                text += thing + ", "
            for thing in self.environment.actions.keys():
                text += thing + ", "
            text = text[:-2]
        print(text)