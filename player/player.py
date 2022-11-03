#Used materials:
#Wikipedia: https://en.wikipedia.org/wiki/Prisoner%27s_dilemma
#Medium.com: https://medium.com/thinking-is-hard/a-prisoners-dilemma-cheat-sheet-4d85fe289d87
#Plato.standford.edu: https://plato.stanford.edu/entries/prisoner-dilemma/strategy-table.html

import random

DEFECT = True
COOPERATE = False

class MyPlayer:
    '''Player chooses from 5 strategies based on payoff_matrix'''

    def __init__(self, payoff_matrix, number_of_iterations = 1):
        #sets payoff_matrix
        self.payoff_matrix = payoff_matrix
        #R, S, T, P are named like in classic Prisoner's Dilemma
        self.R = self.payoff_matrix[COOPERATE][COOPERATE][0]
        self.S = self.payoff_matrix[COOPERATE][DEFECT][0]
        self.T = self.payoff_matrix[DEFECT][COOPERATE][0]
        self.P = self.payoff_matrix[DEFECT][DEFECT][0]

        self.number_of_iterations = number_of_iterations
        self.my_moves = []              #for recording my previous moves
        self.opponent_moves = []        #for recording opponent's previous moves
        self.strategy = self.choose_strategy()  #chooses strategy
        self.current_iteration = 1      #first iteration is number 1

        self.random_parameter = None    #for repeating_strategy



    def move(self):
        '''Does move according to strategy'''

        move = self.strategy()
        self.current_iteration += 1
        return move
        


    def record_last_moves(self, my_last_move, opponent_last_move):
        '''Records my and opponent's last moves'''

        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)

        

    def choose_strategy(self):
        '''Chooses strategy based on payoff_matrix'''
        
        R = self.R  #for easier reading
        S = self.S
        T = self.T
        P = self.P

        if (T > R) and (P > S):         #if dominant strategy exists
            if P > R:                   #if it's not a dilemma
                return self.spam_defect
            elif 2 * R > T + S:         #if it's an iterated dilemma
                return self.main_strategy
            else:                       #if it's not an iterated dilemma
                return self.repeating_strategy

        elif (T < R) and (P < S):       #all is similar for swaped matrix
            if P < R:
                return self.spam_cooperation
            elif 2 * P > T + S:
                return self.main_strategy
            else:
                return self.repeating_strategy

        else:
            return self.reward_remember_strategy



    def calculate_profitible(self):
        '''Function for reward_remember_strategy'''

        defect_sum = 0
        coop_sum = 0
        my_rewards = []

        #fills array of my rewards and calculates reward sum for defect and cooperation
        for i in range(len(self.my_moves)):
            my_rewards.append(self.payoff_matrix[self.my_moves[i]][self.opponent_moves[i]][0])
            if self.my_moves[i] == DEFECT:
                defect_sum += my_rewards[i]
            else:
                coop_sum += my_rewards[i]

        #selects more profitible move
        if defect_sum > coop_sum:
            return DEFECT
        else:
            return COOPERATE



    '''5 STRATEGIES'''

    def spam_defect(self):
        '''Always defects'''

        return DEFECT



    def spam_cooperation(self):
        '''Always cooperates'''

        return COOPERATE
    


    def repeating_strategy(self):
        '''Tries to synchronize with opponent to get D|C C|D every two rounds'''
        
        move = None

        #Player will randomize his move until he sync with other Player
        if self.current_iteration == 1 or self.my_moves[-1] == self.opponent_moves[-1]:
            self.parameter = random.randint(0, 1)

        #starts to repeat C, D
        if self.parameter % 2 == 0:
            move = COOPERATE
        else:
            move = DEFECT
        
        self.parameter += 1
        return move



    def reward_remember_strategy(self):
        '''Starts with 5 D and 5 C, then chooses more profitible'''

        move = None
        
        if self.current_iteration <= 5:
            move = DEFECT
        elif self.current_iteration <= 10:
            move = COOPERATE
        else:
            move = self.calculate_profitible()

        return move



    def main_strategy(self):
        '''Tit For Two Tats'''

        move = None

        #always cooperates on the first two moves
        if self.current_iteration == 1 or self.current_iteration == 2:
            move = COOPERATE

        #always defects on the last move
        elif self.current_iteration == self.number_of_iterations:
            move = DEFECT

        #defects only when the opponent defects two times in a row
        elif self.opponent_moves[-1] == DEFECT and self.opponent_moves[-2] == DEFECT:
            move = DEFECT
        else:
            move = COOPERATE

        if self.P > self.R: #if it's a swaped matrix
            move = not move

        return move
