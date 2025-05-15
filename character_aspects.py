BACKSTORIES = ["I grew up a carpenter. I liked carving statues, but I could never bring myself to carve the same one twice. I had a full, loving family. One day, I went to the tavern and discovered an opening for a quest. I had only just decided to become and adventurer when I met you.",
               "I was born in a remote desert. I was raised by a pack of coyotes. I loved my coyote family, and they taught me how to live with the earth. I now travel the world, documenting - and appreciating - nature.",
               "Growing up, I really liked oranges. I grew up in an orange grove, isolated from the real world. I never knew what the real world was like until I was quite old. I started adventuring to see the world and have excitement in my life.",
               "I have always been a people person :). I have many friends back home. Ever since I was little, I have been training to be a warrior. When I was little, my town was destroyed by a horde of evil creatures. I like adventuring to fight off all the evils and protect my fellow citizens.",
               "I used to be a detective. I would travel around nearby towns, solving mysteries and crimes. I loved solving mysteries, but the townspeople eventually grew distrustful of me. I joined you to keep solving puzzles while avoiding the wrath of my neighbors. I secretly want to find out what happened to make my old townmates hate me so much.",
               "I am a humble candlemaker. I have made candles for nearly 2 decades and sold them for 13 years. Back in my hometown, I have a shop. My nephew will look after my shop while I'm gone. When I saw you, I was so inspired by your bravery that I decided to join you for a while."]

class Species:
    """The species that a character is, subclasses of which are to be stored and accessed by them for stat upgrades."""

    name = "Species"
    description = ""
    base_attack = 1
    base_hp = 1
    base_magic = 0
    backstories = BACKSTORIES
    #could always use more

class Human(Species):
    """A subclass of Species, a human is a persistence hunter ironically most known for being conquerors of foreign lands."""
    #there is not much to say here, i did not know what to put... Woe, ~lore~ be upon ye

    name = "Human"
    description = "A persistence hunter and intelligent species, you know what a human is."
    base_attack = 0
    base_hp = 2
    base_magic = 0
    backstories = Species.backstories #MUST be changed if parent class changes/name changes etc. sorry.

class Type:
    """The fighting style that a character uses, subclasses of which are to be stored and accessed by them for stat upgrades."""

    name = "Type"
    description = ""
    base_attack = 1
    base_hp = 1
    base_magic = 0
    backstories = BACKSTORIES

class Rogue(Type):
    """A subclass of Type, a rogue is a sneaky thief who prefers stealth and surprise."""

    name = "Rogue"
    description = "Rogues are sneaky, favoring close combat, stealth, and surprise. They are most often thiefs."
    base_attack = 2
    base_hp = 0
    base_magic = 0
    backstories = Type.backstories #MUST be changed if parent class changes/name changes etc. sorry again.
