BLANK = -1
BOARD_SIZE = 8
ALL_DIRECTIONS = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)] 
 
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
        #TODO - return None
        move = self.find_optimal_move(board)
        return move
 
 
    def find_possible_moves(self, board):
        #First sifting. I find opponent's stones on the board, then find
        #nearby blanks and write their indexes as KEYS of possible moves
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


    def find_optimal_move(self, board):
        #TODO - strategy
        for move in self.possible_moves:
            return move
 
 
    def find_nearby_blanks(self, board, i, j):
        #I will write matrix 3x3 as a VALUE of a possible moves for now,
        #it will represent points, which I will earn in each direction
        nearby_blanks = dict()

        for dir_i, dir_j in ALL_DIRECTIONS:
            if self.is_on_board(i + dir_i, j + dir_j) and \
            board[i + dir_i][j + dir_j] == BLANK:
                nearby_blanks[(i + dir_i, j + dir_j)] = [[0,0,0],
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
        #I replace matrix with sum of it's elements and
        #delete move, if sum = 0
        copy = self.possible_moves.copy()
        for key, value in copy.items():
            elements_sum = 0
            for line in value:
                elements_sum += sum(line)
             
            if elements_sum == 0:
                del self.possible_moves[key]
            else:
                self.possible_moves[key] = elements_sum
 
 
    def is_on_board(self, a, b):
        #check, if (a, b) is on the board
        return True if 0 <= a < BOARD_SIZE and 0 <= b < BOARD_SIZE else False
 



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
