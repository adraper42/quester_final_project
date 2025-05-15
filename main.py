from character_creation import *
from maps import AdvancedMap , BiomeMap

class Main:
    """Provides and simulates the gameplay of the game."""

    def __init__(self):
        self.player = None
        self.party = None
        self.map = None
        self.current_env = None

    def header(self):
        """Displays header."""
        print("""             _________
            |         |
            | Quester |
            |_________|""")
        print("\nWelcome to Quester, the Coolest Game\n")
        
    def main_menu(self):
        """The main menu provided when no game is active."""
        print("-> New Game\n-> Continue\n-> Settings")
        while True:
            orig_choice = input("\nInput your choice > ")
            if orig_choice != "":
                choice = orig_choice.upper().strip()[0]
            if choice in ["N","C","S"]:
                if choice == "C" or choice == "S":
                    print("Sorry, this feature is not available right now. Try again later.")
                    #fix this eventually
                    # + it's in pause menu now
                elif "new" in orig_choice.lower().split() or "game" in orig_choice.lower().strip():
                    print()
                    break
                else:
                    print("Please input a valid choice.\n")
                    print("-> New Game\n-> Continue\n-> Settings")
            else:
                print("Please input a valid choice.\n")
                print("-> New Game\n-> Continue\n-> Settings")
        self.new_game()

    def start(self):
        """Runs the necessary functions to automatically start a gameplay loop. No other direct action is required from the user to run the full game."""
        self.header()
        self.main_menu()

    def new_game(self,file=None):
        """Clears all previous game data and replaces it with the correct data (pass no additional data for a new game, game file contents for a continued game)."""
        #should basically emulate __init__, then if second param, read file + replace data
        # ^orig. comment fix this its not entirely accruate
        self.player = Player(self)
        self.party = self.player.party
        self.map = AdvancedMap(BiomeMap())
        self.current_env = self.map.place(self.player)
        
        self.gameplay_loop() #<- runs at end of setup automatically

    def gameplay_loop(self):
        """Manipulates other classes to run the game."""
        ##########TODO - finished? but PLAYTESTING
        #heavily handles other materials to force gameplay
        pass
        while True:
            self.current_env.print()
            print("What would you like to do?")
            choice = input("> ").lower()
            #could build in typo recognition someday
            if choice in self.player.eternal_actions:
                self.player.eternal_actions.get(choice)()
            elif choice in self.player.actions:
                self.player.actions.get(choice)()
            elif choice in self.current_env.actions:
                self.current_env.actions.get(choice)()
            else:
                print("Please input a valid action, or type actions to see the available actions.")

    def print_help(self):
        print("This is a text-based game. You can enter a word at any time ot take an action, or you can enter \"actions\" to see your options. Please try to use as few words as possible.")

    def pause_menu(self):
        print("-> Continue\n-> Settings\n-> Exit Game")
        while True:
            choice = input("\nInput your choice > ").upper().strip()[0]
            if choice not in ["E","C","S"]:
                print("Please input a valid choice.\n")
                print("-> Continue\n-> Settings\n-> Exit Game")
            elif choice == "S":
                print("Sorry, this feature is not available right now. Try again later.")
            elif choice == "C":
                return True
            else:
                self.main_menu()

    #def settings(): etc.


if __name__ == "__main__":
    this_game = Main()
    this_game.start()