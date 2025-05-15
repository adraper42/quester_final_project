"""THIS FILE IS NOT REQUIRED FOR THE USER. I'M KEEPING IT AROUND IN CASE IT IS USEFUL LATER LOL."""
#and bcus it's pretty...

from maps import *
from environments import *

colors = {Tundra : "⬜",#🟦
          Desert : "🟧",
          Forest : "🟩",
          Plains : "🟨",
          Town : "⬛"}#⬜   

#formatted two at a time bcus vscode uses a default monospace font that seems to be exactly 1:2 character ratio
symbols = {Tundra : "**", #snow
          Desert : "~~", #sand dunes
          Forest : "||", #tree trunks
          Plains : ",,", #grass
          Town : "[]"} #buildings

def display_map(map_obj):
    for row in map_obj.map:
        for place in row:
            print(colors.get(type(place)),end="")
        print()

def display_biome_map(map_obj):
    for row in map_obj.map:
        for place in row:
            print(colors.get(place),end="")
        print()

def display_map2(map_obj):
    for row in map_obj.map:
        for place in row:
            print(symbols.get(type(place)),end="")
        print()

def display_biome_map2(map_obj):
    for row in map_obj.map:
        for place in row:
            print(symbols.get(place),end="")
        print()


b_map = BiomeMap()
display_biome_map(b_map)
print()
a_map = AdvancedMap(b_map)
display_map(a_map)
print()
display_biome_map2(b_map)
print()
display_map2(a_map)