import random

BLANK = -1
BOARD_SIZE = 8
ALL_DIRECTIONS = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)] 

class MyPlayer:
    '''Very informative comment'''
    def __init__(self, my_color, opponent_color):
        self.name = 'shvaiale'
        self.my_color = my_color
        self.opponent_color = opponent_color
 

    def move(self, board):
        self.possible_moves = dict()
        self.find_possible_moves(board)
        #
        # for key, value in self.possible_moves.items():
        #     print(f"{key} - {value}")
        #
        for move in self.possible_moves:
            return move


    def find_possible_moves(self, board):

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == self.opponent_color:
                    self.possible_moves.update(self.find_nearby_blanks(board, i, j))

        for i, j in self.possible_moves:
            for dir_i, dir_j in ALL_DIRECTIONS:
                self.fill_values(board, i, j, dir_i, dir_j)

        self.final_sifting()


    def find_nearby_blanks(self, board, i, j):
        nearby_blanks = dict()
        for dir_i, dir_j in ALL_DIRECTIONS:
            if self.is_on_board(i + dir_i, j + dir_j) and \
            board[i + dir_i][j + dir_j] == BLANK:
                nearby_blanks[(i + dir_i, j + dir_j)] = [[0,0,0],
                                                         [0,0,0],
                                                         [0,0,0]]
        return nearby_blanks
        

    def fill_values(self, board, i, j, dir_i, dir_j):
        cur_i = i + dir_i
        cur_j = j + dir_j

        if not self.is_on_board(cur_i, cur_j) or \
        board[cur_i][cur_j] != self.opponent_color:
            return

        while self.is_on_board(cur_i, cur_j):
            
            if board[cur_i][cur_j] == BLANK:
                self.possible_moves[(i,j)][1 + dir_i][1 + dir_j] = 0
                return
            
            if board[cur_i][cur_j] == self.opponent_color:
                self.possible_moves[(i,j)][1 + dir_i][1 + dir_j] += 1
                cur_i += dir_i
                cur_j += dir_j
                continue

            if board[cur_i][cur_j] == self.my_color:
                return

        self.possible_moves[(i,j)][1 + dir_i][1 + dir_j] = 0


    def final_sifting(self):
        copy = self.possible_moves.copy()
        for key, value in copy.items():
            points_sum = 0
            for line in value:
                points_sum += sum(line)
            
            if points_sum == 0:
                del self.possible_moves[key]
            else:
                self.possible_moves[key] = points_sum



    def is_on_board(self, a, b):
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
