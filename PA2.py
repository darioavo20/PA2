import numpy as np
import sys
import random
from pmcgs import PMCGS
import pdb
from copy import deepcopy
from MinMax import MinMax
import numpy as np

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
    if output_type.strip() == "verbose":
        pmcgs_ai = PMCGS(board, turn.strip(), True)
    else:
        pmcgs_ai = PMCGS(board, turn.strip(), False)
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
    if output_type.strip() == "verbose":
        print("FINAL Move selected: ", best_move)
    return best_move
    
def uct(board, turn, arg):
    if output_type.strip() == "verbose":
        uct_ai = PMCGS(board, turn.strip(), True)
    else:
        uct_ai = PMCGS(board, turn.strip(), False)
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
    if output_type.strip() == "verbose":
        print("FINAL Move selected: ", best_move[1] + 1)
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
        {"name": "DLMM_5", "function": dlmm, "param": 5},
        {"name": "PMCGS_500", "function": pmcgs, "param": 50},
        {"name": "PMCGS_10000", "function": pmcgs, "param": 1000},
        {"name": "UCT_500", "function": uct, "param": 50},
        {"name": "UCT_10000", "function": uct, "param": 1000}
        
    ]

   
    results = {alg['name']: {other_alg['name']: {"wins": 0, "losses": 0, "draws": 0} for other_alg in algorithms} for alg in algorithms}

    for i, alg1 in enumerate(algorithms):
        print("new alg1")
        for alg2 in algorithms[i+1:]:
            print("new alg2")
            for game in range(100):
                
               
                board = create_initial_board() 
                turn = 'R'  

              
                while True:
                    if turn == 'R':
                        move = alg1['function'](board, turn, alg1['param'])
                    else:
                        move = alg2['function'](board, turn, alg2['param'])
                    
                    
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


def test_results_self():
    algorithms = [
        {"name": "UR", "function": uniform_random, "param": True},
        {"name": "DLMM_5", "function": dlmm, "param": 5},
        {"name": "PMCGS_500", "function": pmcgs, "param": 50},
        {"name": "PMCGS_10000", "function": pmcgs, "param": 1000},
        {"name": "UCT_500", "function": uct, "param": 50},
        {"name": "UCT_10000", "function": uct, "param": 1000}
    ]

    results = {alg['name']: {"wins": 0, "losses": 0, "draws": 0} for alg in algorithms}

    for alg in algorithms:
        print(f"Testing {alg['name']}")
        for game in range(100):
            board = create_initial_board() 
            turn = 'R'  

            while True:
                move = alg['function'](board, turn, alg['param'])
                board[move[0]][move[1]] = turn
                    
                status = checkWin(board).strip()
                if status != 'N':
                    if status == 'R':
                        results[alg['name']]['wins'] += 1
                    elif status == 'Y':
                        results[alg['name']]['losses'] += 1
                    elif status == 'D':
                        results[alg['name']]['draws'] += 1
                    break
                    
                turn = 'Y' if turn == 'R' else 'R'
    print("\nTournament Results:")
    for alg, outcome in results.items():
        print(f"{alg}: Wins - {outcome['wins']}, Losses - {outcome['losses']}, Draws - {outcome['draws']}")
    return results
                

def find_tree_move(board, pmcgs_move):
    moves = find_legal_moves(board)
    for move in moves:
        if move[1] == pmcgs_move:
            return move
        
def play_human_dlmm(board):
    return
    
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
        full_pmcgs_move = pmcgs(board, 'Y', 10000)
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
        full_uct_move = uct(board, 'Y', 10000)
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

def play_human_dlmm(board):
    print(board)
    while True:
        print('Play one of the following legal moves')
        moves = find_legal_moves(board)
        print(moves)
        user_row = input("Enter row: ")
        user_col = input("Enter col: ")
        board[int(user_row)][int(user_col)] = 'R'
        print(board)
        if checkWin(board) != 'N': 
            break 
        dlmm_move = dlmm(board, 'Y', 5)
        dlmm_row = dlmm_move[0]
        dlmm_col = dlmm_move[1]
        board[dlmm_row][dlmm_col] = 'Y'
        print(board)
        if checkWin(board) != 'N': 
            break
    if checkWin(board) == 'R':
        print("You won!")
    elif checkWin(board) == 'Y':
        print("You lost!")
    else:
        print("This was a draw")


def dlmm(board, turn, arg):
    minmax = MinMax(int(arg), board, turn)
    best_move, best_value = minmax.depth_limited_minmax()
    if output_type.strip() == "verbose":
        print(f"Best move: {best_move}, Score: {best_value}")
    return best_move

def main():
    file_name = sys.argv[1]
    global output_type
    output_type = sys.argv[2].lower()
    #preset by programmer for testing purposes
    alternating = False
    algo, arg, turn, board = file_reader(file_name)
    while True:
        print("\nWelcome to AI Connect Four!")
        print("Choose an option:")
        print("1. Run Algorithm from inputted command")
        print("2. Play Against Algorithm")
        print("3. Run Algorithm Tournament")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            if 'UR' in algo:
                uniform_random(board,turn,alternating)

            if 'DLMM' in algo:
                dlmm(board, turn,int(arg))     

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
        elif choice == "2":
            play_human = input("Input then number associated with the desired option \n 1. PMCGS 10000 \n 2. UCT 10000 \n 3. DLM 5 \n 4. No \n")
            if play_human == "1":
                play_human_pmcgs(board)
                sys.exit()
            if play_human == "2":
                play_human_uct(board)
                sys.exit()
            if play_human == "3":
                play_human_dlmm(board)
                sys.exit()
        elif choice == "3":
            test_results()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
        

    

    

if __name__ == "__main__":
    main()