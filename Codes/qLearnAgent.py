import numpy as np
import operator
import state


def greedy_choose_action(sorted_actions):
    pair = sorted_actions[0]
    return int(pair[0][0]), int(pair[0][1])


class QLearnAgent:
    def __init__(self):
        super().__init__()
        self.q_matrix = {}
        self.alpha = 0.5
        self.discount_factor = 0.5

    def retreive_from_db(self):
        pass

    def choose_action(self, current_game_map):
        current_map = current_game_map
        current_state_id = state.get_id_from_map(current_game_map)
        if current_state_id not in self.q_matrix.keys():
            action_list = self.get_possible_action(game_board=current_map)
            self.q_matrix[current_state_id] = {}
            for i in range(0, len(action_list)):
                self.q_matrix[current_state_id][action_list[i]] = 0.0
        sorted_actions = sorted(self.q_matrix[current_state_id].items(), key=operator.itemgetter(1), reverse=True)
        return greedy_choose_action(sorted_actions)

    def get_possible_action(self, game_board):
        result = []
        for i in range(0, len(game_board)):
            for j in range(0, len(game_board[i])):
                if game_board[i][j] == -1 or game_board[i][j] == -2:
                    result.append(str(j) + str(i))
        return result

    def update_q_value(self, last_state_id, action, next_state_id, reward,next_map):
        # last_state_id = state.get_id_from_map(last_state_map)
        # next_state_id = state.get_id_from_map(next_state_map)
        action_str = str(action[0]) + str(action[1])
        max_value = 0.0
        if next_state_id in self.q_matrix.keys():
            max_next_state = sorted(self.q_matrix[next_state_id].items(), key=operator.itemgetter(1), reverse=True)
            max_value = max_next_state[0][1]
        else:
            action_list = self.get_possible_action(game_board=next_map)
            print("state")
            print(np.matrix(next_map))
            print("posible action:")
            print(action_list)
            self.q_matrix[next_state_id] = {}
            for i in range(0, len(action_list)):
                self.q_matrix[next_state_id][action_list[i]] = 0.0
        # print("last-state-id= ", last_state_id)
        # print("action= ", action)
        # print("next-state-id= ",next_state_id)
        # print("q_matrix=",self.q_matrix)
        self.q_matrix[last_state_id][action_str] += self.alpha * (reward + self.discount_factor * max_value
                                                                  - self.q_matrix[last_state_id][action_str])
        return self.q_matrix[last_state_id][action_str]
