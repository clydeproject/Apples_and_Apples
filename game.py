'''
Copyright 2021 Paartha Nimbalkar

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so.

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import os
import objects
import json
import sys 
import subprocess

def install_dependencies():
    #installs required packages via pip
    with open("dependencies.json","r") as f:
        
        dependencies = json.load(f)

        if dependencies["dependencies_not_installed"]:

            print("\nINSTALLING DEPENDENCIES\n")
            
            for package in dependencies["packages"]:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])                
            
            dependencies["dependencies_not_installed"] = False 
           
            with open("dependencies.json","w") as f_:
                json.dump(dependencies,f_)
            
            print("\nALL DEPENDENCIES INSTALLED")
            print("\nSTARTING GAME ...\n")

install_dependencies()

import pyfiglet
from playsound import playsound
from termcolor import colored

board_chars = sys.argv#contains user picked skin for board 

skin_args = {
    "default":["default","⬛","🍏","🍎",objects.default_preview],
    "classic":["classic","#","X","O",objects.classic_ascii_preview],
    }

#commands = []

if len(board_chars) == 2 and board_chars[1] == "classic":
    board_chars = skin_args["classic"]
else:
    board_chars = skin_args["default"]

#Game title 
print(
    f'''{colored(pyfiglet.figlet_format("Apples",font="slant"),"red",
    attrs=["bold"])}{colored(pyfiglet.figlet_format("& Apples",font="slant"),
    "yellow")}'''
    )

playsound(sound=f"{os.getcwd()}\\sounds\\intro.wav")#start up music

player1 = objects.Player(
    input(f"\n{board_chars[3]}  Player 1  enter your display name : "),
    False,
)

player2 = objects.Player(
    input(f"{board_chars[2]}  Player 2 enter your display name : "),
    True
)

print("\nNow enter the dimensions of your board below.")

board1 = objects.Board(
    int(input("Rows : ")),
    int(input("Columns : ")),
    board_chars[1],
    board_chars[2],
    board_chars[3],
)

tryagain = "y"
winner = ""
game_state = True#is false when game is over
whos_turn = [True,]
x_pos = []
y_pos = []
rounds = 1

def classify_input(string):
    if string == "/ff":
        os._exit(0)
    else:
        for index,letter in enumerate(string):
            if letter == ",":
                x_pos.append(int(string[0:index]))
                y_pos.append(int(string[index+1:]))
                break
    

def reset_game():
    global winner,game_state,whos_turn,rounds,x_pos,y_pos#re write line 
    winner = ""
    game_state = True
    whos_turn = [True,]
    x_pos = []
    y_pos = []
    rounds = 1
    board1.reset_board()

def check_game_state():
    global winner,game_state
    #checks columns 
    for column_number in range(board1.coloums):
        if all([square==board1.char_2 for square in board1.get_column(column_number)]):
            winner = "red"
            game_state = False
            return True
        elif all([square==board1.char_1 for square in board1.get_column(column_number)]):
            winner = "green"
            game_state = False
            return True
    #checks rows
    for row_number in range(board1.rows):
        if all([square==board1.char_2 for square in board1.get_row(row_number)]):
            winner = "red"
            game_state = False
            return True
        elif all([square == board1.char_1 for square in board1.get_row(row_number)]):
            winner = "green"
            game_state = False
            return True 
    #checks diagonal 
    if board1.rows == board1.coloums:
        if all([square==board1.char_2 for square in board1.get_diagonal()]):
            winner = "red"
            game_state = False
            return True
        elif all([square==board1.char_1 for square in board1.get_diagonal()]):
            winner = "green"
            game_state = False
            return True 
    #checks if draw
    if all([square != board1.square for square in board1.get_all_squares()]):
        winner = "draw"
        game_state = False
        return True

#Game loop
while True:
    if tryagain == "y":
        print("\n")

        skin_args[board_chars[0]][4](board1)

        while game_state:
            
            print(f"\nROUND - {rounds}")

            if whos_turn[len(whos_turn)-1]:
                classify_input(input(f"{player1.name}'s turn : "))
                
                player1.make_move(board1,
                    x=x_pos[len(x_pos)-1],
                    y=y_pos[len(y_pos)-1],
                )
                whos_turn.append(player1.apple_colour)
                rounds+=1
                
                skin_args[board_chars[0]][4](board1)
                playsound(sound=f"{os.getcwd()}\\sounds\\one.wav")

                check_game_state()
            else:
                classify_input(input(f"{player2.name}'s turn : "))
                
                player2.make_move(board1,
                    x=x_pos[len(x_pos)-1],
                    y=y_pos[len(y_pos)-1],
                )
                    
                whos_turn.append(player2.apple_colour)
                rounds+=1

                skin_args[board_chars[0]][4](board1)
                playsound(sound=f"{os.getcwd()}\\sounds\\one.wav")

                check_game_state()

        #game result 
        if winner == "green":
            print(
                f'''{colored(pyfiglet.figlet_format(f"{player2.name}",font="slant"),"green",attrs=["bold"])}'''
                )
            print(
                f'''{colored(pyfiglet.figlet_format("WON",font="slant"),"magenta",attrs=["bold","underline"])}'''
                )
        elif winner == "draw":
            print(
                f'''{colored(pyfiglet.figlet_format("DRAW",font="slant"),"cyan",attrs=["bold","underline"])}'''
                )
        else:
            print(
                f'''{colored(pyfiglet.figlet_format(f"{player1.name}",font="slant"),"red",attrs=["bold"])}'''
                )
            print(
                f'''{colored(pyfiglet.figlet_format("WON",font="slant"),"magenta",attrs=["bold","underline"])}'''
                )    
        playsound(sound=f"{os.getcwd()}\\sounds\\win.wav")
        
        reset_game()

        tryagain = input("Try again? y/n : ")
    else:
        break
