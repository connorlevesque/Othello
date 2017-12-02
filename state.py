import torch

class State:

    def __init__(self):
        self.to_move = 1
        self.last_move = None
        self.board = torch.rand(8,8)
        self.board *= 0
        self.set(3,4,1)
        self.set(4,3,1)
        self.set(3,3,2)
        self.set(4,4,2)

    def at(self,x,y):
        if not self.in_bounds(x,y): 
            raise ValueError('Position out of bounds')
        return int(self.board[y][x])

    def set(self,x,y,piece):
        if not self.in_bounds(x,y): 
            raise ValueError('Position out of bounds')
        self.board[y][x] = piece

    def clone(self):
        clone = State()
        clone.to_move = self.to_move
        clone.last_move = self.last_move
        clone.board = self.board.clone()
        return clone

    def friendly(self):
        return self.to_move

    def enemy(self):
        return (self.to_move%2) + 1

    def legal_moves(self):
        move_states = []
        for y in range(8):
            for x in range(8):
                try:
                    move_state = self.try_move(x,y)
                except ValueError:
                    continue
                move_states.append(move_state)
        if len(move_states) == 0:
            pass_state = self.clone()
            pass_state.to_move = self.enemy() 
            pass_state.last_move = None
            move_states.append(pass_state)
        return move_states

    def try_move(self, origin_x, origin_y):
        new_state = self.clone()
        origin = self.at(origin_x, origin_y)
        if origin != 0: 
            raise ValueError('Origin occupied.')

        changed = False
        for adj_x, adj_y in self.adjacent_positions(origin_x, origin_y):
            adj = self.at(adj_x, adj_y)
            if adj != self.enemy(): continue
            try:
                new_state = new_state.ray_flip(origin_x, origin_y, adj_x, adj_y)
            except ValueError:
                continue
            changed = True

        if not changed: 
            raise ValueError('No move found.')
        new_state.to_move = self.enemy()
        new_state.last_move = (origin_x, origin_y)
        return new_state

    def adjacent_positions(self,x,y):
        positions = []
        for dy in [-1,0,1]:
            for dx in [-1,0,1]:
                if dy == dx == 0: continue
                if self.in_bounds(x+dx, y+dy):
                    positions.append([x+dx, y+dy])
        return positions

    def in_bounds(self,x,y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def ray_flip(self, origin_x, origin_y, target_x, target_y):
        #**ADD INBOUNDS CHECK
        new_state = self.clone()
        new_state.set(origin_x, origin_y, self.friendly())
        dx = target_x - origin_x
        dy = target_y - origin_y
        piece = self.at(target_x, target_y)
        while piece != self.friendly():
            if piece == self.enemy(): # flip piece
                new_state.set(target_x, target_y, self.friendly())
            elif piece == 0: # no end piece
                raise ValueError('No bracketing piece.')
            target_x += dx
            target_y += dy
            piece = self.at(target_x, target_y)
        return new_state

    def is_over(self):
        return self.is_full() or self.has_no_moves_left()

    def is_full(self):
        for y in range(8):
            for x in range(8):
                if self.at(x,y) == 0: return False
        return True

    def has_no_moves_left(self):
        next_state = self.legal_moves()[0]
        return self.last_move is None and next_state.last_move is None

    def score(self):
        result = [0,0,0] # winner, p1 score, p2 score
        for y in range(8):
            for x in range(8):
                piece = self.at(x,y)
                if piece != 0: result[piece] += 1
        result[0] = 1 if result[1] > result[2] else 2
        if result[1] == result[2]: result[0] = 0
        return result

    def isomorphisms(self):
        reflections = [self, self.reflect('x'), self.reflect('y'), self.reflect('xy')]
        rotations = []
        for reflection in reflections:
            rotations.append(reflection.rotate_clockwise())
        return reflections + rotations

    def reflect(self, axis):
        reflection = self.clone()
        for y in range(8):
            for x in range(8):
                if   axis ==  'x': reflection.set(7-x,   y, self.at(x,y))
                elif axis ==  'y': reflection.set(x,   7-y, self.at(x,y))
                elif axis == 'xy': reflection.set(7-x, 7-y, self.at(x,y))
        return reflection

    def rotate_clockwise(self):
        rotation = self.clone()
        for y in range(8):
            for x in range(8):
                rotation.set(7-y, x, self.at(x,y))
        return rotation

    def pretty_print(self):
        h_border = ' | | | | | | | | | |    '
        v_border = '|'
        print('   0 1 2 3 4 5 6 7       ', end='')
        if self.last_move is None: 
            print()
        else: 
            print(self.player_symbol(self.enemy()), 'at',
                self.last_move[0], self.last_move[1])
        print(h_border, self.player_symbol(self.to_move), 'to move')
        for y in range(8):
            print('', v_border, end=' ')
            for x in range(8):
                p = self.at(x,y)
                print(self.player_symbol(p), end=' ')
            print(v_border, y, sep=' ')
        print(h_border); print()

    def print_score(self, with_winner=False):
        score = self.score()
        print(self.player_symbol(1),': ', score[1], sep='')
        print(self.player_symbol(2),': ', score[2], sep='')
        if with_winner: print(self.player_symbol(score[0]), 'wins!')

    def player_symbol(self,n):
        return { 0:'.', 1:'x', 2:'o' }[n]


def main():
    state = State()
    print('Starting State:')
    print(state.board)
    state.pretty_print()
    print('Legal Moves:')
    for move_state in state.legal_moves():
        move_state.pretty_print()

    try_state = state.try_move(5,4)
    if not (try_state is None): state = try_state
    print('Isomorphisms:')
    for iso in state.isomorphisms():
        iso.pretty_print()


if  __name__ =='__main__':main()
