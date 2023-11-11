import random
import copy
from termcolor import colored




class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.children = []
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.visits = 0
        self.parent = parent

    
class PMCGS:
    def __init__(self, root_state, turn, verbose = False):
        self.root = Node(root_state)
        self.turn = turn #turn that updates every move
        self.verbose = verbose
        self.start_turn = turn #this is the player's turn at the start
    def select(self, node):
        if node.children:
            self.switch_turn()
            return random.choice(node.children)
        else:
            return -1
        
    

    def expand(self, node):
        legal_moves = self.find_legal_moves(node.state)
        for move in legal_moves:
            new_state = self.apply_move(node.state, move)
            child_node = Node(new_state, parent=node)
            node.children.append(child_node)
            if self.verbose:
                print("NODE ADDED")

    def apply_move(self,state,move):
        new_state = copy.deepcopy(state)
        j, i = move
        new_state[j][i] = self.turn
        return new_state
    
    def switch_turn(self):
        self.turn = 'Y' if self.turn == 'R' else 'R'

    def simulate(self, node):
        current_state = copy.deepcopy(node.state)
        while True:
            
            if self.verbose:
                print("New state in simulation")
                self.print_connect_four_board(current_state)

            winner = self.checkWin(current_state)
            if winner != 'N':
                terminal_value = 1 if winner == self.start_turn else -1 if winner != 'D' else 0
                if self.verbose:
                    print(f"TERMINAL NODE VALUE: {terminal_value}")
                return terminal_value

            legal_moves = self.find_legal_moves(current_state)
            if not legal_moves:
                if self.verbose:
                    print("TERMINAL NODE VALUE: 0")  # Draw
                return 0
            self.switch_turn()
            move = random.choice(legal_moves)
            current_state = self.apply_move(current_state, move)
            if self.verbose:
                print(f"Move selected: {move}, Current turn: {self.turn}")
            


    def backprop(self, node, result):
        while node is not None:
            node.visits += 1
            if result == 1:
                node.wins += 1
            elif result == -1:
                node.losses += 1
            else:
                node.draws += 1
            if self.verbose:
                print(f"Updated values:\nwi: {node.wins}\nni: {node.visits}")
            node = node.parent

    def checkWin(self, board):
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

    def find_legal_moves(self, board):
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
    
    def print_connect_four_board(self, board):
        for row in board:
            print("|", end="")
            for cell in row:
                if cell == 'R':
                    colored_cell = colored(cell, 'red')
                elif cell == 'Y':
                    colored_cell = colored(cell, 'yellow')
                else:
                    colored_cell = " "
                print(f" {colored_cell} |", end="")
            print()  
        print("-" * (len(board[0]) * 4 + 1)) 

    




  

