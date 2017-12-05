import random
import dhconnelly_othello as dhc
from state import State
from player import Player


class MinimaxPlayer(Player):

    def __init__(self, depth):
        self.depth = depth    
    def play_move(self, state):
        return self.minimax_wrapper(state, self.depth)
    
    def minimax_wrapper(self, state, depth):
        evaluated_options = [self.minimax(option, depth-1, state.to_move) for option in state.legal_moves()]
        return max(evaluated_options, key=lambda o: o[0])[1]

    def minimax(self, state, depth, us):
        if state.is_over():
            score = state.score()
            if us == score[0]: return 1000, state
            else: return -1000, state
        elif depth==0:
            score = state.score()
            score_wrt_us = score[us]-score[self.other_player(us)]
            #print(score_wrt_us)
            #state.pretty_print()
            return score_wrt_us, state
        else:
            availible_states = [self.minimax(st, depth-1, us) for st in state.legal_moves()]
            #for s in availible_states:
                #print('score:',s[0])
                #s[1].pretty_print()
            if state.to_move == us:
                return max(availible_states, key=lambda st: st[0])[0], state
            else:
                return min(availible_states, key=lambda st: st[0])[0], state





    def other_player(self, player):
        return (2-1*(player-1))

def main():
    mm_player = MinimaxPlayer(3)
    mm_player.play_move(State()).pretty_print()
    #tree = MinimaxTree(State(), 3)
    #choice = tree.go(State(), 3, State().to_move)
    #print("-------------choice below_____________________-")
    #choice[0].pretty_print()
    #choice[1].pretty_print()
    #print(choice[2])

if  __name__ =='__main__':main()
