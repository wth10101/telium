#Telium - the game (stage 6)

import random

#Global variables

num_modules = 17                #The number of modules in the space station
module = 1                      ##The module of the space station we are in
last_module = 0                 #The last module we were in
possible_moves = []             #List of the possible moves we can make
alive = True                    #Whether the player is alive or dead
won = False                     #Whether the player has won
power = 100                     #The amount of power the space station has
fuel = 500                      #The amount of fuel the player has in the flamethrower
locked = 0                      #The module that has been locked by the player
queen = 0                       #Location of the queen alien
vent_shafts = []                #Location of the ventilation shaft entrances
info_panels = []                #Location of the information panels
workers = []                    #Location of the worker aliens

#Procedure declarations

def move_queen():
    global num_modules, module, last_module, locked, queen, won, vent_shafts
    #If we are in the same module as the queen...
    if module == queen:
        print("There it is!  The queen alien is in this module...")
        #Decide how many moves the queen should take
        moves_to_make = random.randint(1,3)
        can_move_to_last_module = False
        while moves_to_make > 0:
            #Get the escapes the queen can make
            escapes = get_modules_from(queen)
            #Remove the current module as an escape
            if module in escapes:
                escapes.remove(module)
            #Allow queen to double back behind us from another module
            if last_module in escapes and can_move_to_last_module == False:
                escapes.remove(last_module)
            #Remove a module that is locked as an escape
            if locked in escapes:
                escapes.remove(locked)

            print("**********")
            print(escapes)
            #If there is no escape then player has won...
            if len(escapes) == 0:
                won = True
                moves_to_make = 0
                print("...and the door is locked.  It's trapped.")
            #Otherwise move the queen to an adjacent module
            else:
                if moves_to_make == 1:
                    print("...and has escaped.")
                queen = random.choice(escapes)
                moves_to_make = moves_to_make - 1
                can_move_to_last_module = True
                #Handle the queen being in a module with a ventilation shaft
                while queen in vent_shafts:
                    if moves_to_make > 1:
                        print("...and has escaped.")
                    print("We can hear scuttling in the ventilation shafts.")
                    valid_move = False
                    #Queen cannot land in a module with another ventilation shaft
                    while valid_move == False:
                        valid_move = True
                        queen = random.randint(1,num_modules)
                        if queen in vent_shafts:
                            valid_move = False
                    #Queen always stops moving after travelling through shaft
                    moves_to_make = 0

def lock():
    global num_modules, power, locked
    new_lock = int(input("Enter module to lock:"))
    if new_lock<0 or new_lock>num_modules:
        print("Invalid module.  Operation failed.")
    elif new_lock == queen:
        print("Operation failed.  Unable to lock module.")
    else:
        locked = new_lock
        print("Aliens cannot get into module",locked)
    power_used = 25 + 5*random.randint(0,5)

def check_vent_shafts():
    global num_modules, module, vent_shafts, fuel
    if module in vent_shafts:
        print("There is a bank of fuel cells here.")
        print("You load one into your flamethrower.")
        fuel_gained = 50
        print("Fuel was",fuel,"now reading: ",fuel+fuel_gained)
        fuel = fuel + fuel_gained
        print("The doors suddenly lock shut.")
        print("What is happening to the station?")
        print("Our only escape is to climb into the ventilation shaft.")
        print("We have no idea where we are going.")
        print("We follow the passages and find ourselves sliding down.")
        last_module = module
        module = random.randint(1,num_modules)
        load_module()


def spawn_npcs():
    global num_modules, queen, vent_shafts, greedy_info_panels, workers
    module_set = []
    for counter in range(2,num_modules):
        module_set.append(counter)
    random.shuffle(module_set)
    i = 0
    queen = module_set[i]
    for counter in range(0,3):
        i=i+1
        vent_shafts.append(module_set[i])

    for counter in range(0,2):
        i=i+1
        info_panels.append(module_set[i])
        
    for counter in range(0,3):
        i=i+1
        workers.append(module_set[i])

def load_module():
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()

def get_modules_from(module):
    moves = []
    text_file = open("Charles_Darwin/module" + str(module) + ".txt", "r")
    for counter in range(0,4):
        move_read = text_file.readline()
        move_read = int(move_read.strip())
        if move_read != 0:
            moves.append(move_read)
    text_file.close()
    return moves
       
def output_module():
    global module
    print()
    print("-----------------------------------------------------------------")
    print()
    print("You are in module",module)
    print()

def output_moves():
    global possible_moves
    print()
    print("From here you can move to modules: | ",end='')
    for move in possible_moves:
        print(move,'| ',end='')
    print()
    
def get_action():
    global module, last_module, possible_moves
    valid_action = False
    while valid_action == False:
        print("What do you want to do next ? (MOVE, SCANNER)")
        action = input(">")
        if action == "MOVE":
            move = int(input("Enter the module to move to: "))
            if move in possible_moves:
                valid_action = True
                last_module = module
                module = move
            else:
                print("The module must be connected to the current module.")

        if action == "SCANNER":
            command = input("Scanner ready.  Enter command (LOCK):")
            if command == "LOCK":
                lock()


#Main program starts here

spawn_npcs()
print("Queen alien is located in module:",queen)
print("Ventilation shafts are located in module:",vent_shafts)
print("Information panels are located in module:",info_panels)
print("Worker aliens are located in:",workers)
                
while alive and not won:
    load_module()
    check_vent_shafts()
    move_queen()
    if won == False and alive == True:
        output_moves()
        get_action()

if won == True:
    print("The queen is trapped and you burn it to death with your flamethrower.")
    print("Game over.  You win!")
if alive == False:
    print("The station has run out of power.  Unable to sustain life support, you die.")
