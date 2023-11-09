import numpy as np
from sys import maxsize


class node(object):
    def __init__(self, i_depth, board, player, i_value=None, twoadj=None, threeadj=None):
        self.i_depth = i_depth
        self.i_value = i_value
        self.board = board
        self.twoadj = twoadj
        self.threeadj = threeadj
        self.player = player
        self.children = []
        self.createPermutations()

#Recursive function to 
def createPermutations(node):
    if node.i_depth >= 0:
        legal = find_legal_moves(node.board)
        for index in legal:
            node.children.board[index] = 
            node.children.append(node(node-1),node.i_value)
            print(node.bo)

    
# Function to read in test case
def file_reader():
    try:
        file_name = input("Enter the file name you wish to test: ")
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
            print(board)
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
# TODO: account for full board (game over)
def checkWin(board):
    height = len(board)
    width = len(board[0])
    red = 'R'
    yellow = 'Y'

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

def main():
    file_name = sys.argv[1]
    output_type = sys.argv[2]
    algo, arg, turn, board = file_reader(file_name)
    root = node(arg,board,turn,node.i_value,node.twoadj,node.threeadj)
    legal = find_legal_moves(node.board)
    node.createPermutations(node)
    
    win = checkWin(board)
    if win == 'R':
        print("Red wins")
    elif win == 'Y':
        print("Yellow wins")
    elif win == 'D':
        print("Draw")
    else:
        print("No win")


if __name__ == "__main__":
    main()