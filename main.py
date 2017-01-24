import time
from random import randint
import qLearnAgent
import pygame
import gui
import state

gui_board = gui.MineSweeperGui(None)

# gui_board.show()
# gui_board.update()
print(" start ")
finish = False
myAgent = qLearnAgent.QLearnAgent()
is_run =True
speed = 1.0

while True:
    speed_scale = 1.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_run,speed_scale = gui_board.mouseDown(pygame.mouse.get_pos())
    if not is_run:
        continue
    if speed/speed_scale != 0:
        speed = speed/speed_scale
        gui_board.speed =speed
    time.sleep(speed)
    x, y = myAgent.choose_action(gui_board.game_map)
    action_tuple = (x, y)
    last_map_id = state.get_id_from_map(gui_board.game_map)
    res, reward = gui_board.select_tile(action_tuple)
    next_state_id = state.get_id_from_map(gui_board.game_map)
    new_value = myAgent.update_q_value(last_state_id=last_map_id, action=action_tuple,
                                       next_state_id=next_state_id, reward=reward,next_map=gui_board.game_map)

    if res == -1:
        time.sleep(speed/10)
        gui_board.restart_game()
        finish = True
    elif res == 2:
        gui_board.restart_game()
        finish = True
        # time.sleep(5)
    gui_board.update_q_value(myAgent.q_matrix[next_state_id])
