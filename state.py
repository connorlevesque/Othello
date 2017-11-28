import torch

class State:

    def __init__(self):
        self.board = torch.rand(8,8)
        self.board *= 0
        self.set(3,4,1)
        self.set(4,3,1)
        self.set(3,3,2)
        self.set(4,4,2)

    def at(self,x,y):
        return self.board[y][x]

    def set(self,x,y,val):
        self.board[y][x] = val

    def pretty_print(self):
        h_border = '  | | | | | | | | | |'
        v_border = '|'
        print('    0 1 2 3 4 5 6 7')
        print(h_border)
        for y in range(8):
            print(y, v_border, end=' ')
            for x in range(8):
                p = self.at(x,y)
                print(self.player_symbol(p), end=' ')
            print(v_border)
        print(h_border); print()

    def player_symbol(self,n):
        return { 0:'.', 1:'x', 2:'o' }[n]

def main():
    state = State()
    print(state.board)
    state.pretty_print()

if  __name__ =='__main__':main()