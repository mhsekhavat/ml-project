import numpy as np
import matplotlib.pyplot as plt
from math import floor
from tqdm import tqdm

def represent_state(uncovered, mines, n=4):
    ret = np.zeros((n,n))-1

    for (i,j) in mines:
        ret[i,j] = -2

    mask = 1
    for i in range(n):
        for j in range(n):
            if uncovered & mask > 0:
                if ret[i,j] == -2:
                    return None #Invalid: a mine cannot be uncovered
                ret[i,j] = 0
                for di in [-1, 0, 1]:
                    if i+di < 0 or i+di >= n:
                        continue
                    for dj in [-1, 0, 1]:
                        if (di == 0 and dj == 0):
                            continue;
                        if (j+dj < 0 or j+dj >= n):
                            continue
                        if ret[i+di, j+dj] == -2:
                            ret[i,j] += 1
            mask *= 2
    ret[ret == -2] = -1
    return ret

def generate_three_mins(map_size):
    states = []
    for i in range(0, map_size * map_size):
        for j in range(i + 1, map_size * map_size):
            for k in range(j + 1, map_size * map_size):
                states.append([(floor(i / map_size), i % map_size),(floor(j / map_size), j % map_size),(floor(k / map_size), k % map_size)])
    return states

def generate_four_mins(map_size):
    states = []
    for i in range(0, map_size * map_size):
        for j in range(i + 1, map_size * map_size):
            for k in range(j + 1, map_size * map_size):
                for w in range(k+1,map_size*map_size):
                    states.append([(floor(i / map_size), i % map_size),(floor(j / map_size), j % map_size),(floor(k / map_size), k % map_size),(floor(w / map_size), w % map_size)])
    return states

def generate_mines(mine_count, n=4):
    if mine_count == 3:
        return generate_three_mins(n)
    elif mine_count == 4:
        return generate_four_mins(n)
    else:
        raise Exception("Invalid mine count")


def generate_states(mine_counts=[3,4], n=2):
    ret = []
    hashes = set()
    for mine_count in mine_counts:
        for mines in tqdm(generate_mines(mine_count, n)):
            for uncovered in range(2**(n**2)):
                state = represent_state(uncovered, mines, n)
                if state is None:
                    continue
                state_hash = ','.join(map(str, state.ravel()))
                if state_hash not in hashes:
                    ret.append(state)
                    hashes.add(state_hash)
    return ret
