import random

class MyPlayer:
    '''Very informative comment'''
    def __init__(self, my_color, opponent_color):
        self.name = 'shvaiale'
        self.my_color = my_color
        self.opponent_color = opponent_color
 
    def move(self, board):
        possible_moves = self.find_possible_moves(board)
        move = random.choice(possible_moves)
        return move

    def find_possible_moves(self, board):
        pass




if __name__ == "__main__":
    player = MyPlayer(1, 0)
    print(player.move())
