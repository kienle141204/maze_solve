import tkinter as tk
import numpy as np
import random
from tkinter import PhotoImage
from queue import PriorityQueue
import time


# Biến toàn cục
matrix = None
weights = None  # Ma trận chứa trọng số
max_targets = 1  # Số đích tối đa
target_count = 0  # Số đích hiện tại
cell_size = 20  # Kích thước mỗi ô
delay = 0.05


#####################################################################################################
# A*  start
#####################################################################################################
def heuristics(current, goal):
    """Tính toán khoảng cách Manhattan làm hàm heuristic."""
    return (abs(current[0] - goal[0]) + abs(current[1] - goal[1])) * int(weight_a_entry.get())

def re_path(came_from, current):
    """Tái tạo lại đường đi từ điểm bắt đầu đến đích."""
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)  # Thêm điểm bắt đầu vào
    path.reverse()
    return path


def a_star_weighted(matrix, start, goal):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng đi: lên, xuống, trái, phải

    pq = PriorityQueue()
    pq.put((0, start))  # (f, node)

    g = {start: 0}  # g(n)
    came_from = {}

    while not pq.empty():
        _, current = pq.get()  # Lấy điểm có f(n) nhỏ nhất

        if current == goal:
            path = re_path(came_from, current)
            # Vẽ đường đi sau khi tìm được
            for (x, y) in path:
                draw_path(x, y)
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            # Kiểm tra nếu ô là hợp lệ và có thể đi được (giá trị lớn hơn 0)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and matrix[neighbor[0]][neighbor[1]] != 0:
                new_g = g[current] + weights[neighbor[0]][neighbor[1]]  # Tính g(n) mới

                if neighbor not in g or new_g < g[neighbor]:
                    g[neighbor] = new_g
                    new_f = new_g + heuristics(neighbor, goal)  # f(n) = g(n) + h(n)
                    came_from[neighbor] = current
                    pq.put((new_f, neighbor))  # Thêm điểm vào hàng đợi ưu tiên

                    # Vẽ quá trình kiểm tra (di chuyển đến ô)
                    draw_process(neighbor[0], neighbor[1])

    return None  # Nếu không tìm thấy đường đi


def draw_process(row, col):
    """Vẽ quá trình tìm đường (khi thuật toán kiểm tra ô)."""
    root.update()
    global cell_size, weights
    rows, cols = matrix.shape
    x0, y0 = col * cell_size, row * cell_size
    x1, y1 = (col + 1) * cell_size, (row + 1) * cell_size
    canvas.create_rectangle(x0, y0, x1, y1, fill="yellow", outline="")  # Vẽ ô đang được kiểm tra

    # Hiển thị trọng số của ô
    if weights[row, col] > 0:
        canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(weights[row, col]), fill="blue", font=("Arial", 10))
    time.sleep(delay)


def draw_path(row, col):
    """Vẽ đường đi từ điểm bắt đầu đến đích."""
    root.update()
    global cell_size, weights
    rows, cols = matrix.shape
    x0, y0 = col * cell_size, row * cell_size
    x1, y1 = (col + 1) * cell_size, (row + 1) * cell_size
    canvas.create_rectangle(x0, y0, x1, y1, fill="green", outline="")  # Vẽ ô thuộc đường đi

    # Hiển thị trọng số của ô
    if weights[row, col] > 0:
        canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(weights[row, col]), fill="white", font=("Arial", 10, "bold"))
    time.sleep(delay)


def run_algorithm():
    """Chạy thuật toán A* để tìm đường đi."""
    global matrix
    start = None
    goal = None
    start_found = False

    # Tìm điểm bắt đầu (0,0) và điểm đích (-1)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == -1:
                if not start_found:
                    # Giả sử điểm đầu tiên gặp là điểm bắt đầu
                    start = (i, j)
                    start_found = True  # Đánh dấu là đã tìm thấy điểm bắt đầu
                else:
                    # Lấy điểm còn lại làm điểm kết thúc
                    goal = (i, j)

    if start and goal:
        # Gọi thuật toán A* và vẽ quá trình tìm đường
        path = a_star_weighted(matrix, start, goal)
        if path:
            print("Tìm thấy đường đi:", path)
        else:
            print("Không tìm thấy đường đi.")
    else:
        tk.messagebox.showerror("Lỗi", "Vui lòng đảm bảo có cả điểm bắt đầu và đích trong ma trận!")

#####################################################################################################
# A* end
#####################################################################################################


#####################################################################################################
# dijkstra start
#####################################################################################################
def re_path_djk(came_from, current):
    """Tái tạo lại đường đi từ điểm bắt đầu đến đích."""
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)  # Thêm điểm bắt đầu vào
    path.reverse()
    return path

def dijkstra(matrix, start, goal):
    rows = len(matrix)
    cols = len(matrix[0])
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
            path = re_path_djk(came_from, current)
            # Vẽ đường đi sau khi tìm được
            for (x, y) in path:
                draw_path_djk(x, y)
            return path


        for dx, dy in directions:
            new_state = (current[0] + dx, current[1] + dy)

            if 0 <= new_state[0] < rows and 0 <= new_state[1] < cols:
                wght = weights[new_state[0]][new_state[1]]

                if wght != 0 and new_state not in visited and matrix[new_state[0]][new_state[1]] !=0 :
                    new_dist = current_dist + wght

                    if new_dist < dist.get(new_state, float('inf')):
                        dist[new_state] = new_dist
                        came_from[new_state] = current
                        pq.put((new_dist, new_state))
                        draw_process_djk(new_state[0], new_state[1])

    return None


def draw_process_djk(row, col):
    """Vẽ quá trình tìm đường (khi thuật toán kiểm tra ô)."""
    root.update()
    global cell_size, weights
    rows, cols = matrix.shape
    x0, y0 = col * cell_size, row * cell_size
    x1, y1 = (col + 1) * cell_size, (row + 1) * cell_size
    canvas_clone.create_rectangle(x0, y0, x1, y1, fill="yellow", outline="")

    # Hiển thị trọng số của ô
    if weights[row, col] > 0:
        canvas_clone.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(weights[row, col]), fill="blue", font=("Arial", 10))
    time.sleep(delay)


def draw_path_djk(row, col):
    """Vẽ đường đi từ điểm bắt đầu đến đích."""
    root.update()
    global cell_size, weights
    rows, cols = matrix.shape
    x0, y0 = col * cell_size, row * cell_size
    x1, y1 = (col + 1) * cell_size, (row + 1) * cell_size
    canvas_clone.create_rectangle(x0, y0, x1, y1, fill="green", outline="")

    # Hiển thị trọng số của ô
    if weights[row, col] > 0:
        canvas_clone.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(weights[row, col]), fill="white", font=("Arial", 10, "bold"))
    time.sleep(delay)


def run_algorithm_djk():
    """Chạy thuật toán A* để tìm đường đi."""
    global matrix
    start = None
    goal = None
    start_found = False

    # Tìm điểm bắt đầu (0,0) và điểm đích (-1)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == -1:
                if not start_found:
                    # Giả sử điểm đầu tiên gặp là điểm bắt đầu
                    start = (i, j)
                    start_found = True  # Đánh dấu là đã tìm thấy điểm bắt đầu
                else:
                    # Lấy điểm còn lại làm điểm kết thúc
                    goal = (i, j)

    if start and goal:
        path = dijkstra(matrix, start, goal)
        if path:
            print("Tìm thấy đường đi:", path)
        else:
            print("Không tìm thấy đường đi.")
    else:
        tk.messagebox.showerror("Lỗi", "Vui lòng đảm bảo có cả điểm bắt đầu và đích trong ma trận!")

#####################################################################################################
# dijkstra end
#####################################################################################################

def create_matrix(rows, cols):
    """Tạo ma trận với kích thước tùy chỉnh."""
    global matrix, weights, target_count
    matrix = np.ones((rows, cols), dtype=int)
    weights = np.zeros((rows, cols), dtype=int)
    target_count = 0
    draw_grid()


def draw_grid():
    """Vẽ ma trận lên canvas."""
    global cell_size
    canvas.delete("all")
    rows, cols = matrix.shape
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    cell_size = min(canvas_width // cols, canvas_height // rows)

    # Vẽ các ô trong ma trận
    for i in range(rows):
        for j in range(cols):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = (j + 1) * cell_size, (i + 1) * cell_size
            if matrix[i, j] == 0:  # Tường
                canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="")
                canvas_clone.create_rectangle(x0, y0, x1, y1, fill="black", outline="")

            elif matrix[i, j] == -1:  # Đích
                canvas.create_oval(x0 + cell_size // 4, y0 + cell_size // 4, x1 - cell_size // 4, y1 - cell_size // 4, fill="red", outline="")
                canvas_clone.create_oval(x0 + cell_size // 4, y0 + cell_size // 4, x1 - cell_size // 4, y1 - cell_size // 4, fill="red", outline="")
            else:  # Ô trắng
                canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="")
                canvas_clone.create_rectangle(x0, y0, x1, y1, fill="white", outline="")
                if weights[i, j] > 0:
                    # Hiển thị trọng số trong ô
                    canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(weights[i, j]), fill="blue", font=("Arial", 10))
                    canvas_clone.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(weights[i, j]), fill="blue", font=("Arial", 10))

    # Vẽ viền ngoài cùng của ma trận
    outer_x0, outer_y0 = 0, 0
    outer_x1, outer_y1 = cols * cell_size, rows * cell_size
    canvas.create_rectangle(outer_x0, outer_y0, outer_x1, outer_y1, outline="black", width=1)
    canvas_clone.create_rectangle(outer_x0, outer_y0, outer_x1, outer_y1, outline="black", width=1)


def cell_click(event):
    """Xử lý chọn đích hoặc vẽ tường tại một ô."""
    global matrix, target_count
    col = event.x // cell_size
    row = event.y // cell_size
    if row < matrix.shape[0] and col < matrix.shape[1]:
        if current_mode.get() == "Destination":
            # Kiểm tra số đích không vượt quá giới hạn
            if target_count < max_targets and matrix[row, col] !=0:
                matrix[row, col] = -1
                target_count += 1
                draw_grid()
        elif current_mode.get() == "Wall":
            # Vẽ tường tại ô
            matrix[row, col] = 0
            draw_grid()

def cell_drag(event):
    """Xử lý vẽ tường khi kéo chuột."""
    global matrix
    if current_mode.get() == "Wall":
        col = event.x // cell_size
        row = event.y // cell_size
        if 0 <= row < matrix.shape[0] and 0 <= col < matrix.shape[1]:
            matrix[row, col] = 0
            draw_grid()

def clear_canvas():
    """Xóa canvas và đặt lại ma trận."""
    global target_count, weights
    canvas.delete("all")
    if matrix is not None:
        matrix.fill(1)
    if weights is not None:
        weights.fill(0)
    target_count = 0
    draw_grid()

def set_max_targets(value):
    """Cập nhật số đích tối đa."""
    global max_targets
    max_targets = int(value)

def create_custom_matrix():
    """Tạo ma trận với kích thước do người dùng chọn."""
    try:
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
        create_matrix(rows, cols)
    except ValueError:
        tk.messagebox.showerror("Lỗi", "Vui lòng nhập kích thước hợp lệ!")

def assign_weights():
    """Đánh trọng số ngẫu nhiên cho các ô trắng."""
    try:
        a = int(weight_a_entry.get())
        b = int(weight_b_entry.get())
        if a > b:
            raise ValueError("a phải nhỏ hơn hoặc bằng b")
        global weights
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i, j] == 1:  # Ô trắng
                    weights[i, j] = random.randint(a, b)
        draw_grid()
    except ValueError:
        tk.messagebox.showerror("Lỗi", "Vui lòng nhập khoảng trọng số hợp lệ!")

def on_resize(event):
    """Điều chỉnh lại ma trận khi cửa sổ thay đổi kích thước."""
    draw_grid()

# Giao diện người dùng
root = tk.Tk()
root.title("MAZE SOLVER")
root.geometry("1100x600")

# Khung bên trái (nút bấm và tùy chọn)
button_frame = tk.Frame(root, width=250, bg="#DDDDDD", highlightbackground="#AAAAAA", highlightthickness=1)
button_frame.pack(side="left", fill="y")

# Khung chứa canvas
canvas_frame = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=1)
canvas_frame.pack(side="right", fill="both", expand=True)

# Canvas thứ hai để hiển thị giống canvas chính
canvas_clone = tk.Canvas(canvas_frame, bg="white", highlightthickness=1)
canvas_clone.pack(side="left", fill="both", expand=True)



# Thêm các nút vào khung bên trái
tk.Label(button_frame, text="OPTION", font=("Comic Sans MS", 16, "bold"), bg="#DDDDDD").pack(pady=10)

# Tạo ma trận tùy chỉnh
matrix_size_frame = tk.Frame(button_frame, bg="#DDDDDD")  # Tạo Frame để chứa các widget
matrix_size_frame.pack(pady=5)  # Thêm khoảng cách giữa các phần
tk.Label(matrix_size_frame, text="Size:", bg="#DDDDDD", font=("Comic Sans MS", 12)).pack(side="left", padx=5)
rows_entry = tk.Entry(matrix_size_frame, width=5, font=("Comic Sans MS", 12))
rows_entry.pack(side="left", padx=5)
rows_entry.insert(0, "10")
tk.Label(matrix_size_frame, text="x", bg="#DDDDDD", font=("Comic Sans MS", 12)).pack(side="left", padx=2)
cols_entry = tk.Entry(matrix_size_frame, width=5, font=("Comic Sans MS", 12))
cols_entry.pack(side="left", padx=5)
cols_entry.insert(0, "10")
tk.Button(matrix_size_frame, text="Make", font=("Comic Sans MS", 12, "bold"), command=create_custom_matrix, bg="#4CAF50", fg="white").pack(side="left", padx=10)

target_frame = tk.Frame(button_frame, bg="#DDDDDD")  # Tạo một Frame để chứa Label và Spinbox
target_frame.pack(pady=5)  # Đặt khoảng cách giữa các thành phần bên trong frame và phần khác

tk.Label(target_frame, text="Max destination", bg="#DDDDDD", font=("Comic Sans MS", 12)).pack(side="left", padx=5)  # Gắn Label
target_spinbox = tk.Spinbox(target_frame, from_=1, to=10, width=5, font=("Comic Sans MS", 12), command=lambda: set_max_targets(target_spinbox.get()))
target_spinbox.pack(side="left")  # Gắn Spinbox cạnh Label

# Đánh trọng số
tk.Label(button_frame, text="Weight range(a, b)", bg="#DDDDDD", font=("Comic Sans MS", 12)).pack(pady=5)
weight_a_entry = tk.Entry(button_frame, width=5, font=("Comic Sans MS", 12))
weight_a_entry.pack(pady=2)
weight_a_entry.insert(0, "1")
weight_b_entry = tk.Entry(button_frame, width=5, font=("Comic Sans MS", 12))
weight_b_entry.pack(pady=2)
weight_b_entry.insert(0, "10")
tk.Button(button_frame, text="Generate weight", font=("Comic Sans MS", 12, "bold"), command=assign_weights, bg="#2196F3", fg="white").pack(pady=10)

# Xóa ma trận
tk.Button(button_frame, text="Delete matrix", font=("Comic Sans MS", 12, "bold"), command=clear_canvas, bg="#9E9E9E", fg="white").pack(pady=10)

# Tùy chọn chế độ
current_mode = tk.StringVar(value="Wall")
tk.Label(button_frame, text="Draw mode", bg="#DDDDDD", font=("Comic Sans MS", 12)).pack(pady=5)
mode_menu = tk.OptionMenu(button_frame, current_mode, "Wall", "Destination")
mode_menu.pack(pady=5)

# nút "Chạy thuật toán"
tk.Button(button_frame, text="A* Algorithm", font=("Comic Sans MS", 12, "bold"), command=run_algorithm, bg="#FF5722", fg="white").pack(pady=10)
tk.Button(button_frame, text="Dijkstra Algorithm", font=("Comic Sans MS", 12, "bold"),command= run_algorithm_djk, bg="#FF5722", fg="white").pack(pady=10)

# Canvas để vẽ ma trận
canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.bind("<Button-1>", cell_click)
canvas.bind("<B1-Motion>", cell_drag)

# Đăng ký sự kiện thay đổi kích thước
root.bind("<Configure>", on_resize)

# Khởi tạo ma trận mặc định
create_matrix(10, 10)

# Bắt đầu vòng lặp chính
root.mainloop()
