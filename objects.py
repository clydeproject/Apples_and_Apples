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


class Board():
    def __init__(self,rows,coloums,square,char_1,char_2):

        '''rows : int,\ncoloums : int,\nsquare : str,\nchar_1 : str,\nchar_2 : str'''
       
        self.square = square
        self.char_1 = char_1
        self.char_2 = char_2
        self.rows = rows
        self.coloums = coloums
        self.board = [[ self.square for k in range(self.coloums)] for j in range(self.rows)]
        self.__display_board = ""

    def populate_board_green(self,x,y):
        if self.board[x-1][y-1] == self.square:
            self.board[x-1][y-1] = self.char_1
        else:
            return False 
    
    def populate_board_red(self,x,y):
        if self.board[x-1][y-1] == self.square:
            self.board[x-1][y-1] = self.char_2
        else:
            return False 
    
    def board_preview(self):
        x_label = "  "
        y_label = 1

        for a in range(self.coloums):
            x_label+=f"{a+1} "
        
        self.__display_board = x_label
        self.__display_board += "\n"

        for square_row in (self.board):
            self.__display_board += f"{y_label}"
            for square in square_row:
                self.__display_board += f"{square}"
            y_label+=1
            self.__display_board += "\n"
            
        print(self.__display_board)
        self.__display_board = ""
    
    def get_row(self,index):
        return self.board[index]

    def get_column(self,index):
        return [self.get_row(x)[index] for x in range(self.rows)]

    def get_diagonal(self):
        diagonal = False
        if self.rows == self.coloums:
            diagonal = [self.board[x][x] for x in range(self.coloums)]
        return diagonal
    
    def get_all_squares(self):
        squares = []
        for row in self.board:
            for square in row:
                squares.append(square)
        return squares

    def reset_board(self):
        self.board = ""
        self.board = [[self.square for k in range(self.coloums)] for j in range(self.rows)]

    def __len__(self):
        return self.rows*self.coloums


class Player():
    def __init__(self,name,colour):
        '''
        name : str\n 
        colour : bool: True - Green, False - Red
        '''
        self.name = name
        self.apple_colour = colour
        self.moves_made = 0
        self.__squares = []

    def make_move(self,board,x,y):#might have to change arg names
        if self.apple_colour:
            board.populate_board_green(x,y)
            self.__squares.append(f"{x},{y}")
            self.moves_made+=1
        else:
            board.populate_board_red(x,y)
            self.__squares.append(f"{x},{y}")
            self.moves_made+=1
    
    def reset_player(self):
        self.__squares = []
        self.moves_made = 0

#wrapper function 
def default_preview(board_object):
    board_object.board_preview()

def classic_ascii_preview(board_obj,x_spacing=1,y_spacing=0):
    '''
    #spaceing works best with single classical ascii characters 
    '''
    display_board = " "
    x_label = 1
    y_label = 1

    for a in range(board_obj.coloums):#column numbering 
        display_board+= (x_spacing*" ") + f"{x_label}"
        x_label+=1    
        
    display_board += f"\n"

    for square_row in (board_obj.board):

        display_board += ("\n"*y_spacing)+f"{y_label}"#row numbering 

        for square in square_row:
            if square == board_obj.square:
                display_board += (x_spacing*" ") + f"{board_obj.square}"
            elif square == board_obj.char_1:
                display_board += (x_spacing*" ") + f"{board_obj.char_1}"
            else:
                display_board += (x_spacing*" ") + f"{board_obj.char_2}"

        y_label+=1
        display_board += "\n"
            
    print(display_board)
    display_board = ""


if __name__ == "__main__":
   # print(__name__)
    pass