import random
import copy
class Node:
    def __init__(self, state):
        self.state = state
        self.children = []


    
class PMCGS:
    def __init__(self, root_state, turn):
        self.root = Node(root_state)
        self.turn = turn

    def select(self, node):
        if node.children:
            return random.choice(node.children)
        else:
            return -1
    

    def expand(self, node):
        legal_moves = self.find_legal_moves(node.state)
        for move in legal_moves:
            print(move)
            new_state = self.apply_move(node.state, move)
            child_node = Node(new_state)
            node.children.append(child_node)

    def apply_move(self,state,move):
        new_state = copy.deepcopy(state)
        j, i = move
        new_state[j][i] = self.turn
        return new_state
    
    def switch_turn(self):
        self.turn = 'Y' if self.turn == 'R' else 'R'

    def simulate(self):
        pass

    def backprop(self):
        pass

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


