import tkinter as tk
import json

CELL_SIZE = 12      # 每格大小 (像素)
MAZE_SIZE = 50      # 50x50

MAP_FILE = "map.json"

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("迷宮遊戲")

        self.canvas = tk.Canvas(root, width=CELL_SIZE*MAZE_SIZE, height=CELL_SIZE*MAZE_SIZE, bg="brown")
        self.canvas.pack()

        # 讀取地圖
        with open(MAP_FILE, "r") as f:
            self.maze = json.load(f)

        # 玩家初始位置
        self.player_pos = [1, 1]

        # 終點
        self.goal_pos = [MAZE_SIZE-2, MAZE_SIZE-2]

        self.draw_maze()
        self.draw_goal()
        self.draw_player()
        
        self._prev_invaild_action = False
        self._is_best_move = False

    def draw_maze(self):
        for y in range(MAZE_SIZE):
            for x in range(MAZE_SIZE):
                if self.maze[y][x] == 1:
                    self.canvas.create_rectangle(
                        x*CELL_SIZE, y*CELL_SIZE,
                        (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                        fill="black", outline="")

    def draw_player(self):
        x, y = self.player_pos
        self.player = self.canvas.create_text(
            x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2,
            text="P", fill="blue", font=("Arial", int(CELL_SIZE*0.8), "bold"))

    def draw_goal(self):
        gx, gy = self.goal_pos
        self.goal = self.canvas.create_rectangle(
            gx*CELL_SIZE, gy*CELL_SIZE,
            (gx+1)*CELL_SIZE, (gy+1)*CELL_SIZE,
            fill="gold", outline="")
    
    def get_player_pos(self) -> tuple[int, int]:
        return self.player_pos[0], self.player_pos[1]

    def move(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if 0 <= new_x < MAZE_SIZE and 0 <= new_y < MAZE_SIZE:
            if self.maze[new_y][new_x] == 0:  # 空地才能走
                self._prev_invaild_action = False
                self.player_pos = [new_x, new_y]
                self.canvas.coords(self.player,
                                   new_x*CELL_SIZE+CELL_SIZE//2,
                                   new_y*CELL_SIZE+CELL_SIZE//2)
            else:
                self._prev_invaild_action = True
    
    def is_prev_action_invaild(self):
        return self._prev_invaild_action
    
    def is_goal(self):
        return self.player_pos == self.goal_pos

    def move_up(self, *args, **kwargs): self.move(0, -1)
    def move_down(self, *args, **kwargs): self.move(0, 1)
    def move_left(self, *args, **kwargs): self.move(-1, 0)
    def move_right(self, *args, **kwargs): self.move(1, 0)

    def reset_game(self):
        self._step = 0
        
        new_x = 1
        new_y = 1

        self._prev_invaild_action = False
        self.player_pos = [new_x, new_y]
        self.canvas.coords(self.player,
            new_x*CELL_SIZE+CELL_SIZE//2,
            new_y*CELL_SIZE+CELL_SIZE//2)

if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()
