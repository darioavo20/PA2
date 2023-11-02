import numpy as np

# Function to read in test case
def file_reader():
    try:
        #file_name = input("Enter the file name you wish to test: ")
        file_name = "test1.txt"
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
    
def main():
    algo, arg, turn, board = file_reader()
    

if __name__ == "__main__":
    main()