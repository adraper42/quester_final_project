import random
from environments import *


class Map:
    """Generates a random square grid of Environments.
    Random size and Environment subclasses"""

    sizes = [9,12,15,18,21,24] # List of all possible sizes of the map, square (same length and width), all multiples of 3
                               #could automate this probably... [x*3 for x in range()]... but IDC

    def __init__(self):
        """Randomly generates a random map/grid of Environments"""
        self.map = [] #is this a good var name???
        self.size = random.choice(Map.sizes)
        for row in range(self.size):
            self.map.append([])
            for column in range(self.size): #column could be _ but i'm keeping it in this ONE INSTANCE to denote the x and y organization of the grid
                self.map[row].append(random.choice(Environment.__subclasses__())())
        for row in self.map:
            for env in row:
                env.add_map(self)

    def get_north(self,env):
        """Returns the Environment to the north of the passed Environment,
        None if there isn't one"""
        for row in range(self.size):
            for column in range(self.size):
                if self.map[row][column] == env:
                    if row == 0:
                        return None
                    else:
                        return self.map[row-1][column]
                    
    def get_east(self,env):
        """Returns the Environment to the east of the passed Environment,
        None if there isn't one"""
        for row in range(self.size):
            for column in range(self.size):
                if self.map[row][column] == env:
                    if column == self.size - 1:
                        return None
                    else:
                        return self.map[row][column+1]
                    
    def get_south(self,env):
        """Returns the Environment to the south of the passed Environment,
        None if there isn't one"""
        for row in range(self.size):
            for column in range(self.size):
                if self.map[row][column] == env:
                    if row == self.size - 1:
                        return None
                    else:
                        return self.map[row+1][column]
                    
    def get_west(self,env):
        """Returns the Environment to the west of the passed Environment,
        None if there isn't one"""
        for row in range(self.size):
            for column in range(self.size):
                if self.map[row][column] == env:
                    if column == 0:
                        return None
                    else:
                        return self.map[row][column-1]     
                    
    def move_player(self,new_env):
        """Finds where the Player is in the map and moves them to the new passed Environment"""
        for row in range(self.size):
            for column in range(self.size):
                if self.map[row][column].player:
                    player = self.map[row][column].remove_player()
        new_env.add_player(player)
        player.environment = new_env #sorry for disparity this is last minute addition bc i did some dumb code
        player.game.current_env = new_env
    
    def place(self,player):
        """Places the passed Player at a random spot in the map upon game start"""
        i1 = random.randint(0,self.size-1)
        i2 = random.randint(0,self.size-1)
        new_env = self.map[i1][i2]
        new_env.add_player(player)
        player.environment = new_env
        return new_env
    
    def debug(self):
        colors = {Tundra : "⬜",
            Desert : "🟧",
            Forest : "🟩",
            Plains : "🟨",
            Town : "⬛"} 
        for row in self.map:
            for place in row:
                if place.player:
                    print("U ",end="")
                else:
                    print(colors.get(type(place)),end="")
            print()
        
                    
class BiomeMap(Map):
    """Small, functionally-methodless map used as a template for an AdvancedMap"""

    size = 3 #set size

    def __init__(self):
        """Generates a random 3x3 grid of Environment subclasses (not initialized)"""
        self.map = []
        for row in range(self.size):
            self.map.append([])
            for _ in range(self.size):
                self.map[row].append(random.choice(Environment.__subclasses__()))

class AdvancedMap(Map):
    """Based on a passed BiomeMap, creates a larger map with some border scattering"""

    def __init__(self,biome_map):
        """Scales up the BiomeMap and introduces random scattering at the edges"""
        self.biome_map_object = biome_map
        self.map = []
        self.size = random.choice(self.sizes)
        self.scale = int(self.size / self.biome_map_object.size)
        for row in range(self.size):
            self.map.append([])
            for column in range(self.size):
                biome_row = row // self.scale
                if biome_row != biome_map.size - 1 and (row + 1) // self.scale != biome_row:
                    if self.scale <= 3:
                        if random.randint(1,4) == 4:
                            biome_row += 1
                    else:
                        if random.randint(1,2) == 1:
                            biome_row += 1
                elif biome_row != 0 and (row - 1) // self.scale != biome_row:
                    if self.scale <= 3:
                        if random.randint(1,4) == 4:
                            biome_row -= 1
                    else:
                        if random.randint(1,2) == 1:
                            biome_row -= 1
                biome_column = column // self.scale
                if biome_column != biome_map.size - 1 and (column + 1) // self.scale != biome_column:
                    if self.scale <= 3:
                        if random.randint(1,4) == 4:
                            biome_column += 1
                    else:
                        if random.randint(1,2) == 1:
                            biome_column += 1
                elif biome_column != 0 and (column - 1) // self.scale != biome_column:
                    if self.scale <= 3:
                        if random.randint(1,4) == 4:
                            biome_column -= 1
                    else:
                        if random.randint(1,2) == 1:
                            biome_column -= 1
                new_env_type = biome_map.map[biome_row][biome_column]
                self.map[row].append(new_env_type())
        for row in self.map:
            for env in row:
                env.add_map(self)
