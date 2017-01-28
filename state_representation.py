import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import itertools
from math import floor
from tqdm import tqdm
import random

N = 4 # board size
M = 4 # mine count

################################################ PART1

N2 = N * N

NUMS = [ord('0')+i for i in range(9)]
UNKNOWN = ord('-')
MINE = ord('X')
BORDER = ord('#')

UNKNOWN_BOARD = np.zeros((N+2, N+2), dtype=np.dtype('b')) + UNKNOWN
def fill_borders(board):
    board[0] = BORDER
    board[N+1] = BORDER
    board[:,0] = BORDER
    board[:,N+1] = BORDER

CORDS = list(itertools.product(range(1, N+1), range(1, N+1)))

def hash_board(board):
    return ''.join(map(chr, board.ravel()))

def print_board(board):
    if (isinstance(board, list)):
        for b in board:
            print_board(b)
            print('~~~~~~~~')
    else:
        print('\n'.join([''.join([chr(cell) for cell in row]) for row in board]))

def gen_mine_boards():
    for comb in itertools.combinations(range(N2), M):
        board = UNKNOWN_BOARD.copy()
        for cord in comb:
            board[CORDS[cord]] = MINE
        fill_borders(board)
        yield board
mine_boards = list(gen_mine_boards())

def gen_board_rotations(board):
    hashes = set()
    for i in range(8):
        h = hash_board(board)
        if h not in hashes:
            yield board
            hashes.add(h)
        board = np.rot90(board)
        if i == 3:
            board = board.T

class EqSet(object):
    def __init__(self, on_new=(lambda x,y: x)):
        self.count = 0
        self.map = {}
        self.items = []
        self.on_new = on_new

    def to_id(self, board):
        h = hash_board(board)
        ret = self.map.get(h, None)
        if ret is None:
            board = board.copy()
            for b in gen_board_rotations(board):
                self.map[hash_board(b)] = self.count
            ret = self.count
            self.items.append(board)
            self.on_new(board, self.count)
            self.count += 1
        return ret

es_mine_boards = EqSet()
for board in mine_boards:
    es_mine_boards.to_id(board)

es_states = EqSet()

def recurse_states(counts, i, mask_limit):
    if (i == N2):
        es_states.to_id(counts)
        return
    cords = CORDS[i]
    count = counts[cords]

    counts[cords] = UNKNOWN
    recurse_states(counts, i+1, mask_limit)

    if count != -1: # not mine
        counts[cords] = NUMS[count]
        recurse_states(counts, i+1, mask_limit)

    if (count > 0 and mask_limit > 0):
        counts[cords] = MINE
        recurse_states(counts, i+1, mask_limit - 1)

    counts[cords] = count

count_filter = np.zeros((3, 3)) + 1
count_filter[1,1] = 0
for board in tqdm(es_mine_boards.items):
    is_mine = board == MINE
    counts = convolve2d(is_mine, count_filter, mode='same').astype(int)
    counts[is_mine] = -1
    fill_borders(counts)
    recurse_states(counts, 0, 0)

print("Game state count: {}".format(es_states.count))

#################################################### Part2
es_actions = EqSet()

for board in tqdm(es_states.items):
    is_unknown = board == UNKNOWN
    is_border = board == BORDER
    is_known = np.logical_not(np.logical_or(is_unknown, is_border))
    counts = convolve2d(is_unknown, count_filter, mode='same').astype(int)
    b = np.zeros_like(board)
    b[is_known] = 10 * counts[is_known] + (board[is_known]-ord('0'))
    b[is_border] = 100
    b[is_unknown] = 101
    for cords in CORDS:
        if board[cords] != UNKNOWN:
            continue
        row, col = cords
        es_actions.to_id(b[row-1:row+2, col-1:col+2])

print(es_actions.count)

#%%
