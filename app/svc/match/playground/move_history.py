from copy import deepcopy


class MoveHistory(list):

    def move(self, chess_id, from_posi, to_posi, kill_chess_id=None):
        item = {
            'chess_id': chess_id,
            'from_posi': from_posi.to_dict(),
            'to_posi': to_posi.to_dict(),
            'kill_chess_id': kill_chess_id
        }
        self.append(item)

    def retract(self):
        return deepcopy(self.pop())

    def is_empty(self):
        return len(self) == 0

    def to_dict(self):
        return {
            'stack': list(deepcopy(self))
        }

    @staticmethod
    def from_dict(data):
        return MoveHistory([deepcopy(item) for item in data['stack']])
