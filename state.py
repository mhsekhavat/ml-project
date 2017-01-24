import numpy as np

items = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def get_map_from_id(id, width, height):
    game_map = np.zeros(shape=(width, height))
    for i in range(0, len(id)):
        y = i / height
        x = i % height
        game_map[y][x] = id[i]
    for i in range(0, height):
        for j in range(0, width):
            if id[i] in items:
                game_map[i][j] = id[i]
            elif id[i] == 'a':
                game_map[i][j] = -2
            elif id[i] == '9':
                game_map[i][j] = -1
    return game_map


def get_id_from_map(game_map):
    result = ""
    for i in range(0, len(game_map)):
        for j in range(0, len(game_map[i])):
            if game_map[i][j] >= 0:
                result += str(game_map[i][j])
            elif game_map[i][j] == -1:
                result += "9"
            elif game_map[i][j] == -2:
                result += "a"
    return result
