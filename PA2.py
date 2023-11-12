import numpy as np
import sys
import random
from pmcgs import PMCGS

class node():
    def __init__(self, i_depth, board, player, i_heuristic, parent = None):
        self.i_depth = i_depth
        self.i_heuristic = i_heuristic
        self.board = board
        self.player = player
        self.children = [] # list of nodes 
        self.parent = parent

    def playMove(self, move):
        tempboard = [row.copy() for row in self.board]  # Create a new copy of the board
        tempboard[move[0]][move[1]] = self.player  # Apply the move to the new board
        return tempboard
        
    def getOppositePlayer(self):
        if self.player == 'Y':
            return 'R'
        else:
            return 'Y'
    
       #Recursive function to 
    def createPermutations(self):
        if self.i_depth > 0:
            legal = find_legal_moves(self.board)
            for index in legal:
                new_board = self.playMove(index)
                new_player = self.getOppositePlayer()
                self.children.append(node(self.i_depth - 1, new_board, new_player, self.i_heuristic, self))

        for child in self.children:
            child.createPermutations()

    def getHeuristic(self):
        opponent = 'R' if self.player == 'Y' else 'Y'

        winner = checkWin(self.board)
        if winner == "red":
            print("Red wins")
            return float('inf')  # Assign a high value for winning state
        elif winner == "yellow":
            print("Yellow wins")
            return -float('inf')  # Assign a low value for losing state
        elif all(cell != 'O' for row in self.board for cell in row):
            return 0  # Assign a value for a draw
        else:
            return self.count_consecutive_total()
        
    def count_consecutive_total(self):
        count = 0

        # Check horizontally
        for row in self.board:
            count += self.count_consecutive(row)

        # Check vertically
        for col in range(len(self.board[0])):
            column = [self.board[row][col] for row in range(len(self.board))]
            count += self.count_consecutive(column)

        # Check diagonally (top-left to bottom-right)
        for row in range(len(self.board) - 1):
            for col in range(len(self.board[0]) - 1):
                diagonal = [self.board[row + i][col + i] for i in range(min(len(self.board) - row, len(self.board[0]) - col))]
                count += self.count_consecutive(diagonal)

        # Check diagonally (top-right to bottom-left)
        for row in range(len(self.board) - 1):
            for col in range(1, len(self.board[0])):
                diagonal = [self.board[row + i][col - i] for i in range(min(len(self.board) - row, col + 1))]
                count += self.count_consecutive(diagonal)

        return count

    def count_consecutive(self, line):
        count = 0
        current_player = self.player
        consecutive_count = 0

        for cell in line:
            if cell == current_player:
                consecutive_count += 1
            else:
                consecutive_count = 0

            if consecutive_count >= 4:
                count += 1

        return count


    def backprop(self, arg):
        temp = self
        testcheck = 0

        # Traverse the tree to find the leaf node
        while temp.children:
            temp = temp.children[0]

        # Perform backpropagation to update the values of parent nodes
        while temp.parent:
            temp.i_heuristic = temp.getHeuristic()

            # Check if there are children before finding the maximum value
            if temp.children:
                for count, child in enumerate(temp.children):
                    print(f"column{count}: {child.i_heuristic} \n")

                # Check for a tie
                if all(child.i_heuristic == -0 for child in temp.children):
                    temp.i_heuristic = -1
                    print("It's a tie!")
                    break  # Exit the loop in case of a tie

                # Continue with the maximum or minimum value based on the player
                if temp.parent.player == "Y":
                    temp.i_heuristic = max(child.i_heuristic for child in temp.children)
                    print(f"Move Selected: {temp.i_heuristic}")
                else:
                    temp.i_heuristic = min(child.i_heuristic for child in temp.children)
                    print(f"Move Selected: {temp.i_heuristic}")

            temp = temp.parent
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
            print(algo)
            arg = lines[1]
            turn = lines[2]
            for row, line in enumerate(remaining):
                for column, char in enumerate(line):
                    if column == 7:
                        break
                    board[row][column] = char

        print(f'starting Board:\n {board} \n')
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
    
def uniform_random(board, turn, alternating):
    if alternating:
        moves = find_legal_moves(board)
        chosen_move = random.randint(0,len(moves)-1)
        row = moves[chosen_move][0]
        col = moves[chosen_move][1]
        return (row,col)
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

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def pmcgs(board, turn, arg, verbose):
    pmcgs_ai = PMCGS(board, turn.strip(), verbose)
    i = 0
    while i < int(arg):
        if pmcgs_ai.select(pmcgs_ai.root) == -1:
            pmcgs_ai.expand(pmcgs_ai.root)
        
        selection = pmcgs_ai.select(pmcgs_ai.root)
        result = pmcgs_ai.simulate(selection)
        pmcgs_ai.backprop(selection, result)
        #print("_____________________________________________________")
        i += 1
    
    best_move = pmcgs_ai.choose_best_move()
    pmcgs_ai.print_move_scores()
    print("FINAL Move selected: ", best_move)
    return best_move
    
def uct(board, turn, arg, verbose):
    uct_ai = PMCGS(board, turn.strip(), verbose)
    i = 0
    while i < int(arg):
        if uct_ai.uct_select(uct_ai.root) == -1:
            uct_ai.expand(uct_ai.root)
        
        selection = uct_ai.uct_select(uct_ai.root)
        result = uct_ai.simulate(selection)
        uct_ai.backprop(selection, result)
        print("_____________________________________________________")
        i += 1
    
    best_move = uct_ai.choose_best_move()
    uct_ai.print_move_scores()
    print("FINAL Move selected: ", best_move)
    return best_move

def test_results(board, turn):
    empty_board = board
    if 'R' in turn:
        turn = 'R'
    if 'Y' in turn:
        turn = 'Y'

    #testing UR vs PMCGS (500)
    ur_pmcgs500_wins = 0
    ur_pmcgs500_losses = 0
    ur_pmcgs500_draws = 0
    for i in range(100):
        while(True):
            ur_move = uniform_random(board, turn, True)
            ur_row = ur_move[0]
            ur_col = ur_move[1]
            board[ur_row][ur_col] = turn
            print(board)
            print(turn)
            print(checkWin(board))
            if checkWin(board) != 'N': 
                break
            if turn == 'R':
                turn = 'Y'
            elif turn == 'Y':
                turn = 'R'
            pmcgs_move = pmcgs(board, turn, 500, False)
            full_pmcgs_move = find_tree_move(board, pmcgs_move-1)
            pmcgs_row = full_pmcgs_move[0]
            pmcgs_col = full_pmcgs_move[1]
            board[pmcgs_row][pmcgs_col] = turn
            print(board)
            print(turn)
            print(checkWin(board))
            if checkWin(board) != 'N': 
                break
            if turn == 'R':
                turn = 'Y'
            elif turn == 'Y':
                turn = 'R'
        if(checkWin(board) == 'R'):
            ur_pmcgs500_wins += 1
        elif(checkWin(board) == 'Y'):
            ur_pmcgs500_losses += 1
        else:
            ur_pmcgs500_draws += 1
        board = empty_board
    print('UR wins', ur_pmcgs500_wins)
    print("UR win%:", ur_pmcgs500_wins/100)
    print("PMCGS500 wins", ur_pmcgs500_losses)
    print("PMCGS500 win%:", ur_pmcgs500_losses/100)
    print("UR vs PMCGS500 draws:", ur_pmcgs500_draws)
    

    
def find_tree_move(board, pmcgs_move):
    moves = find_legal_moves(board)
    for move in moves:
        if move[1] == pmcgs_move:
            return move
    

def main():
    file_name = sys.argv[1]
    output_type = sys.argv[2]
    #preset by programmer for testing purposes
    alternating = False
    algo, arg, turn, board = file_reader(file_name)
    test_results(board, turn)

    if 'UR' in algo:
        uniform_random(board,turn,alternating)

    if 'DLMM' in algo:
        root = node(int(arg),board,turn,0)
        legal = find_legal_moves(root.board)
        root.createPermutations()
        root.backprop(arg)

    if "PMCGS" in algo:
        if output_type == "verbose":
            pmcgs(board, turn, arg, True)
        else:
            pmcgs(board, turn, arg, False)

    if "UCT" in algo:
        if output_type == "verbose":
            uct(board, turn, True)
        else:
            uct(board, turn, False)

    

if __name__ == "__main__":
    main()