import random
import numpy as np 

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def create_maze_dfs(self):
        m = self.height
        n = self.width

        maze = np.zeros((2*m + 1, 2*n + 1), dtype=int)

        directions = [(-2,0),(2,0),(0,-2),(0,2)]

        stack = []

        start_x, start_y = 1,1
        stack.append((start_x, start_x))

        while stack:
            x, y = stack[-1]
            neighbors = []
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 < new_x < 2*m and 0 < new_y < 2*n and maze[new_x][new_y] != 1:
                    neighbors.append((new_x, new_y))

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[nx][ny] = 1
                maze[(nx+x)//2][(ny+y)//2] = 1
                stack.append((nx,ny))
            else:
                stack.pop()    
        
        return maze



            
            
