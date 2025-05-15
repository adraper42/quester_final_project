class Party:
    """Stores the characters who are adventuring with the player"""

    def __init__(self,PC):
        """Must have a Player passed to it to be initialized, there can be no party without a player..."""
        self.player = PC
        self.members = [PC]
        self.members_with_names = {} #for id'ing party members easier,
                                     #PC never needs to be found from a string (inputted by user)

    def add_member(self,member):
        """Adds the passed member to the party"""
        #necessary because of the dict
        self.members.append(member)
        self.members_with_names[member.name.split()[0]] = member #id's by first name only,
                                        #because when a user tries to find a character, full name input is not guaranteed

    def remove_player(self,member):
        """Removes the player from the party. Never to be seen again
        Will only be called in case of a character's death by the program, so member is an object"""
        self.members.remove(member)
        del self.members_with_names[member.name.split()[0]]

    def find_player(self):
        """Returns player for an NPC to talk to"""
        #PC would always initiate talking and that's why find_member exists... they do not have autonomy why did i write this function... todo:deletethisfunction
        return self.player
    
    def find_member(self,member_name):
        """Given a name the user has input, find the NPC with the corresponding name.
        Only first names necessary, strings, 'Tina Dongus' would return a Tina Flower
        but there are no duplicates so it will never return a different member than expected if the first name is correct.
        Returns None if there is no corresponding member."""
        member_name = member_name.split()[0].title()
        if member_name in self.members_with_names.values():
            return self.members_with_names.get(member_name)
        else:
            return None
    
    def get_party(self):
        """Returns the list of members in the party"""
        return self.members