from math import inf
from copy import deepcopy

BLANK = -1  #-1 represents blank field
BOARD_SIZE = 8
ALL_DIRECTIONS = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)] 
#matrix FIELDS_VALUES represents value of each field
FIELDS_VALUES = [[ 25, -10,  5,  5,  5,  5, -10,  25],
                 [-10, -10, -2, -2, -2, -2, -10, -10],
                 [  5,  -2,  0,  0,  0,  0,  -2,   5],
                 [  5,  -2,  0,  0,  0,  0,  -2,   5],
                 [  5,  -2,  0,  0,  0,  0,  -2,   5],
                 [  5,  -2,  0,  0,  0,  0,  -2,   5],
                 [-10, -10, -2, -2, -2, -2, -10, -10],
                 [ 25, -10,  5,  5,  5,  5, -10,  25]]
#initial values for minimax strategy with alpha-beta pruning
START_ALPHA = -inf
START_BETA = inf
START_DEPTH = 3 #3 is maximum possible depth of algorithm with time limit 1 sec
START_MAXIMIZING_PLAYER = True
 
class MyPlayer:
    '''Player uses minimax strategy with alpha-beta pruning with depth = 3'''
    def __init__(self, my_color, opponent_color):
        self.name = 'shvaiale'
        self.my_color = my_color
        self.opponent_color = opponent_color
  
 
    def move(self, board):
        #I store possible moves as a dictionary, where
        #KEY is a tuple of indexes of a possible move (i, j) and
        #VALUE is a count of opponent's stones, which I will earn
        self.possible_moves = set()
        self.find_possible_moves(board, self.my_color, self.opponent_color)
        if not self.possible_moves: #if set is empty
            return None
        self.optimal_move = None
        self.minimax(board, START_MAXIMIZING_PLAYER, \
            START_DEPTH, START_ALPHA, START_BETA)
        return self.optimal_move
        
 
 
    def find_possible_moves(self, board, my_color, opp_color):
        #First sifting. I find opponent's stones on the board, then find
        #nearby blanks and write their indexes as KEYS of possible moves
        self.possible_moves = set()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == opp_color:
                    nearby_blanks = self.find_nearby_blanks(board, i, j)
                    self.possible_moves.update(nearby_blanks)
        #Now I'm filling matrix of VALUES
        copy = self.possible_moves.copy()
        for i, j in copy:
            is_move = False
            for dir_i, dir_j in ALL_DIRECTIONS:
                if self.is_sequence(board, i, j, dir_i, dir_j, my_color, opp_color):
                    is_move = True
                    break
            if not is_move:
                self.possible_moves.remove((i, j))
            

                
    def find_nearby_blanks(self, board, i, j):
        #I will write matrix 3x3 as a VALUE of possible moves for now,
        #it will represent points, which I will earn in each direction
        nearby_blanks = set()

        for dir_i, dir_j in ALL_DIRECTIONS:
            cur_i, cur_j = i + dir_i, j + dir_j
            if self.is_on_board(cur_i, cur_j) and \
            board[cur_i][cur_j] == BLANK:
                nearby_blanks.add((cur_i, cur_j))
        return nearby_blanks


    def is_sequence(self, board, i, j, dir_i, dir_j, my_color, opp_color):
        cur_i = i + dir_i
        cur_j = j + dir_j
        
        if not self.is_on_board(cur_i, cur_j) or \
        board[cur_i][cur_j] != opp_color:
            return False
 
        while self.is_on_board(cur_i, cur_j):
            if board[cur_i][cur_j] == BLANK:
                return False
             
            if board[cur_i][cur_j] == opp_color:
                cur_i += dir_i
                cur_j += dir_j
                continue
 
            if board[cur_i][cur_j] == my_color:
                return True
        return False
 
 
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
            self.find_possible_moves(board, self.my_color, self.opponent_color)
            moves = self.possible_moves
            if not moves:
                return self.minimax(board, True, depth - 1, alpha, beta)
            for move in moves:
                new_board = self.update_board(board, move, self.my_color)
                eval = self.minimax(new_board, False, depth - 1, alpha, beta)
                if eval >= max_eval:
                    max_eval = eval
                    if depth == START_DEPTH:
                        self.optimal_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = inf 
            self.find_possible_moves(board, self.opponent_color, self.my_color)
            moves = self.possible_moves
            if not moves:
                return self.minimax(board, False, depth - 1, alpha, beta)
            for move in moves:
                new_board = self.update_board(board, move, self.opponent_color)
                eval = self.minimax(new_board, True, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


    def game_ended(self, board):
        self.find_possible_moves(board, self.my_color, self.opponent_color)
        my_moves = self.possible_moves
        if my_moves:
            return False
 
        self.find_possible_moves(board, self.opponent_color, self.my_color)
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



    def flip_stones(self, board, i, j, dir_i, dir_j, color):
        cur_i = i + dir_i
        cur_j = j + dir_j

        while board[cur_i][cur_j] != color:
            board[cur_i][cur_j] = color
            cur_i += dir_i
            cur_j += dir_j
    



if __name__ == "__main__":
    player = MyPlayer(0, 1)
    board = [[-1, -1, -1, -1, -1,  1, -1,  0],
             [-1, -1, -1,  1, -1, -1,  1, -1],
             [-1, -1, -1, -1,  1,  0,  1,  1],
             [-1, -1, -1,  0,  0,  1, -1, -1],
             [-1, -1,  0,  0,  0,  1, -1, -1],
             [-1, -1,  0,  0,  0, -1, -1, -1],
             [-1, -1,  0, -1,  0, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1, -1]]
     
    print(player.move(board))
