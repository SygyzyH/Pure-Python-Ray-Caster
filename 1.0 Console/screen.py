import os
import shutil

os.system('mode con: cols=120 lines=40')
screen_size = shutil.get_terminal_size()


class Screen:
    def __init__(self, default_symbol: chr, invert_y_axis=False):
        self.default_symbol = default_symbol
        self.buffer = [[default_symbol for j in range(screen_size.columns)] for i in range(screen_size.lines)]
        self.inverted = invert_y_axis
        self.screen_size = screen_size

    def set(self, xy: tuple, symbol: chr):
        if self.inverted:
            temp = list(xy)
            temp[1] = screen_size.lines - xy[1]
            xy = tuple(temp)
        self.buffer[xy[1]][xy[0]] = symbol

    def draw(self):
        os.system("cls || clear")
        for i in range(screen_size.lines - 1):
            for j in range(screen_size.columns):
                print(self.buffer[i][j], end='')
            print()
        self.buffer = [[self.default_symbol for j in range(screen_size.columns)] for i in range(screen_size.lines)]


def main():
    sc = Screen(".")
    sc.set((0, 23), "#")
    sc.draw()


if __name__ == "__main__":
    main()
    print(screen_size)

