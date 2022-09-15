'''This is demo version Zombie Apocalypse v4.6.1'''
'''
Author: Tan Chieu Duong, NGUYEN
Date: 15/09/2022
'''
import os
from time import sleep
import numpy as np

# Clearing screen
def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

# Game introduction greeting
def welcome():
    screen_clear()
    print()
    print('+'*100)
    print('+'*20, ' '*13, ' Welcome To Zombie Apocalypse!', ' '*13, '+'*20)
    print('+'*100)
    print()
    sleep(1)

    desc1 = "After the nuclear war, a strange and deadly virus has infected the planet producing mindless zombies."
    desc2 = "\nThese zombies now wander the world converting any remaining living creatures they find to zombies as well..."
    for char in desc1:
        print(char, end='', flush= True)
        sleep(0.05)
    sleep(1)
    for char in desc2:
        print(char, end='', flush= True)
        sleep(0.05)
    sleep(1)
    print()

# Input the world map dimensions X-Y
def inputDimension():
    print()
    n = int(input("Please enter a number for generating the territory dimensions NxN => "))
    return n

#Function checking for valid input positions for Creatures
def checkAvailablePos(map, cPos, zPos, cID, cNum ):
    if map[cPos[0]][cPos[1]] == 'X':
        print("There is already a creature here. \nPlease enter another...")
    elif cPos != zPos:
        map[cPos[0]][cPos[1]] = 'X'
        cID += 1
        cNum -= 1
    else: 
        print("There is a Zombie in this position! \nPlease enter another...")
    return cID, cNum

#Map Initialize, main game simulation
def MapInit(n):
    x, y = [], []
    finalZombies = [] #Final list of zombies in the map
    # Create map coordinates
    for i in range(n):
        x.append('-')
        y.append(x)
    map = np.array(y)

    # Initialize the Zombie location
    print("Please input initial Zombie's position.")
    zombie_x_pos = int(input("Enter X: "))
    zombie_y_pos = int(input("Enter Y: "))

    zombiePos = [zombie_x_pos, zombie_y_pos] #Zombie location
    map[zombie_x_pos][zombie_y_pos] = 'Z' #Put zombie into position
    screen_clear()
    s1 = f"WARNING! \nZombie 'Z' awaked at coordinates (x: {zombie_x_pos}, y: {zombie_y_pos})...."
    s2 = f"Map Grid = {n}x{n}"
    print(s1, '\n')
    print(s2, '\n')
    sleep(2)

    # Create creature locations, check valid positions
    s2 = f"Number of creatures cannot >{n*n - 1}" + "\nPlease enter no. of creatures: "
    numberCreatures = int(input(s2))
    creatureId = 1
    while numberCreatures > 0:
        crt_x_pos, crt_y_pos = None, None        
        crt_x_pos = int(input(f"X-pos of creature-{creatureId}: "))
        crt_y_pos = int(input(f"Y-pos of creature-{creatureId}: "))
        print()
        crtPos = [crt_x_pos, crt_y_pos] #Creature location
        (creatureId, numberCreatures) = checkAvailablePos(map, crtPos, zombiePos, creatureId, numberCreatures)
    
    # Generate world map
    print("\nInitializing map...")
    sleep(2)
    screen_clear()
    print(map)

    # Input movement sequence for the Zombie using single characters
    # Up - U
    # Down - D
    # Left - L
    # Right - R
    moveSeq = input("\nUp-U\nDown-D\nLeft-L\nRight-R\nInput movement sequence: ")
    moveZombie(map, zombiePos, moveSeq, finalZombies) #Begin zombie movements & update final list

    #End simulation
    sleep(1)
    print("\n\nEND GAME.")

# Define movement behaviours: Up, Down, Right, Left
def moveDefine(map, zombiePos, moveSeq, zombie, finalZombies):
    xMax = len(map[0])
    yMax = len(map[1])
    zID = 0
    for char in moveSeq:
        if char == 'U':
            zNextPos = [zombiePos[0] -1, zombiePos[1]] #Get next zombie position
            zNextPos[0] = checkEdge(zNextPos[0], xMax) #Check horizontal edge
            attack = attackCheck(zNextPos, map) #Check for preparing Attack
            zID = makeDecisions(attack, map, zombiePos, zNextPos, finalZombies, zombie, zID, "UP")
            
        elif char == 'D':
            zNextPos = [zombiePos[0] +1, zombiePos[1]] #Get next zombie position
            zNextPos[0] = checkEdge(zNextPos[0], xMax) #Check horizontal edge
            attack = attackCheck(zNextPos, map) #Check for preparing Attack
            zID = makeDecisions(attack, map, zombiePos, zNextPos, finalZombies, zombie, zID, "DOWN")
  
        elif char == 'L':
            zNextPos = [zombiePos[0], zombiePos[1] -1] #Get next zombie position
            zNextPos[1] = checkEdge(zNextPos[1], yMax) #Check horizontal edge
            attack = attackCheck(zNextPos, map) #Check for preparing Attack
            zID = makeDecisions(attack, map, zombiePos, zNextPos, finalZombies, zombie, zID, "LEFT")

        elif char == 'R':
            zNextPos = [zombiePos[0], zombiePos[1] +1] #Get next zombie position
            zNextPos[1] = checkEdge(zNextPos[1], yMax) #Check horizontal edge
            attack = attackCheck(zNextPos, map) #Check for preparing Attack
            zID = makeDecisions(attack, map, zombiePos, zNextPos, finalZombies, zombie, zID, "RIGHT")

    #Add the current working zombie into final list           
    finalZombies.append([zombiePos[0], zombiePos[1]])

    #Print out all zombies, creatures positions
    printZombies(finalZombies)
    printCreatures(map)

# Function making zombie movement decisions (UDRL), and attack creatures or not.
# Then, update zombie ID.
def makeDecisions(attack, map, zombiePos, zNextPos, finalZombies, zombie, zID, action):
    if not attack: #Non-attack route
        if [zombiePos[0], zombiePos[1]] in finalZombies:
            zID += 1
        else: map[zombiePos[0], zombiePos[1]] = '-' #Reset current position to '-'
        [zombiePos[0], zombiePos[1]] = [zNextPos[0], zNextPos[1]]  #moving to next position
        map[zombiePos[0], zombiePos[1]] = 'Z'
        posUpdate(map, zombie, zID, action)

    else: #Attack route
        print("\nLiving creature detected! ATTACKING!")
        sleep(1)
        if [zombiePos[0], zombiePos[1]] in finalZombies:
            pass
        else: map[zombiePos[0], zombiePos[1]] = '-' #Reset current position to '-' 
        [zombiePos[0], zombiePos[1]] = [zNextPos[0], zNextPos[1]]  #moving to next position
        map[zombiePos[0], zombiePos[1]] = 'Z'
        finalZombies.append([zombiePos[0], zombiePos[1]])
    return zID

#Listing out all final zombie positions in the map
def printZombies(finalZombies):
    print('\nZombie\'s positions: ')
    for i, zombie in enumerate(finalZombies):
        print(zombie, end=" ")
    print()

#Listing out all final creature positions in the map
def printCreatures(map):
    crtCount = 0
    print("\nCreature's positions: ")
    for i, crt in np.ndenumerate(map):
        if crt == "X":
            crtCount +=1
            print(i, end=" ")
    if crtCount == 0:
        print("\nNone")

# Function to check if the zombie reaches any map edges and update the new positions
def checkEdge(position, maxLimit):
    if position <= -1:
        position = maxLimit -1
    elif position >= maxLimit:
        position = 0
    return position

# Checking for an Attack if there is a living creature in the position
def attackCheck(position, map):
    if map[position[0]][position[1]] == 'X':
        return True #There is a living creature here!
    else: 
        return False #No living creature here.

# Zombie positioning update
def posUpdate(map, zombie, zID, move):
    screen_clear()
    print(map, '\n')

    #Print each zombie move to console
    for pos in zombie:
        print(f"Zombie {zID} moves {move} to position {pos}")
    sleep(1)

# Zombie main movement management
def moveZombie(map, zombiePos, moveSeq, finalZombies):
    zombie = [zombiePos]
    screen_clear()
    print(map)
    print(f"Movement sequence = {moveSeq}")
    for id, pos in enumerate(zombie):
        print(f"Zombie {id} is at position {pos}")
    sleep(2)
    moveDefine(map, zombiePos, moveSeq, zombie, finalZombies)

#Main simulation starter
def SimulationStart():
    n = inputDimension()
    MapInit(n)

if __name__ == "__main__":
    welcome()
    SimulationStart()
    