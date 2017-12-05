import json
import torch
from state import State

class LegalMoveDict:

    def __init__(self):
        file = open('./legal_moves.json')
        json_obj = json.load(file)
        self.dict = json.loads(json_obj)

    def save(self):
        file = open('./legal_moves.json', 'r+')
        file.truncate()
        json_obj = json.dumps(dict(self.dict))
        json.dump(json_obj, file)
        file.close()

    def get_legal_moves_for(self, state):
        key = self.key_from(state)
        if self.dict.get(key, None) is None:
            legal_moves = state.search_for_legal_moves()
            self.dict[key] = list(map(self.key_from, legal_moves))
            return legal_moves
        return list(map(self.state_from, self.dict[key]))

    def key_from(self, state):
        to_move = str(state.to_move)
        if state.last_move is None:
            x = '_'; y = '_'
        else:
            x,y = state.last_move
        last_move = ' ' + str(x) + ' ' + str(y)
        board = self.unroll_into_str(state.board)
        key = to_move + last_move + board
        return key

    def unroll_into_str(self, tensor):
        board_str = ""
        for y in range(8):
            for x in range(8):
                board_str += ' ' + str(tensor[y][x])
        return board_str

    def state_from(self, key):
        state = State()
        key = key.split()
        state.to_move = int(key[0])
        if key[1] == '_':
            state.last_move = None
        else:
            state.last_move = (int(key[1]), int(key[2]))
        state.board = self.roll_up_str(key[3:])
        return state

    def roll_up_str(self, tensor_l):
        v = list(map(float, tensor_l))
        tensor = torch.rand(8,8)
        i = 0
        for y in range(8):
            for x in range(8):
                tensor[y][x] = v[i]
                i += 1
        return tensor


# move_dict = LegalMoveDict()
# state1 = State()
# state1.set(5,3,1)
# state1.pretty_print()
# print(move_dict.key_from(state1))
# print(move_dict.state_from(move_dict.key_from(state1)).board)

# legals = move_dict.get_legal_moves_for(state1)
# for legal in legals:
#     legal.pretty_print()

# print('-------reading-------'); print()

# legals = move_dict.get_legal_moves_for(state1)
# for legal in legals:
#     legal.pretty_print()

# move_dict.save()
