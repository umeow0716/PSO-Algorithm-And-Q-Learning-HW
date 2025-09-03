import json
import random
import numpy as np
import tkinter as tk

from typing import List
from threading import Thread
from mazegame import MazeGame

class QLearning:
    def __init__(self, size: List[int] = [50, 50, 4], epsilon = 0.9):
        self._table = np.zeros(size, dtype=np.float64)
        
        self._root = tk.Tk()
        self._game = MazeGame(self._root)
        
        self._epsilon = epsilon
        
        self._step = 0
    
    def thread_learning(self):
        while True:
            random_val = random.random()
            
            origin_player_pos = self._game.get_player_pos()
            
            if random_val < self._epsilon:
                actions = list(range(4))
                action = random.choice(actions)
            else:
                action = np.argmax(self._table[self._game.get_player_pos()]).item()
                
            self.do_action(action)
            
            if self._game.is_goal():
                reward = 100.0
            elif self._game.is_prev_action_invaild():
                reward = -1.0
            else:
                reward = -0.1
            
            self.update_q(origin_player_pos, action, reward)
            
            if self._game.is_goal():
                print(f'到達終點 花了 {self._step} 步')
                self._step = 0
                self._epsilon = max(0.1, self._epsilon * 0.995) 
                self._game.reset_game()
    
    def update_q(self, origin_player_pos, action, reward, alpha=0.1, gamma=0.9):
        if self._game.is_goal():
            best_next_q = 0
        else:
            best_next_q = np.max(self._table[self._game.get_player_pos()])

        self._table[origin_player_pos[0], origin_player_pos[1], action] += alpha * (
            reward + gamma * best_next_q - self._table[origin_player_pos[0], origin_player_pos[1], action]
        )
        
    def do_action(self, action: int):
        self._step += 1
        if action == 0:
            self._game.move_down()
        elif action == 1:
            self._game.move_right()
        elif action == 2:
            self._game.move_up()
        elif action == 3:
            self._game.move_left()
    
    def game_start(self):
        try:
            thread = Thread(target=self.thread_learning, daemon=True)
            thread.start()
            self._root.mainloop()
        except KeyboardInterrupt:
            open('table.json', 'w', encoding='utf-8').write(json.dumps(self._table.tolist()))

if __name__ == '__main__':
    learn = QLearning()
    learn.game_start()