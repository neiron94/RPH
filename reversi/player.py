'''----------Used materials----------'''
#1)Video about minimax strategy: 
#https://www.youtube.com/watch?v=STjW3eH0Cik&t
#2)My implementation of minimax strategy is inspired by this video:
#https://www.youtube.com/watch?v=l-hh51ncgDI&t

'''----------Used libraries----------'''
from math import inf
from copy import deepcopy

'''----------Constants for MyPlayer----------'''
BLANK = -1  #-1 represents blank field
BOARD_SIZE = 8
ALL_DIRECTIONS = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
#Initial values for minimax strategy with alpha-beta pruning
START_ALPHA = -inf
START_BETA = inf
START_DEPTH = 3 #3 is maximum possible depth of algorithm with time limit 1 sec
START_MAXIMIZING_PLAYER = True  #True - my turn, False - opponent's turn
#Matrix FIELDS_VALUES represents value of each field
FIELDS_VALUES = [[20, -5,  5,  5,  5,  5, -5, 20],
                 [-5, -5, -2, -2, -2, -2, -5, -5],
                 [ 5, -2,  0,  0,  0,  0, -2,  5],
                 [ 5, -2,  0,  0,  0,  0, -2,  5],
                 [ 5, -2,  0,  0,  0,  0, -2,  5],
                 [ 5, -2,  0,  0,  0,  0, -2,  5],
                 [-5, -5, -2, -2, -2, -2, -5, -5],
                 [20, -5,  5,  5,  5,  5, -5, 20]]


class MyPlayer:
    '''Player uses minimax strategy with alpha-beta pruning with depth = 3'''
    def __init__(self, my_color, opponent_color):
        self.name = 'shvaiale'
        self.my_color = my_color
        self.opp_color = opponent_color

 
    def move(self, board):
        #At first I check, if at least one possible move exists
        possible_moves = MyPlayer.find_moves(board, self.my_color, self.opp_color)
        #if there is no any possible moves, then return None
        if not possible_moves:
            return None
        #else count self.optimal_move in function minimax and return it
        self.optimal_move = None
        self.minimax(board, START_MAXIMIZING_PLAYER, \
            START_DEPTH, START_ALPHA, START_BETA)
        return self.optimal_move


    '''----------Functions for finding possible moves----------'''
    @staticmethod
    def find_moves(board, my_color, opp_color):
        #Arguments my_color and opp_color allow me to compute my possible
        #moves (my_color = self.my_color, opp_color = self.opponent_color)
        #and opponent's possible 
        #moves (my_color = self.opponent_color, opp_color = self.my_color)

        #I store possible moves as a set of tuples of
        #indexes of a possible move (i, j) and return it
        possible_moves = set()

        #Find opponent's stones on the board, then find nearby
        #blanks and write their indexes in a set of possible moves
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == opp_color:
                    nearby_blanks = MyPlayer.find_nearby_blanks(board, i, j)
                    possible_moves.update(nearby_blanks)
        
        #Go throw a set of possible moves and delete invalid moves
        copy = possible_moves.copy()
        for i, j in copy:
            #Look at all directions from (i, j) and search for
            #the sequence of opponent's stones ended with my stone.
            #If there is a sequence, then it's a valid move
            is_valid_move = False
            for dir_i, dir_j in ALL_DIRECTIONS:
                if MyPlayer.is_sequence(board, i, j, dir_i, dir_j, my_color, opp_color):
                    is_valid_move = True
                    break
            if not is_valid_move:
                possible_moves.remove((i, j))
        return possible_moves
            

    @staticmethod
    def find_nearby_blanks(board, i, j):
        nearby_blanks = set()
        #Look at all directions from (i, j) and add all nearby
        #blanks to the nearby_blanks set, then return it
        for dir_i, dir_j in ALL_DIRECTIONS:
            cur_i, cur_j = i + dir_i, j + dir_j
            if MyPlayer.is_on_board(cur_i, cur_j) and \
            board[cur_i][cur_j] == BLANK:
                nearby_blanks.add((cur_i, cur_j))
        return nearby_blanks


    @staticmethod
    def is_sequence(board, i, j, dir_i, dir_j, my_color, opp_color):
        #Look from field (i, j) in direction (dir_i, dir_j) and
        #return True, if there is a sequence of opp_color stones
        #ended with my_color stone, else return False

        #current field to check (cur_i, cur_j) 
        cur_i = i + dir_i
        cur_j = j + dir_j
        
        #After this check we are sure, that there is
        #an opp_color stone on (cur_i, cur_j)
        if not MyPlayer.is_on_board(cur_i, cur_j) or \
        board[cur_i][cur_j] != opp_color:
            return False
 
        while MyPlayer.is_on_board(cur_i, cur_j):
            #there is obviosly no sequence, if we've encountered BLANK
            if board[cur_i][cur_j] == BLANK:
                return False
             
            if board[cur_i][cur_j] == opp_color:
                #go to the next field
                cur_i += dir_i
                cur_j += dir_j
                continue
 
            #end of sequence
            if board[cur_i][cur_j] == my_color:
                return True
        #return False, if we've gone off a loop (= gone off a board)
        return False


    @staticmethod
    def is_on_board(a, b):
        #Check, if (a, b) is on the board
        return True if 0 <= a < BOARD_SIZE and 0 <= b < BOARD_SIZE else False


    '''----------Strategy functions----------'''
    def minimax(self, board, maximizingPlayer, depth, alpha, beta):
        #Classic minimax with alpha-beta pruning. This recursive algorithm
        #looks three moves ahead and chooses the move, that will lead
        #to the best position.
        #maximizingPlayer = True means it's my turn to choose
        #evaluation now and I will choose maximal,
        #maximizingPlayer = False means it's opponent's turn
        #to choose now and he will choose minimal.
        #You can watch more about this strategy in "Used materials"

        #if I won, then I obviosly want to reach this position (return inf),
        #else I lost or it's a draw (return -inf)
        if self.game_finished(board):
            if self.I_won(board):
                return inf
            else:
                return -inf
        #if maximal depth of recursion is reached, 
        #then return value of the position 
        if depth == 0:
            return self.count_position(board)
        #if it's my turn now, then find the maximal value of a position,
        #that can be reached in one move, and return it
        if maximizingPlayer:
            max_eval = -inf #initial maximal evaluation
            #find my possible moves
            moves = MyPlayer.find_moves(board, self.my_color, self.opp_color)
            #if there is no any moves, then I skip the turn
            if not moves:
                return self.minimax(board, False, depth - 1, alpha, beta)
            #look throw all moves and find the best position
            for move in moves:
                #compute board, which will be reached with the particular move
                new_board = self.update_board(board, move, self.my_color)
                #compute the best evaluation for the particular move
                eval = self.minimax(new_board, False, depth - 1, alpha, beta)
                if eval >= max_eval:
                    max_eval = eval
                    #if it's the upper level of recursion, then
                    #set self.optimal_move on the current move
                    if depth == START_DEPTH:
                        self.optimal_move = move
                #alpha-beta pruning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        #else it's opponent's turn now. Find the minimal value of a position,
        #that can be reached in one move, and return it
        else:
            min_eval = inf  #initial minimal evaluation
            #find opponent's possible moves
            moves = MyPlayer.find_moves(board, self.opp_color, self.my_color)
            #if there is no any moves, then he skips the turn
            if not moves:
                return self.minimax(board, True, depth - 1, alpha, beta)
            #look throw all moves and find the worst position
            for move in moves:
                #compute board, which will be reached with the particular move
                new_board = self.update_board(board, move, self.opp_color)
                #compute the worst evaluation for the particular move
                eval = self.minimax(new_board, True, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                #alpha-beta pruning
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


    def game_finished(self, board):
        #Game is finished, if neither I, nor opponent has any moves
        my_moves = MyPlayer.find_moves(board, self.my_color, self.opp_color)
        if my_moves:
            return False
 
        opp_moves = MyPlayer.find_moves(board, self.opp_color, self.my_color)
        if opp_moves:
            return False

        return True


    def I_won(self, board):
        #I won, if game is finished and I have more stones, than the opponent 
        if not self.game_finished(board):
            return False

        my_stones = 0
        opp_stones = 0
        for line in board:
            for stone in line:
                if stone == self.my_color:
                    my_stones += 1
                elif stone == self.opp_color:
                    opp_stones += 1
        return my_stones > opp_stones


    def count_position(self, board):
        #Function counts evaluation of the particular position.
        #Evaluation = MS + MFV - OS - OFV, where
        #MS - number of my stones, OS - number of opponent's stones,
        #MFV - sum of values of fields, where my stones are placed
        #OFV - sum of values of fields, where opponent's stones are placed
        eval = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                stone = board[i][j]
                if stone == self.my_color:
                    eval += 1
                    eval += FIELDS_VALUES[i][j]
                elif stone == self.opp_color:
                    eval -= 1
                    eval -= FIELDS_VALUES[i][j]
        return eval


    def update_board(self, board, move, color):
        #Function returns board after adding stone (color of stone = color)
        #placed on the field (i, j) = (move[0], move[1])
        
        i, j = move[0], move[1]
        #set second color
        sec_color = self.opp_color
        if color == self.opp_color:
            sec_color = self.my_color
        #create new board
        new_board = deepcopy(board)
        new_board[i][j] = color
        #flip all stones (with second color) in all
        #directions, if they are in a sequence
        for dir_i, dir_j in ALL_DIRECTIONS:
            if MyPlayer.is_sequence(new_board, i, j, dir_i, dir_j, color, sec_color):
                MyPlayer.flip_stones(new_board, i, j, dir_i, dir_j, color)
        return new_board


    @staticmethod
    def flip_stones(board, i, j, dir_i, dir_j, color):
        #Function assumes, that there is a sequence to be fliped
        #from field (i, j) in the direction (dir_i, dir_j). Function
        #changes all stones in this direction to stone with 'color'

        #current stone to be fliped (cur_i, cur_j)
        cur_i = i + dir_i
        cur_j = j + dir_j
        #flip stones until stone with 'color' is encountered 
        while board[cur_i][cur_j] != color:
            board[cur_i][cur_j] = color
            cur_i += dir_i
            cur_j += dir_j
