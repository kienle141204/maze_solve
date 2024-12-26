import json
import os
import numpy as np
import matplotlib.pyplot as plt

def save_solution(maze, start, goal, path, algorithm, _time):
    steps = len(path)
    out_path = f'results/{algorithm.__name__}.json'

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Chuyển maze thành danh sách để JSON có thể xử lý
    maze_list = maze.tolist() if isinstance(maze, np.ndarray) else maze

    # Tạo dữ liệu đầu ra
    solution_data = {
        "maze shape": maze.shape ,
        "start": start,
        "goal": goal,
        "algorithm": algorithm.__name__,
        "steps": steps,
        "solution": [f"{x}, {y}" for x, y in path],
        "execution_time": _time
    }

    # Ghi dữ liệu vào tệp JSON
    with open(out_path, 'w') as json_file:
        json.dump(solution_data, json_file, indent=4)

    print(f'Solution saved to {out_path}')


def matplot(ttime1, ttime2, steps1, steps2, case1, case2):
    labels = [case1, case2]
    
    times = [ttime1, ttime2]
    steps = [steps1, steps2]
    

    x = range(len(labels))
    
    fig, ax = plt.subplots(2, 1, figsize=(8, 8))
    
    # Biểu đồ thời gian
    ax[0].bar(x, times, color=['blue', 'orange'], alpha=0.7)
    ax[0].set_title('Comparison of Execution Times')
    ax[0].set_ylabel('Time (s)')
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(labels)
    
    # Biểu đồ số bước
    ax[1].bar(x, steps, color=['green', 'red'], alpha=0.7)
    ax[1].set_title('Comparison of Steps')
    ax[1].set_ylabel('Steps')
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(labels)
    
    plt.tight_layout()
    plt.show()
