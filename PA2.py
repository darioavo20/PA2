import numpy as np
import sys
import random
from pmcgs import PMCGS
from copy import deepcopy


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
                new_board = self.playMove(index)  # Pass a specific move instead of the entire list
                new_player = self.getOppositePlayer()  # Get the opposite player for the new node
                #print(f"{print_board(new_board)} \n")
                self.children.append(node(self.i_depth-1, new_board, new_player, self.i_heuristic,self))
                #print(f'{self.board} \n')
            
            for child in self.children:
                child.createPermutations()

    def getHeuristic(self):
        opponent = 'R' if self.player == 'Y' else 'Y'

        winner = checkWin(self.board)
        #print(f"Current Board:\n{print_board(self.board)}")
        print(f"Winner: {winner}")

        if winner == 'R':
            print("Red wins")
            return 'R'  # Assign a high value for winning state
        elif winner == 'Y':
            print("Yellow wins")
            return 'Y'  # Assign a low value for losing state
        elif all(cell != 'O' for row in self.board for cell in row):
            print("It's a draw")
            return 'N'  # Assign a value for a draw
        else:
            # Calculate the new heuristic values
            consecutive_total = self.count_consecutive_total()
            open_ended_total = self.open_ended_consecutive_count()

            # Normalize the values to be between -1 and 1
            max_value = max(consecutive_total, open_ended_total)
            normalized_consecutive = consecutive_total / max_value if max_value != 0 else 0.0
            normalized_open_ended = open_ended_total / max_value if max_value != 0 else 0.0

            # Combine the normalized values with weights
            return normalized_consecutive + 0.5 * normalized_open_ended
        
    def count_consecutive_total(self):
        count = 0

    # Check horizontally
        for row in self.board:
            count += self.score_consecutive(row)

        # Check vertically
        for col in range(len(self.board[0])):
            column = [self.board[row][col] for row in range(len(self.board))]
            count += self.score_consecutive(column)

        # Check diagonally (top-left to bottom-right)
        for row in range(len(self.board) - 1):
            for col in range(len(self.board[0]) - 1):
                diagonal = [self.board[row + i][col + i] for i in range(min(len(self.board) - row, len(self.board[0]) - col))]
                count += self.score_consecutive(diagonal)

        # Check diagonally (top-right to bottom-left)
        for row in range(len(self.board) - 1):
            for col in range(1, len(self.board[0])):
                diagonal = [self.board[row + i][col - i] for i in range(min(len(self.board) - row, col + 1))]
                count += self.score_consecutive(diagonal)

        return count

    def score_consecutive(self, line):
        current_player = self.player
        opponent = 1 if current_player == -1 else -1  # Assuming player values are -1 and 1
        score = 0
        consecutive_count = 0

        for cell in line:
            if cell == current_player:
                consecutive_count += 1
            elif cell == opponent:
                consecutive_count = 0
            else:
                consecutive_count = 0

            if consecutive_count >= 4:
                score += 1

        return score
    
    def open_ended_consecutive_count(self):
        count = 0

        # Check horizontally
        for row in self.board:
            count += self.count_open_ended_consecutive(row)

        # Check vertically
        for col in range(len(self.board[0])):
            column = [self.board[row][col] for row in range(len(self.board))]
            count += self.count_open_ended_consecutive(column)

        # Check diagonally (top-left to bottom-right)
        for row in range(len(self.board) - 1):
            for col in range(len(self.board[0]) - 1):
                diagonal = [self.board[row + i][col + i] for i in range(min(len(self.board) - row, len(self.board[0]) - col))]
                count += self.count_open_ended_consecutive(diagonal)

        # Check diagonally (top-right to bottom-left)
        for row in range(len(self.board) - 1):
            for col in range(1, len(self.board[0])):
                diagonal = [self.board[row + i][col - i] for i in range(min(len(self.board) - row, col + 1))]
                count += self.count_open_ended_consecutive(diagonal)

        return count

    def count_open_ended_consecutive(self, line):
        current_player = self.player
        opponent = 1 if current_player == -1 else -1  # Assuming player values are -1 and 1
        consecutive_count = 0

        for i, cell in enumerate(line):
            if cell == current_player:
                consecutive_count += 1
            elif cell == opponent:
                consecutive_count = 0
            else:
                # Check if the sequence has at least one open end
                if i - consecutive_count > 0 and i < len(line) - 1 and line[i - consecutive_count - 1] == 0 and line[i + 1] == 0:
                    consecutive_count += 1
                else:
                    consecutive_count = 0

        return consecutive_count


    def backprop(self):
        temp = self

       
        for child in temp.children:
            child.backprop()

        if not temp.children:
            temp.i_heuristic = temp.getHeuristic() # this node is a leaf 
            return
        
        dicionary = {}
        for count, child in enumerate(temp.children):
            dicionary[count] = child.i_heuristic
            print(f"column: {count}: {child.i_heuristic} \n")

        if temp.i_heuristic == 'R':
            return
        if temp.i_heuristic == 'Y':
            return
        if temp.i_heuristic == 'N':
            return
        

        if temp.parent:
            temp.i_heuristic = max(dicionary.values()) if temp.parent.player == 'Y'else min(dicionary.values())
            #alpha > Beta prunne     
            for key, value in dicionary.items():
                if value == temp.i_heuristic:
                    print(f"Testing Move Selected: {key}")
                    break
        

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
            #print(algo)
            arg = lines[1]
            turn = lines[2]
            for row, line in enumerate(remaining):
                for column, char in enumerate(line):
                    if column == 7:
                        break
                    board[row][column] = char

        #print(f'starting Board:\n {board} \n')
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
        
        
        if turn == 'R':
           
            turn = 'Y'
        elif turn == 'Y':
            
            turn = 'R'
    

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def pmcgs(board, turn, arg):
    pmcgs_ai = PMCGS(board, turn.strip())
    i = 0
    while i < int(arg):
        if pmcgs_ai.select(pmcgs_ai.root) == -1:
            pmcgs_ai.expand(pmcgs_ai.root)
        
        selection = pmcgs_ai.select(pmcgs_ai.root)
        result = pmcgs_ai.simulate(selection)
        pmcgs_ai.backprop(selection, result)
        i += 1
    
    best_move = pmcgs_ai.choose_best_move()
    pmcgs_ai.print_move_scores()
    print("FINAL Move selected: ", best_move)
    return best_move
    
def uct(board, turn, arg):
    uct_ai = PMCGS(board, turn.strip())
    i = 0
    while i < int(arg):
        if uct_ai.uct_select(uct_ai.root) == -1:
            uct_ai.expand(uct_ai.root)
        
        selection = uct_ai.uct_select(uct_ai.root)
        result = uct_ai.simulate(selection)
        uct_ai.backprop(selection, result)
        i += 1
    
    best_move = uct_ai.choose_best_move()
    uct_ai.print_move_scores()
    print("FINAL Move selected: ", best_move)
    return best_move

def create_initial_board():
    # Return a new, empty board
    return [['O' for _ in range(7)] for _ in range(6)]

def find_lowest_available_row(board, column):
    for row in range(len(board) - 1, -1, -1):  
        if board[row][column] == 'O':  
            return row
    return None

def test_results():
    algorithms = [
        {"name": "UR", "function": uniform_random, "param": True},
        {"name": "PMCGS_500", "function": pmcgs, "param": 500},
        {"name": "PMCGS_10000", "function": pmcgs, "param": 10000},
        {"name": "UCT_500", "function": uct, "param": 500},
        {"name": "UCT_10000", "function": uct, "param": 10000}
    ]

   
    results = {alg['name']: {other_alg['name']: {"wins": 0, "losses": 0, "draws": 0} for other_alg in algorithms} for alg in algorithms}

    for i, alg1 in enumerate(algorithms):
        for alg2 in algorithms[i+1:]:
            for game in range(100):
                print("new Game")
               
                board = create_initial_board() 
                turn = 'R'  

              
                while True:
                    if turn == 'R':
                        move = alg1['function'](board, turn, alg1['param'])
                    else:
                        move = alg2['function'](board, turn, alg2['param'])
                    
                    print(move)
                    board[move[0]][move[1]] = turn
                    
                    
                   
                    status = checkWin(board).strip()
                    if status != 'N':
                        
                        if status == 'R':
                            results[alg1['name']][alg2['name']]['wins'] += 1
                            results[alg2['name']][alg1['name']]['losses'] += 1
                        elif status == 'Y':
                            results[alg1['name']][alg2['name']]['losses'] += 1
                            results[alg2['name']][alg1['name']]['wins'] += 1
                        elif status == 'D':
                            results[alg1['name']][alg2['name']]['draws'] += 1
                            results[alg2['name']][alg1['name']]['draws'] += 1
                        break
                    
                   
                    turn = 'Y' if turn == 'R' else 'R'
                

   
    for alg1 in algorithms:
        for alg2 in algorithms:
            if alg1 != alg2:
                print(f"{alg1['name']} vs {alg2['name']}: Wins: {results[alg1['name']][alg2['name']]['wins']}, Losses: {results[alg1['name']][alg2['name']]['losses']}, Draws: {results[alg1['name']][alg2['name']]['draws']}")



def ur_vs_pmcgs(board, turn):
    empty_board = deepcopy(board)
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
    
        board = deepcopy(empty_board)
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
    
# method to play with human player
def play_human_pmcgs(board):
    print(board)
    while(True):
        print('Play one of the following legal moves')
        moves = find_legal_moves(board)
        print(moves)
        user_row = input("Enter row: ")
        user_col = input("Enter col: ")
        board[int(user_row)][int(user_col)] = 'R'
        print(board)
        if checkWin(board) != 'N': 
            break
        pmcgs_move = pmcgs(board, 'Y', 10000, False)
        full_pmcgs_move = find_tree_move(board, pmcgs_move-1)
        pmcgs_row = full_pmcgs_move[0]
        pmcgs_col = full_pmcgs_move[1]
        board[pmcgs_row][pmcgs_col] = 'Y'
        print(board)
        if checkWin(board) != 'N': 
            break
    if checkWin(board) == 'R':
        print("You won!")
    elif checkWin(board) == 'Y':
        print("You lost!")
    else:
        print("This was a draw")

def play_human_uct(board):
    print(board)
    while(True):
        print('Play one of the following legal moves')
        moves = find_legal_moves(board)
        print(moves)
        user_row = input("Enter row: ")
        user_col = input("Enter col: ")
        board[int(user_row)][int(user_col)] = 'R'
        print(board)
        if checkWin(board) != 'N': 
            break
        uct_move = uct(board, 'Y', 10000, False)
        full_uct_move = find_tree_move(board, uct_move-1)
        uct_row = full_uct_move[0]
        uct_col = full_uct_move[1]
        board[uct_row][uct_col] = 'Y'
        print(board)
        if checkWin(board) != 'N': 
            break
    if checkWin(board) == 'R':
        print("You won!")
    elif checkWin(board) == 'Y':
        print("You lost!")
    else:
        print("This was a draw")


def main():
    file_name = sys.argv[1]
    output_type = sys.argv[2]
    #preset by programmer for testing purposes
    alternating = False
    algo, arg, turn, board = file_reader(file_name)
    play_human = input("Would you like to play against an algorithm? (Input then number associated with the desired option) \n 1. PMCGS 10000 \n 2. UCT 10000 \n 3. No \n")
    if play_human == "1":
        play_human_pmcgs(board)
        sys.exit()
    if play_human == "2":
        play_human_uct(board)
        sys.exit()
    run_tournament = input("Would you like to run the algo tournament (y/n)")
    if run_tournament == 'y':
        test_results()

    if 'UR' in algo:
        uniform_random(board,turn,alternating)

    if 'DLMM' in algo:
        root = node(int(arg),board,turn,0)
        legal = find_legal_moves(root.board)
        root.createPermutations()
        root.backprop()

    if "PMCGS" in algo:
        if output_type == "verbose":
            pmcgs(board, turn, arg)
        else:
            pmcgs(board, turn, arg)

    if "UCT" in algo:
        if output_type == "verbose":
            uct(board, turn, arg)
        else:
            uct(board, turn, arg)

    

if __name__ == "__main__":
    main()