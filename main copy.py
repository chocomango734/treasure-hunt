
# This program has the user move around a map to find treasures.
# If the user hits a trap they lose, but if they find all seven treasures they win.

import random

def main():
    #initialize map and player location
    player_position = [0,0]
    upper_bound = 6
    quit = False
    treasures_left = 7
    hidden_map = []
    for i in range(7):
        hidden_map.append(['.'] * 7)
    map_key = read_map() #create map key list

    #start game! display initial standings of game
    print("Treasure Hunt!")
    print("Find the 7 treasures without getting caught in a trap. Look around to spot nearby traps and treasures.")
    display_map(hidden_map, player_position)

    while quit is False:
        #ask user for what direction they want to move
        dir = input("Enter direction (WASD or L to Look around or Q to Quit): ").upper()
        
        #check for valid input, prompt user for valid input
        while (dir != "W") and (dir != "A") and (dir != "S") and (dir != "D") and (dir != "L") and (dir != "Q"):
            print("Invalid input.")
            display_map(hidden_map, player_position)
            dir = input("Enter direction (WASD or L to Look around or Q to Quit): ").upper()

        # quit if user wants to quit
        if dir == "Q":
            quit = True

        # look around and tell user number of treasures and traps nearby
        elif dir == "L":
            count = count_treasures_traps(map_key, player_position, upper_bound)
            print(f"You detect {count[0]} treasures nearby.")
            print(f"You detect {count[1]} traps nearby.")
            if hidden_map[player_position[0]][player_position[1]] != 'T':
                hidden_map[player_position[0]][player_position[1]] = count[1]
            display_map(hidden_map, player_position)

        # move player if valid input
        else:
            move_player(player_position, dir, upper_bound)
            
            #check if player's current location is a treasure
            if (map_key[player_position[0]][player_position[1]] == 'T') and (hidden_map[player_position[0]][player_position[1]] != 'T'):
                treasures_left -= 1
                print(f"You found treasure!\nThere are {treasures_left} treasures remaining.")
                #update map to show treasure
                hidden_map[player_position[0]][player_position[1]] = 'T'

                #end game if user has found all treasures
                if treasures_left == 0:
                    print("You found all the treasures! You win!")
                    quit = True

                #display current map with updated location and treasures
                display_map(hidden_map, player_position)
                
            #quit if player's current location is a trap
            elif map_key[player_position[0]][player_position[1]] == 'X':
                print(f"You were caught in a trap! \nYou found {7 - treasures_left} treasures.")
                display_map(hidden_map, player_position)
                print("Game over!")
                quit = True

            #display map if nothing on player's current location
            else:
                display_map(hidden_map, player_position)
            
def read_map():
    """ this function reads the map from the file and returns a 2D list of the map
    arguments: 
        none
    returns:
        map_list: 2D list of the map
    """

    # to make a randomized map: for each row number each position 0-6 randint treasure
    # & trap, exclusive; for loop through each row incrementing counts, replace w T or X if randint

    map_list = []
    # read each line of the file and append it to the map key list
    for i in range(7):
        # randomize treasure and trap placement for each row excluding starting position
        if i == 0:
            treasure = random.randint(1, 6)
            trap = random.randint(1, 6)
        else:
            treasure = random.randint(0, 6)
            trap = random.randint(0, 6)
        # create each list row within the 2D list
        list = []
        for j in range(7):
            if j == treasure:
                list.append('T')
            elif j == trap:
                list.append('X')
            else:
                list.append('.')
        map_list.append(list)

    return map_list


def display_map(map, player):
    """ displays current map including player location and found treasures or hints
    arguments:
        map (2D list), player (player's location as a list of coordinates)
    returns:
        none
    """
    for row in range(len(map)):
        for item in range(len(map[row])):
            #print P on player's location
            if (row == player[0]) and (item == player[1]) and (item != 6):
                print("P", end=" ")
                
            #print P on player's location with new row after if player is at end of row
            elif (row == player[0]) and (item == player[1]) and (item == 6):
                print("P", end="\n")
                
            #print list with next line after each row
            elif item == 6:
                print(map[row][item], end="\n")
            else:
                print(map[row][item], end=" ")

def move_player(player, dir, upper_bound):
    """ moves the player in the selected direction, checks player in bounds
    arguments:
        player (coordinates of player), dir (direction the olayer chooses to move), upper_bound (boundaries of map)
    returns:
        player coordinates as a list
    """
    # w moves player up, a moves player left, s moves player down, d moves player right
    if dir == "A":
        if player[1] == 0:
            print("You cannot move that direction")
        else:    
            player[1] -= 1
    elif dir == "W":
        if player[0] == 0:
            print("You cannot move that direction")
        else:
            player[0] -=1
    elif dir == "D":
        if player[1] == upper_bound:
            print("You cannot move that direction")
        else:
            player[1] += 1
    elif dir == "S":
        if player[0] == upper_bound:
            print("You cannot move that direction")
        else:
            player[0] +=1
    else:
        print("Invalid input")
    return player

def count_treasures_traps(map, player, upper_bound):
    """ reads the map around the player and counts the number of treasures and traps
    arguments:
        map (player's coordinates) player (player's location as a list of coordinates), upper_bound (boundaries of map)
    returns: 
        the count of treasures and traps as a list (0 = treasures, 1 = traps)
    """
    #setting trasure and trap count to 0 and defining the directions around the player
    treasure_traps_count = [0,0]
    adjacent_spaces = [(-1,0), (1,0), (0,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    
    #checks every space around player
    for space in adjacent_spaces:
        map_row = player[0] + space[0]
        map_column = player[1] + space[1]
        
        #adds to the treasure_traps_count if the space is a treasure or trap
        if upper_bound >= map_row >= 0 and upper_bound >= map_column >= 0:
            if map[map_row][map_column] == 'T':
                treasure_traps_count[0] += 1
            elif map[map_row][map_column] == 'X':
                treasure_traps_count[1] += 1

    return treasure_traps_count

if __name__ == "__main__":
    main()