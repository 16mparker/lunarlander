# lunar_lander.py #

# on top of the origional game, I decided to alter it slightly to make it a 1v1 an the winner is who lands first.

# first start with the basic game
# ========================================= #
import pyinputplus as pyip  # module for making sure inputs are valid. Save's writing my own logic function.

def simple_1_player(num_players=1, difficulty="easy"):

    determine_landed = lambda alt: True if alt <= 0 else False

    # setting up some initial variables
    landed = crashed = False  # game will end when either is set to True

    # change fuel burn rate depending on difficulty
    difficulties = {"easy": .15, "medium": .3, "hard": .5}

    fuel_burn_constant = difficulties[difficulty]  # rate at which fuel is burnt. Higher values = more difficult game

    altitude = 250.0  # altitude measured in meters. game ends upon reaching 0 metres
    velocity = 0.0 if difficulty != "hard" else 25 # velocity measured in m/s. for more difficult games set above 0
    fuel = 250.0 # fuel remaining measured in litres. cannot pass below 0
    time = 0  # amount of seconds passed. Increases by one per iteration of the while loop

    # safe landing must be below 10m/s

    while not (landed or crashed):
        print("Current velocity: %s, Current Altiude: %s" % (round(velocity, 2), round(altitude, 2)))
        # ask the user to input fuel to burn.
        # user will be repromted if type != int or input is more than fuel remaining
        fuel_burned = pyip.inputInt(prompt="How much fuel would you like to burn. %s litres remaining. \n>>> " % fuel, max=fuel, min=0)
        fuel -= fuel_burned  # reduce fueld remaining in tank
        velocity += 1.6 - fuel_burned * fuel_burn_constant
        altitude -= velocity

        landed = determine_landed(altitude)

        if landed and velocity > 10.0:
            crashed = True
            print("You crashed, Game Over")

        elif landed:
            crashed = False
            print("You landed succesfully")


# WORK IN PROGRESS #

# now to make the 2 player version with similar logic #
# we will be making each rocket a class instance #
# game ends when someone lands or crashes
# ===================================================== #

def simple_2_player(num_players=2, difficulty="easy"):
    # setting up some initial variables

    # change fuel burn rate depending on difficulty
    difficulties = {"easy": (.15, 250), "medium": (.3, 150), "hard": (.5, 150)}

    fuel_burn_constant = difficulties[difficulty][0]  # rate at which fuel is burnt. Higher values = more difficult game

    class Lander:  # create class to use for each player
        def __init__(self, name):
            self.landed = self.crashed = False  # game will end when either is set to True
            self.name = name
            self.altitude = 250
            self.fuel = difficulties[difficulty][1]
            self.velocity = 0 if difficulty != "hard" else 25
            self.time = 0  # TODO score players based on time taken

        determine_landed = lambda self: True if self.altitude <= 0 else False

        def turn(self):
            print("\n%s's go \nCurrent velocity: %sm/s, Current Altiude: %sm" % (self.name, round(self.velocity, 2), round(self.altitude, 2)))
            # ask the player to input fuel to burn.
            # user will be repromted if type != int or input is more than fuel remaining
            self.fuel_burned = pyip.inputInt(prompt="How much fuel would you like to burn. %s litres remaining. \n>>> " % self.fuel, max=self.fuel, min=0)
            self.fuel -= self.fuel_burned  # reduce fueld remaining in tank
            self.velocity += 1.6 - self.fuel_burned * fuel_burn_constant
            self.altitude -= self.velocity

            self.landed = self.determine_landed()

            if self.landed and self.velocity > 10.0:
                self.crashed = True
                print("You crashed, Game Over\n")

            elif self.landed:
                self.crashed = False
                print("You landed succesfully\n")

        def check_game_over(self):
            return True if self.crashed or self.landed else False

    # repeat the match until any of landed or crashed is equal to true

    # create list of player objects
    players = [Lander(input(f"\nWhat's player {str(i+1)}'s name?\n>>> ")) for i in range(num_players)]

    over = []
    successful = []

    while players:  # game repeats until players crash
        for player in players:
            if not player.check_game_over():  # checks play is True and player has not crashed
                player.turn()
            else:
                over.append(player)
                if not player.crashed:
                    successful.append(player)

                del players[players.index(player)]

    # logic for first to land wins or last to crash

    print(successful[0].name, "won!\n") if successful else print(over[-1].name, "won!\n")

def main():
    play = True
    while play:  # games will repeat until player selects "no" for play again
        games = {1: simple_1_player, 2: simple_2_player}

        players_number = pyip.inputInt(prompt="\nHow many players?\n>>> ", min=1)  # retrieves number of players from user

        print()
        difficulty = pyip.inputMenu(['easy', 'medium', 'hard'], numbered=True)  # asks the user for the difficulty

        game_option = lambda x: 1 if x == 1 else 2  # determines what game to play (single player for 1 and multiplayer for >2)
        games[game_option(players_number)](num_players=players_number, difficulty=difficulty)  # run game basedn off of user input for num of players

        # play again if user selects yes
        print("Would you like to play again?")
        play = True if pyip.inputMenu(['yes', 'no'], numbered=True) == "yes" else False


if __name__ == "__main__":
    main()
