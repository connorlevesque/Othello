import torch

class State:

    def __init__(self):
        self.to_move = 1
        self.board = torch.rand(8,8)
        self.board *= 0
        self.set(3,4,1)
        self.set(4,3,1)
        self.set(3,3,2)
        self.set(4,4,2)

    def at(self,x,y):
        return self.board[y][x]

    def set(self,x,y,piece):
        self.board[y][x] = piece

    def clone(self):
        clone = State()
        clone.to_move = self.to_move
        clone.board = self.board.clone()
        return clone

    def friendly(self):
        return self.to_move

    def enemy(self):
        return (self.to_move%2) + 1

    def legal_moves(self):
        move_states = []
        for y1 in range(8):
            for x1 in range(8):
                origin = self.at(x1,y1)
                if origin == self.friendly():

                    for x2,y2 in self.adjacent_positions(x1,y1):
                        target = self.at(x2,y2)
                        if target == self.enemy():
                            
                            move_state = self.try_move(x1,y1,x2,y2)
                            if not (move_state is None):
                                move_states.append(move_state)
        if len(move_states) == 0: move_states.append(self)
        return move_states

    def adjacent_positions(self,x,y):
        positions = []
        for dy in [-1,0,1]:
            for dx in [-1,0,1]:
                if dy == dx == 0: continue
                positions.append([x+dx, y+dy])
        return positions

    def try_move(self, origin_x, origin_y, target_x, target_y):
        new_state = self.clone()
        dx = target_x - origin_x
        dy = target_y - origin_y
        piece = self.at(target_x, target_y)
        while piece != 0:
            if piece == self.enemy(): # flip piece
                new_state.set(target_x, target_y, self.friendly())
            elif piece == self.friendly(): # second face found
                return None
            target_x += dx
            target_y += dy
            piece = self.at(target_x, target_y)
        new_state.set(target_x, target_y, self.friendly())
        new_state.to_move = self.enemy()
        return new_state

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
    # state = state.try_move(3,4,4,4)
    print('Starting State:')
    print(state.board)
    state.pretty_print()
    print('Legal Moves:')
    for move_state in state.legal_moves():
        move_state.pretty_print()

if  __name__ =='__main__':main()