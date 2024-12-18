from __init__ import Maze
from maze_solve import bfs, a_star
from utils import save_solution
from visualize import visualize_maze
import pyfiglet
from colorama import init, Fore, Back, Style

# Khởi tạo colorama
init(autoreset=True)

def main():
    print(Fore.CYAN + "#" * 36)
    ascii_art = pyfiglet.figlet_format("Gr 21", font="slant")
    print(Fore.YELLOW + ascii_art)
    print(Fore.CYAN + "#" * 36)
    while True:
        print(Fore.GREEN + "1. Mê cung không trọng số.")
        print(Fore.GREEN + "2. Mê cung có trọng số.")
        print(Fore.MAGENTA + "0. Thoát")

        lc = int(input(Fore.WHITE + "--Lựa chọn của bạn: "))
        print(Fore.CYAN + "#" * 36)
        
        if lc == 1:
            n = int(input(Fore.YELLOW + "Nhập kích thước mê cung bạn muốn: "))
            maze = Maze(n, n)
            maze = maze.create_maze_dfs()

            nn = int(input(Fore.YELLOW + "Nhập số điểm đi qua: "))
            visualize_maze(maze, nn)
        
        elif lc == 2:
            import weighted_maze
        
        elif lc == 0:
            print(Fore.RED + "Đang thoát chương trình...")
            break
        
        else:
            print(Fore.RED + "Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
