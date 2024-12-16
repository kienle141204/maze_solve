import random
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import time
from utils import save_solution
from __init__ import Maze
from maze_solve import bfs, a_star, simulated_annealing

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_algorithm_results(algorithm, maze, frame, title, points, n=0):
    fig, ax = plt.subplots(figsize=(6, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    frame.config(cursor="tcross")

    ax.imshow(maze, cmap="gray")
    ax.set_title(f"{title}: Click de chon 2 diem Start va Goal")

    # Thông số cho thuật toán
    time_label = ttk.Label(frame, text="Thời gian: --", font=("Arial", 12))
    time_label.pack(pady=5)
    length_label = ttk.Label(frame, text="Độ dài đường đi: --", font=("Arial", 12))
    length_label.pack(pady=5)
    start_label = ttk.Label(frame, text="Start: --", font=("Arial", 12))
    start_label.pack(pady=5)
    goal_label = ttk.Label(frame, text="Goal: --", font=("Arial", 12))
    goal_label.pack(pady=5)

    def on_click(event):
        if n == 0:
            if len(points) < 2:
                x, y = int(round(event.ydata)), int(round(event.xdata))

                if 0 <= x < maze.shape[0] and 0 <= y < maze.shape[1]:
                    if maze[x][y] != 0 and (x, y) not in points:
                        points.append((x,y))
                        if len(points) <= 2:
                            ax.scatter(y, x, c="red", s=25)
                        else:
                            ax.scatter(y, x, c="blue", s=25)
                        canvas.draw()

                        if len(points) == 2:
                            start, goal = points[0] , points[1]
                            print(f"Start: {start}, Goal: {goal}")


                            st = time.time()
                            path, qq = algorithm(maze, start, goal)
                            et = time.time()
                            _time = et - st



                            time_label.config(text=f"Thời gian: {_time:.8f} giây")
                            start_label.config(text=f"Start: {start}")
                            goal_label.config(text=f"Goal: {goal}")

                            if path:
                                path_length = len(path)
                                length_label.config(text=f"Độ dài đường đi: {path_length}")
                                # tôi muốn hoạt ảnh hiển thị trước khi tôi màu đường đi tói ưu
                                colored_maze = maze.copy()

                                def update(frame):
                                    ax.scatter(qq[frame][1], qq[frame][0], c="green", s=25)
                                    canvas.draw()  # Cập nhật canvas sau khi vẽ

                                def draw_path():
                                    for x, y in path:
                                        colored_maze[x][y] = 2
                                    cmap = ListedColormap(["black","white","green"])
                                    ax.imshow(colored_maze, cmap=cmap)
                                    ax.set_title(f"{title}")

                                    for x, y in points:
                                        if (x,y) == points[0] or (x,y)==points[1]:
                                            ax.scatter(y, x, c="red", s=25)
                                        else:
                                            ax.scatter(y,x,c="blue", s=25)
                                    canvas.draw()
                                # Tạo animation
                                if n==0:
                                    ani = FuncAnimation(fig, update, frames=len(qq), interval=100, blit=False, repeat=False)

                                canvas.draw()

                                def on_button_click():
                                    draw_path()

                                button = ttk.Button(frame, text="Hiển thị đường đi", command=on_button_click)
                                button.pack(pady=10)

                                save_solution(maze, start, goal, path, algorithm, _time)
                            else:
                                length_label.config(text="Độ dài đường đi: Không tìm thấy")
                                print("Không tìm thấy đường đi!")
                    else:
                        if (x, y) in points:
                            print("Ô này đã được chọn rồi!")
                        else:
                            print("Hãy chọn các ô trắng!")
                else:
                    print("Điểm chọn ngoài phạm vi mê cung!")
        else:
            if len(points) < 2 + n:
                x, y = int(round(event.ydata)), int(round(event.xdata))

                if 0 <= x < maze.shape[0] and 0 <= y < maze.shape[1]:
                    if maze[x][y] != 0 and (x, y) not in points:
                        points.append((x, y))
                        if len(points) <= 2:
                            ax.scatter(y, x, c="red", s=25)
                        else:
                            ax.scatter(y, x, c="blue", s=25)
                        canvas.draw()

                        if len(points) == 2 + n:
                            start, goal = points[0], points[1]
                            print(f"Start: {start}, Goal: {goal}")


                            st = time.time()
                            _, b, path = simulated_annealing(maze, points[2:], points[0], points[1])
                            print(f"thứ tự đi qua tối ưu là :  start -> {b} -> goal")
                            et = time.time()
                            _time = et - st

                            time_label.config(text=f"Thời gian: {_time:.8f} giây")
                            start_label.config(text=f"Start: {start}")
                            goal_label.config(text=f"Goal: {goal}")

                            if path:
                                print(path)
                                path_length = len(path)
                                length_label.config(text=f"Độ dài đường đi: {path_length}")
                                # tôi muốn hoạt ảnh hiển thị trước khi tôi màu đường đi tói ưu
                                colored_maze = maze.copy()

                                for x, y in path:
                                    colored_maze[x][y] = 2
                                cmap = ListedColormap(["black", "white", "green"])
                                ax.imshow(colored_maze, cmap=cmap)
                                ax.set_title(f"{title}")

                                for x, y in points:
                                    if (x, y) == points[0] or (x, y) == points[1]:
                                        ax.scatter(y, x, c="red", s=25)
                                    else:
                                        ax.scatter(y, x, c="blue", s=25)
                                canvas.draw()
                                save_solution(maze, start, goal, path, algorithm, _time)
                            else:
                                length_label.config(text="Độ dài đường đi: Không tìm thấy")
                                print("Không tìm thấy đường đi!")
                    else:
                        if (x, y) in points:
                            print("Ô này đã được chọn rồi!")
                        else:
                            print("Hãy chọn các ô trắng!")
                else:
                    print("Điểm chọn ngoài phạm vi mê cung!")
    canvas.mpl_connect("button_press_event", on_click)
    return time_label, length_label, start_label, goal_label

def visualize_maze(maze, n):
    root = tk.Tk()
    root.title("akye")
    root.geometry("1200x800")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)


    if n == 0:
        bfs_frame = ttk.Frame(main_frame)
        bfs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        a_star_frame = ttk.Frame(main_frame)
        a_star_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        bfs_points = []
        a_star_points = []

        show_algorithm_results(bfs, maze, bfs_frame, "BFS", bfs_points, n)

        show_algorithm_results(a_star, maze, a_star_frame, "A STAR", a_star_points, n)
    else:
        frame = ttk.Frame(main_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=5)

        _points = []
        show_algorithm_results(bfs, maze, frame,"aaa", _points, n)


    def reset():
        if n==0:
            bfs_points.clear()
            a_star_points.clear()

            for widget in bfs_frame.winfo_children():
                widget.destroy()
            for widget in a_star_frame.winfo_children():
                widget.destroy()

            show_algorithm_results(bfs, maze, bfs_frame, "BFS", bfs_points,n)

            show_algorithm_results(a_star, maze, a_star_frame, "A STAR", a_star_points,n)
        else:
            _points.clear()
            for widget in frame.winfo_children():
                widget.destroy()
            show_algorithm_results(bfs, maze, frame, "aaa", _points, n)

    reset_button = ttk.Button(root, text="Reset", command=reset)
    reset_button.pack(side=tk.BOTTOM, pady=10)

    def on_closing():
        root.destroy()
        plt.close('all')


    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

