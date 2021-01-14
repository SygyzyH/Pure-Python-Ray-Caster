# By Nadav Hashamai and Jonathan Tuval.
# 9/2020

import math

import enemy_pathfind
from screen import Screen
import keyboard
import time

screen = Screen('.')
running = True
last_time = time.time()

playerX = 2
playerY = 2
playerA = 0
playerHealth = 100

FOV = math.pi / 4
DEPTH = 16
BOUND = 0.007
SPEED = 3

game_map = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],  # Map array
           ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '@', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', 'e', '#', '.', '#', 'e', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '#', '#', '#', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '#', '#', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', 'm', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '#', '#', '#', '#', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
           ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
map_width = len(game_map)
map_height = len(game_map[0])


def main():
    global last_time
    while running:
        current_time = time.time()
        elapsed_time = current_time - last_time
        last_time = current_time

        detect_input(elapsed_time)
        update()
        render()


def render():
    for x in range(screen.screen_size.columns):
        # figure out the ray angle
        ray_angle = (playerA - FOV / 2) + (x / screen.screen_size.columns) * FOV
        dist_player_to_wall = 0
        hit_wall = False
        boundary = False
        hit_portal = False
        hit_enemy = False

        eye_x = math.sin(ray_angle)
        eye_y = math.cos(ray_angle)

        while not hit_wall and not hit_portal and not hit_enemy:
            dist_player_to_wall += .01
            test_x = int(playerX + eye_x * dist_player_to_wall)
            test_y = int(playerY + eye_y * dist_player_to_wall)

            if 0 > test_x >= map_width or 0 > test_y >= map_height:
                hit_wall = True
                dist_player_to_wall = DEPTH
            if dist_player_to_wall > DEPTH:
                hit_wall = True
                dist_player_to_wall = DEPTH

            elif game_map[test_y][test_x] == "#":
                hit_wall = True

                # check if corner
                vector = []
                # all 4 corners
                for tx in range(2):
                    for ty in range(2):
                        vy = test_y + ty - playerY
                        vx = test_x + tx - playerX
                        d = math.sqrt(vx*vx + vy*vy)
                        dot = (eye_x * vx / d) + (eye_y * vy / d)
                        vector.append((d, dot))

                # sort vector by closest distance
                def sort_vector(e):
                    # sorting function
                    return e[0]
                vector.sort(key=sort_vector)

                if math.acos(vector[0][1]) < BOUND:
                    boundary = True
                if math.acos(vector[1][1]) < BOUND:
                    boundary = True

            elif game_map[test_y][test_x] == "@":
                hit_portal = True

            elif game_map[test_y][test_x] == "e":
                hit_enemy = True

        ceil = screen.screen_size.lines / 2 - screen.screen_size.lines / dist_player_to_wall
        flor = screen.screen_size.lines - ceil

        if dist_player_to_wall <= DEPTH / 4:  # very close
            shade = '▓'
        elif dist_player_to_wall < DEPTH / 3:
            shade = '▒'
        elif dist_player_to_wall < DEPTH / 2:
            shade = '▒'
        elif dist_player_to_wall < DEPTH:  # too close
            shade = '░'
        else:
            shade = ' '

        # if hit a boundary
        if boundary:
            shade = ' '

        if hit_portal:
            shade = '@'

        if hit_enemy:
            shade = 'e'

        for y in range(screen.screen_size.lines):
            if y < ceil:
                # draw ceil
                screen.set((x, y), " ")
            elif flor >= y > ceil:
                # draw wall
                screen.set((x, y), shade)
            else:
                # draw floor
                b = 1 - ((y - screen.screen_size.lines / 2) / (screen.screen_size.lines / 2))
                if b < 0.25:  # very close
                    shade = '#'
                elif b < 0.5:
                    shade = 'X'
                elif b < 0.75:
                    shade = '='
                elif b < 0.9:  # too close
                    shade = '-'
                else:
                    shade = '.'
                screen.set((x, y), shade)
    screen.draw()


def detect_input(elapsed_time):
    global running
    global playerA
    global playerX
    global playerY
    if keyboard.is_pressed('a'):
        playerA -= 0.5 * elapsed_time * SPEED
    if keyboard.is_pressed('d'):
        playerA += 0.5 * elapsed_time * SPEED
    if keyboard.is_pressed('w'):
        playerX += math.sin(playerA) * elapsed_time * SPEED
        playerY += math.cos(playerA) * elapsed_time * SPEED
        if game_map[int(playerY)][int(playerX)] == '#':
            playerX -= math.sin(playerA) * elapsed_time * SPEED
            playerY -= math.cos(playerA) * elapsed_time * SPEED
    if keyboard.is_pressed('s'):
        playerX -= math.sin(playerA) * elapsed_time * SPEED
        playerY -= math.cos(playerA) * elapsed_time * SPEED
        if game_map[int(playerY)][int(playerX)] == '#':
            playerX += math.sin(playerA) * elapsed_time * SPEED
            playerY += math.cos(playerA) * elapsed_time * SPEED
    if keyboard.is_pressed('esc'):
        running = False
    print("FPS: " + str(int(1/(elapsed_time if elapsed_time != 0 else 1))) + ", Health:" + str(playerHealth) + ", (" + str("{:.2f}".format(playerX)) + ", " + str("{:.2f}".format(playerY)) + ") ^ " + str(int((math.sin(playerA) + 1) * 180)))


def update():
    global playerX
    global playerY
    global game_map

    # place player in game map
    temp_map = game_map
    game_map[int(playerY)][int(playerX)] = 'p'

    if game_map[int(playerY)][int(playerX)] == '@':
        playerX = 20
        playerY = 20

    # enemy path-find
    for column in range(len(game_map)):  # [[1, 2], [3, 4]] column 1: [2, 4]
        for line in range(len(game_map[column])):  # row 1: [2, 3]
            if game_map[column][line] == 'e':
                # for each enemy, make a map
                enemy_vision = [['#' for i in range(7)] for j in range(7)]
                for j in range(-3, 4):
                    for i in range(-3, 4):
                        if 0 <= column + j < len(game_map) and 0 <= line + i < len(game_map[column]):
                            enemy_vision[3 + j][3 + i] = game_map[column + j][line + i]
                # path-find to next location
                new_location = enemy_pathfind.pathfinder(enemy_vision)
                temp_map[column][line] = '.'
                temp_map[column - 3 + new_location[1]][line - 3 + new_location[0]] = 'e'
    game_map = temp_map


if __name__ == "__main__":
    main()
