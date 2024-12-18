# import random
# import numpy as np

# class Maze:
#     def __init__(self, width, height):
#         self.width = width  
#         self.height = height  

#     def create_weighted_maze(self, weight_range=(1, 10)):
#         m, n = self.height, self.width


#         maze = np.zeros((2 * m + 1, 2 * n + 1), dtype=int)


#         weights = np.zeros((2 * m + 1, 2 * n + 1), dtype=float)


#         directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]


#         stack = []


#         start_x, start_y = 1, 1
#         maze[start_x][start_y] = 1  
#         weights[start_x][start_y] = random.uniform(*weight_range)  

#         stack.append((start_x, start_y))

#         while stack:
#             x, y = stack[-1]
#             neighbors = []

#             for dx, dy in directions:
#                 nx, ny = x + dx, y + dy
#                 if 0 < nx < 2 * m and 0 < ny < 2 * n and maze[nx][ny] == 0:
#                     neighbors.append((nx, ny))

#             if neighbors:
#                 nx, ny = random.choice(neighbors)

#                 maze[nx][ny] = 1
#                 maze[(x + nx) // 2][(y + ny) // 2] = 1

#                 weights[nx][ny] = random.uniform(*weight_range)
#                 weights[(x + nx) // 2][(y + ny) // 2] = random.uniform(*weight_range)


#                 stack.append((nx, ny))
#             else:

#                 stack.pop()

#         weighted_maze = np.where(maze == 1, weights, 0)

#         return weighted_maze