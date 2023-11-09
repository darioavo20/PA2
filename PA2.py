import numpy as np
import sys
import random

class node():
    def __init__(self, i_depth, board, player, i_heuristic):
        self.i_depth = i_depth
        self.i_heuristic = i_heuristic
        self.board = board
        self.player = player
        self.children = [] # list of nodes 

    def playMove(node,moves):
        tempboard = node.board
        player = node.player
        for move in moves:
            tempboard[move[0]][move[1]] = node.player
        return tempboard
    
    def getOppositePlayer(self):
        if self.player == 'Y':
            return 'R'
        else:
            return 'Y'
    
       #Recursive function to 
    def createPermutations(self):
        if self.i_depth >= 0:
            legal = find_legal_moves(self.board)
            for index in legal:
                self.children.append(node(self.i_depth-1,self.playMove(legal),self.getOppositePlayer(),self.i_heuristic))
                print(f'{self.board} \n')
            for child in self.children:
                child.createPermutations()

        

# Function to read in test case
def file_reader(file_name):
    try:
        board = [[string for string in range(7)] for string in range(6)]
        for i in range(6):
            for j in range(7):
                board[i][j] = "0"
        board = np.array(board)
        with open(file_name, 'r') as file:
            lines = file.readlines()
            remaining = lines[3:]
            algo = lines[0]
            arg = lines[1]
            turn = lines[2]
            for row, line in enumerate(remaining):
                for column, char in enumerate(line):
                    if column == 7:
                        break
                    board[row][column] = char
        return algo, arg, turn, board
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None, None, None
    
# finds legal moves for a given board and returns a list containing tuples for those moves
def find_legal_moves(board):
    legal = []
    for i in range(len(board[0])):
        for j in range(len(board)):
            if board[j][i] == 'O' and j == len(board)-1:
                legal.append((j,i))
                break
            if board[j][i] == 'O' and board[j+1][i] != 'O':
                legal.append((j,i))
                break
    return legal

# Checks if someone has won the game 
def checkWin(board):
    height = len(board)
    width = len(board[0])
    red = 'R'
    yellow = 'Y'
    draw = True

    # check for horizontal win
    for i in range(height):
        for j in range(width - 3):
            if board[i][j] == red and board[i][j+1] == red and board[i][j+2] == red and board[i][j+3] == red:
                return red
            if board[i][j] == yellow and board[i][j+1] == yellow and board[i][j+2] == yellow and board[i][j+3] == yellow:
                return yellow
            
    # check for vertical win
    for i in range(height-3):
        for j in range(width):
            if board[i][j] == red and board[i+1][j] == red and board[i+2][j] == red and board[i+3][j] == red:
                return red
            if board[i][j] == yellow and board[i+1][j] == yellow and board[i+2][j] == yellow and board[i+3][j] == yellow:
                return yellow
            
    #check for / diagonal wins
    for i in range(3, height):
        for j in range(width -3):
            if board[i][j] == red and board[i-1][j+1] == red and board[i-2][j+2] == red and board[i-3][j+3] == red:
                return red
            if board[i][j] == yellow and board[i-1][j+1] == yellow and board[i-2][j+2] == yellow and board[i-3][j+3] == yellow:
                return yellow
            
    #check for \ diagonal wins
    for i in range(height-3):
        for j in range(width-3):
            if board[i][j] == red and board[i+1][j+1] == red and board[i+2][j+2] == red and board[i+3][j+3] == red:
                return red
            if board[i][j] == yellow and board[i+1][j+1] == yellow and board[i+2][j+2] == yellow and board[i+3][j+3] == yellow:
                return yellow
            
    #check for draw
    for i in range(height):
        for j in range(width):
            if board[i][j] == 'O':
                draw = False
    
    if draw:
        return 'D'
    else:
        return 'N'
    
def uniform_random(board, turn):
    while(checkWin(board) == 'N'):
        moves = find_legal_moves(board)
        chosen_move = random.randint(0,len(moves)-1)
        row = moves[chosen_move][0]
        col = moves[chosen_move][1]
        board[row][col] = turn
        print(board)
        print('Move selected',col)
        if turn == 'R':
            print("Yellow turn now")
            turn = 'Y'
        elif turn == 'Y':
            print("Red turn now")
            turn = 'R'
    
    if checkWin(board) == 'Y':
        print("yellow wins")
    elif checkWin(board) == 'R':
        print("red wins")
    else:
        print("draw") 

def main():
    file_name = sys.argv[1]
    output_type = sys.argv[2]
    algo, arg, turn, board = file_reader(file_name)

    if 'DLMM' in algo:
        root = node(int(arg),board,turn,0)
        legal = find_legal_moves(root.board)
        root.createPermutations()
        
    if 'UR' in algo:
        uniform_random(board,turn)
        
    # win = checkWin(board)
    # if win == 'R':
    #     print("Red wins")
    # elif win == 'Y':
    #     print("Yellow wins")
    # elif win == 'D':
    #     print("Draw")
    # elif win == 'N':
    #     print("No win")

if __name__ == "__main__":
    main()