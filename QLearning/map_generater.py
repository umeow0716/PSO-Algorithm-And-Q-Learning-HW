import tkinter as tk
import json
import os
import random
from collections import deque

CELL_SIZE = 12      # 每格大小 (像素)
MAZE_SIZE = 50      # 50x50
MAP_FILE = "map.json"

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("迷宮遊戲")

        self.canvas = tk.Canvas(root, width=CELL_SIZE*MAZE_SIZE, height=CELL_SIZE*MAZE_SIZE, bg="brown")
        self.canvas.pack()

        self.generate_valid_map(MAZE_SIZE, MAZE_SIZE)

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

        # 綁定鍵盤
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

    def generate_map(self, width, height):
        """生成隨機地圖 (約 35% 空地)"""
        maze = [[1 for _ in range(width)] for _ in range(height)]
        for y in range(1, height-1):
            for x in range(1, width-1):
                if random.random() > 0.35:  # 35% 空地
                    maze[y][x] = 0
        maze[1][1] = 0
        maze[height-2][width-2] = 0
        return maze

    def is_solvable(self, maze, start, goal):
        """用 BFS 檢查是否能到達終點"""
        q = deque([start])
        visited = set([tuple(start)])
        while q:
            x, y = q.popleft()
            if [x, y] == goal:
                return True
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < MAZE_SIZE and 0 <= ny < MAZE_SIZE:
                    if maze[ny][nx] == 0 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.append((nx, ny))
        return False

    def generate_valid_map(self, width, height):
        """反覆生成直到有通路"""
        while True:
            maze = self.generate_map(width, height)
            if self.is_solvable(maze, [1,1], [width-2, height-2]):
                with open(MAP_FILE, "w") as f:
                    json.dump(maze, f)
                print("✅ 已生成可通關迷宮並儲存到 map.json")
                break

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

    def move(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if 0 <= new_x < MAZE_SIZE and 0 <= new_y < MAZE_SIZE:
            if self.maze[new_y][new_x] == 0:  # 空地才能走
                self.player_pos = [new_x, new_y]
                self.canvas.coords(self.player,
                                   new_x*CELL_SIZE+CELL_SIZE//2,
                                   new_y*CELL_SIZE+CELL_SIZE//2)

                # 判斷是否到達終點
                if self.player_pos == self.goal_pos:
                    self.win_game()

    def move_up(self, event): self.move(0, -1)
    def move_down(self, event): self.move(0, 1)
    def move_left(self, event): self.move(-1, 0)
    def move_right(self, event): self.move(1, 0)

    def win_game(self):
        self.canvas.create_text(MAZE_SIZE*CELL_SIZE//2, MAZE_SIZE*CELL_SIZE//2,
                                text="你贏了！", fill="red", font=("Arial", 40, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()
