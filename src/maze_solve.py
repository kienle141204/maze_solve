from queue import Queue
from queue import PriorityQueue
import random
import math

def re_path(maze, came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    
    path.reverse()

    return path

def draw_path(maze, path):
    for x, y in path:
        maze[x][y] = 2

# BFS
def bfs(maze, start, goal, blocks=[]):
    rows = len(maze)
    cols = len(maze[0])

    came_from = {} # luu cha cua cac diem trong loi giai

    visited = [[0]*cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    q = Queue()
    qq = []
    q.put(start)
    visited[start[0]][start[1]] = 1

    while not q.empty():
        current = q.get()

        if current == goal:
            return re_path(maze, came_from, current), qq
        
        for dx, dy in directions:
            new_state = (current[0] + dx, current[1] + dy)

            if 0 <= new_state[0] < rows and 0 <= new_state[1] < cols and visited[new_state[0]][new_state[1]] == 0:
                if maze[new_state[0]][new_state[1]] != 0 and (new_state[0], new_state[1]) not in blocks:
                    came_from[new_state] = current
                    visited[new_state[0]][new_state[1]] = 1
                    q.put(new_state)
                    qq.append(new_state)
    return [], None 


# A STAR
def heurictics(a_point, b_point):
    return abs(a_point[0]-b_point[0]) + abs(a_point[1]-b_point[1])

def a_star(maze, start, goal):
    came_from = {}
    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    pq = PriorityQueue()
    qq = []
    pq.put((0,start))

    g = {start : 0}
    f = {start : heurictics(start, goal)}

    while not pq.empty():
        _, current = pq.get()

        if current == goal:
            return re_path(maze, came_from, current), qq

        for dx, dy in directions:
            new_state = (current[0] + dx, current[1] + dy)
            if 0 < new_state[0] < rows and 0 < new_state[1] < cols and maze[new_state[0]][new_state[1]] != 0:
                new_g = g[current] + 1

                if new_g < g.get(new_state, float('inf')):
                    came_from[new_state] = current
                    new_f = new_g + heurictics(new_state, goal)
                    f[new_state] = new_f
                    g[new_state] = new_g
                    pq.put((new_f, new_state))
                    qq.append(new_state)
    return None


def distance_to_checkpoint(maze, check_points, start, goal):
    rows, cols = len(maze), len(maze[0])
    m = len(check_points)

    new_check_points = [start] + check_points + [goal]
    d = {}

    for i in range(m+2):
        for j in range(i+1, m+2):
            distance = 0
            if (new_check_points[i], new_check_points[j]) not in d:
                path,_ = bfs(maze, new_check_points[i], new_check_points[j])
                if path is not None:
                    distance = len(path)
                d[(new_check_points[i], new_check_points[j])] = distance
                d[(new_check_points[j], new_check_points[i])] = distance

    return d
def total_distance(maze, start, goal, check_points,d):
    n = len(check_points)
    res = 0
    res += d[(start, check_points[0])]
    for i in range(n-1):
        res += d[(check_points[i], check_points[i+1])]
    res += d[(check_points[n-1], goal)]

    return res

def simulated_annealing(maze, check_points, start, goal):
    d = distance_to_checkpoint(maze, check_points, start, goal)

    if len(check_points) == 1:
        path = []
        path1, _ = bfs(maze,start, check_points[0], [goal])
        path2, _ = bfs(maze, check_points[0], goal, [start])
        if path1 == [] or path2 ==[]:
            return 0,0,0
        else:
            path = path1[:] + path2[1:]
        # draw_path(maze, path)
        return total_distance(maze, start, goal, check_points, d), check_points, path
    rows, cols = len(maze), len(maze[0])
    T = 1000
    T_min = 0.0001
    cooling_rate = 0.95

    current_checkpoints = check_points[:]
    best_checkpoints = current_checkpoints[:]
    best_cost = total_distance(maze, start, goal, current_checkpoints, d)
    current_t = T

    while current_t > T_min:
        new_checkpoints = current_checkpoints[:]
        i, j = random.sample(range(len(check_points)),2)
        new_checkpoints[i], new_checkpoints[j] = new_checkpoints[j], new_checkpoints[i]

        current_cost = total_distance(maze, start, goal, current_checkpoints, d)
        new_cost = total_distance(maze, start, goal, new_checkpoints, d)
        delta_cost = new_cost - current_cost

        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost/current_t):
            current_checkpoints = new_checkpoints[:]
            if new_cost < best_cost:
                best_cost = new_cost
                best_checkpoints = current_checkpoints[:]

        current_t = current_t * cooling_rate

    if best_checkpoints == []:
        return 0,0,0
    path = []
    path1, _ = bfs(maze, start, best_checkpoints[0],[goal])
    print(path1)
    if path1 == []:
        return 0,0,None
    else:
        path += path1
    for i in range(0, len(best_checkpoints)-1):
        path2, _  = bfs(maze, best_checkpoints[i], best_checkpoints[i+1], [goal])
        if path2 == []:
            return 0,0,None 
        else:
            path += path2[1:]
    path3, _ =bfs(maze, best_checkpoints[-1], goal, [start])
    print(path3)
    if path3 == []:
        return 0,0,None 
    else:
        path += path3[1:]
    # draw_path(maze, path)

    return best_cost, best_checkpoints, path


#####################################################################################################
# Mê cung có trọng số
#####################################################################################################
def a_star_weighted(maze, start, goal):

    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  


    pq = PriorityQueue()
    pq.put((0, start))  

    g = {start: 0}
    came_from = {}

    while not pq.empty():
        _, current = pq.get()  

        if current == goal:
            return re_path(maze, came_from, current)


        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] > 0:
                new_g = g[current] + maze[neighbor[0]][neighbor[1]]

                if neighbor not in g or new_g < g[neighbor]:
                    g[neighbor] = new_g
                    new_f = new_g + heurictics(neighbor, goal)  # f(n) = g(n) + h(n)
                    came_from[neighbor] = current
                    pq.put((new_f, neighbor)) 
    return None  


def dijkstra(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    dist = {start: 0}
    came_from = {}
    pq = PriorityQueue()
    pq.put((0, start))
    visited = set()
    qq = []

    while not pq.empty():
        current_dist, current = pq.get()
        
        if current in visited:
            continue
        
        visited.add(current)
        qq.append(current)
        
        if current == goal:
            return re_path(came_from, current), qq
        
        for dx, dy in directions:
            new_state = (current[0] + dx, current[1] + dy)
            
            if 0 <= new_state[0] < rows and 0 <= new_state[1] < cols:
                weight = maze[new_state[0]][new_state[1]]
                
                if weight != 0 and new_state not in visited:
                    new_dist = current_dist + weight
                    
                    if new_dist < dist.get(new_state, float('inf')):
                        dist[new_state] = new_dist
                        came_from[new_state] = current
                        pq.put((new_dist, new_state))

    return [], []


