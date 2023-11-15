import copy

class MinMax:
    def __init__(self, depth_limit, board, turn):
        self.depth_limit = depth_limit
        self.board = board
        self.turn = turn

    def heuristic_evaluation(self, board):
        # Constants to weigh the importance of each factor
        connected_weight = 0.5
        ended_paths_weight = 0.5

        # Calculate the scores for connected pieces and ended paths
        connected_score = self.calculate_connected_score(board)
        ended_paths_score = self.calculate_ended_paths_score(board)

        # Combine the scores
        combined_score = (connected_weight * connected_score) + (ended_paths_weight * ended_paths_score)

        # Normalize the score between -1 and 1
        normalized_score = self.normalize_score(combined_score, 1, -1)

        return normalized_score

    def calculate_connected_score(self, board):
        score = 0
        height = len(board)
        width = len(board[0])

        # Define scoring for different lengths of connections
        scoring = {2: 1, 3: 2, 4: 4}

        # Check horizontal, vertical, and diagonal connections
        for row in range(height):
            for col in range(width):
                for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:  # directions: horizontal, vertical, diagonal
                    count = 0
                    for d in range(1, 4):  # check up to 3 steps in each direction
                        x, y = col + d * dx, row + d * dy
                        if 0 <= x < width and 0 <= y < height and board[row][col] == board[y][x] and board[row][col] != 'O':
                            count += 1
                        else:
                            break
                    score += scoring.get(count, 0)

        return score
    
    def calculate_ended_paths_score(self, board):
        score = 0
        height = len(board)
        width = len(board[0])

        # Check for potential extendable lines
        for row in range(height):
            for col in range(width):
                if board[row][col] == 'O':
                    continue
                for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    count = 0
                    for d in range(1, 4):
                        x, y = col + d * dx, row + d * dy
                        if 0 <= x < width and 0 <= y < height:
                            if board[row][col] == board[y][x]:
                                count += 1
                            elif board[y][x] == 'O':
                                # Open space for extension
                                score += 1 if count >= 2 else 0
                                break
                            else:
                                break

        return score
    
    def normalize_score(self, score, max_score, min_score):
        # Assuming max_score and min_score are known or estimated
        range = max_score - min_score
        normalized = (score - min_score) / range
        return normalized * 2 - 1 


    def checkWin(self, board):
        height = len(board)
        width = len(board[0])
        red = "R"
        yellow = "Y"
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

    def minmax(self, game_state, depth, is_maximizing_player):
        if depth == 0 or self.checkWin(game_state):
            return self.heuristic_evaluation(game_state)

        if is_maximizing_player:
            best_value = -float('inf')
            for move in self.find_legal_moves(game_state):
                new_state = self.apply_move(game_state, move)
                value = self.minmax(new_state, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for move in self.find_legal_moves(game_state):
                new_state = self.apply_move(game_state, move)
                value = self.minmax(new_state, depth - 1, True)
                best_value = min(best_value, value)
            return best_value

    def depth_limited_minmax(self):
        best_move = None
        best_value = -float('inf')
        
        for move in self.find_legal_moves(self.board):
            new_state = self.apply_move(self.board, move)
            value = self.minmax(new_state, self.depth_limit - 1, False)
            if value > best_value:
                best_value = value
                best_move = move

        return best_move, best_value
    
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
    
    def apply_move(self,state,move):
        new_state = copy.deepcopy(state)
        j, i = move
        new_state[j][i] = self.turn
        return new_state