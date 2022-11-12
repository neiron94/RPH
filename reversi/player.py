from math import inf
from copy import deepcopy

BLANK = -1
BOARD_SIZE = 8
ALL_DIRECTIONS = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)] 
#this matrix represents value of each field
FIELDS_VALUES = [[ 6, -5,  3,  3,  3,  3, -5,  6],
                 [-5, -5, -2, -2, -2, -2, -5, -5],
                 [ 3, -2,  0,  0,  0,  0, -2,  3],
                 [ 3, -2,  0,  0,  0,  0, -2,  3],
                 [ 3, -2,  0,  0,  0,  0, -2,  3],
                 [ 3, -2,  0,  0,  0,  0, -2,  3],
                 [-5, -5, -2, -2, -2, -2, -5, -5],
                 [ 6, -5,  3,  3,  3,  3, -5,  6]]
#initial values for minimax alpha-beta pruning strategy
START_ALPHA = inf
START_BETA = -inf
START_DEPTH = 3
START_MAXIMIZING_PLAYER = True
 
class MyPlayer:
    #TODO - class description
    '''Very informative comment'''
    def __init__(self, my_color, opponent_color):
        self.name = 'shvaiale'
        self.my_color = my_color
        self.opponent_color = opponent_color
  
 
    def move(self, board):
        #I store possible moves as a dictionary, where
        #KEY is a tuple of indexes of a possible move (i, j) and
        #VALUE is a count of opponent's stones, which I will earn
        self.possible_moves = dict()
        self.find_possible_moves(board)
        if self.possible_moves:    #if dict isn't empty
            self.move = None
            self.minimax(board, START_MAXIMIZING_PLAYER, \
                START_DEPTH, START_ALPHA, START_BETA)
            return self.move
        return None     #if dict is empty
 
 
    def find_possible_moves(self, board):
        #First sifting. I find opponent's stones on the board, then find
        #nearby blanks and write their indexes as KEYS of possible moves
        self.possible_moves = dict()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == self.opponent_color:
                    nearby_blanks = self.find_nearby_blanks(board, i, j)
                    self.possible_moves.update(nearby_blanks)
        #Now I'm filling matrix of VALUES
        for i, j in self.possible_moves:
            for dir_i, dir_j in ALL_DIRECTIONS:
                self.fill_matrix(board, i, j, dir_i, dir_j)

        self.final_sifting()
 
 
    def find_nearby_blanks(self, board, i, j):
        #I will write matrix 3x3 as a VALUE of possible moves for now,
        #it will represent points, which I will earn in each direction
        nearby_blanks = dict()

        for dir_i, dir_j in ALL_DIRECTIONS:
            cur_i, cur_j = i + dir_i, j + dir_j
            if self.is_on_board(cur_i, cur_j) and \
            board[cur_i][cur_j] == BLANK:
                nearby_blanks[(cur_i, cur_j)] = [[0,0,0],
                                                 [0,0,0],
                                                 [0,0,0]]
        return nearby_blanks
         
 
    def fill_matrix(self, board, i, j, dir_i, dir_j):
        #I'm checking direction (dir_i, dir_j) from point (i, j),
        #if there is a chain of opponent's stones, finished with my stone,
        #then I write number of opponent's stones in the matrix of VALUES
        #on related place ([1 + dir_i][1 + dir_j]), else I write 0
        key = (i, j)
        matrix_i = 1 + dir_i
        matrix_j = 1 + dir_j
        #(cur_i, cur_j) - current point to be checked
        cur_i = i + dir_i
        cur_j = j + dir_j
        #after this check we are sure, that the first stone is opponent's
        if not self.is_on_board(cur_i, cur_j) or \
        board[cur_i][cur_j] != self.opponent_color:
            return
 
        while self.is_on_board(cur_i, cur_j):
            if board[cur_i][cur_j] == BLANK:
                #there is obviosly no turn, if we've encountered blank
                self.possible_moves[key][matrix_i][matrix_j] = 0
                return
             
            if board[cur_i][cur_j] == self.opponent_color:
                #increments related element of matrix of VALUES
                self.possible_moves[key][matrix_i][matrix_j] += 1
                #go to the next point (cur_i + dir_i, cur_j + dir_j)
                cur_i += dir_i
                cur_j += dir_j
                continue
 
            if board[cur_i][cur_j] == self.my_color:
                #end of a chain
                return
        #if we've got off a loop, then we aren't on the board
        self.possible_moves[key][matrix_i][matrix_j] = 0
 
 
    def final_sifting(self):
        #I replace matrix of VALUES with sum of it's elements + value of
        #related element of matrix FIELDS_VALUES and
        #delete move, if sum = 0
        copy = self.possible_moves.copy()
        for key, value in copy.items():
            elements_sum = 0
            for line in value:
                elements_sum += sum(line)
             
            if elements_sum == 0:
                del self.possible_moves[key]
            #to delete
            else:
                self.possible_moves[key] = elements_sum
            #
 
    def is_on_board(self, a, b):
        #check, if (a, b) is on the board
        return True if 0 <= a < BOARD_SIZE and 0 <= b < BOARD_SIZE else False

################################################################################

    def minimax(self, board, maximizingPlayer, depth, alpha, beta):
        if self.game_ended(board):
            if self.I_won(board):
                return inf
            else:
                return -inf

        if depth == 0:
            return self.count_position(board)

        if maximizingPlayer:
            max_eval = -inf
            self.find_possible_moves(board)
            moves = self.possible_moves.keys()
            for move in moves:
                new_board = self.update_board(board, move, self.my_color)
                eval = self.minimax(new_board, False, depth - 1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    self.move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = inf
            self.my_color, self.opponent_color = self.opponent_color, self.my_color 
            self.find_possible_moves(board)
            self.my_color, self.opponent_color = self.opponent_color, self.my_color
            moves = self.possible_moves.keys()
            for move in moves:
                new_board = self.update_board(board, move, self.opponent_color)
                eval = self.minimax(new_board, True, depth - 1, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval


    def game_ended(self, board):
        self.find_possible_moves(board)
        my_moves = self.possible_moves
        if my_moves:
            return False

        self.my_color, self.opponent_color = self.opponent_color, self.my_color 
        self.find_possible_moves(board)
        self.my_color, self.opponent_color = self.opponent_color, self.my_color
        opp_moves = self.possible_moves
        if opp_moves:
            return False

        return True

    def I_won(self, board):
        my_stones = 0
        opp_stones = 0
        for line in board:
            for stone in line:
                if stone == self.my_color:
                    my_stones += 1
                elif stone == self.opponent_color:
                    opp_stones += 1
        return my_stones > opp_stones


    def count_position(self, board):
        result = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                stone = board[i][j]
                if stone == self.my_color:
                    result += 1
                    result += FIELDS_VALUES[i][j]
                elif stone == self.opponent_color:
                    result -= 1
                    result -= FIELDS_VALUES[i][j]
        return result

    
    def update_board(self, board, move, color):
        another_color = 0
        if color == 0:
            another_color = 1
        
        new_board = deepcopy(board)
        i, j = move[0], move[1]
        new_board[i][j] = color
        for dir_i, dir_j in ALL_DIRECTIONS:
            if self.is_sequence(new_board, i, j, dir_i, dir_j, color, another_color):
                self.flip_stones(new_board, i, j, dir_i, dir_j, color)
        return new_board

    def is_sequence(self, board, i, j, dir_i, dir_j, color, another_color):
        cur_i = i + dir_i
        cur_j = j + dir_j
        
        if not self.is_on_board(cur_i, cur_j) or \
        board[cur_i][cur_j] != another_color:
            return False
 
        while self.is_on_board(cur_i, cur_j):
            if board[cur_i][cur_j] == BLANK:
                return False
             
            if board[cur_i][cur_j] == another_color:
                cur_i += dir_i
                cur_j += dir_j
                continue
 
            if board[cur_i][cur_j] == color:
                return True
        return False

    def flip_stones(self, board, i, j, dir_i, dir_j, color):
        cur_i = i + dir_i
        cur_j = j + dir_j

        while board[cur_i][cur_j] != color:
            board[cur_i][cur_j] = color
            cur_i += dir_i
            cur_j += dir_j
    



if __name__ == "__main__":
    player = MyPlayer(1, 0)
    board = [[-1, -1, -1, -1,  1, -1, -1, -1],
             [-1, -1, -1,  1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1,  0,  0,  0, -1, -1],
             [-1,  1,  1,  1,  0, -1, -1, -1],
             [-1, -1, -1, -1,  0, -1, -1, -1],
             [-1, -1, -1, -1,  0, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1, -1]]
     
    print(player.move(board))
    
