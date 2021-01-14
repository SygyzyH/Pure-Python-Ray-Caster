import math

import main
import pygame
import settings


def display(surface, elapsed_time):
    """
    Displays the HUD.
    :param surface: pygame surface
    :param elapsed_time: time needed to calculate the FPS
    :return: None
    """

    # display game map
    pygame.draw.rect(surface, (20, 20, 20), pygame.Rect(0, 0, 160, 160))
    for line in range(len(main.game_map)):
        for column in range(len(main.game_map[line])):
            color = (20, 20, 20)
            if main.game_map[column][line] == '#':
                color = (50, 50, 50)
            if main.game_map[column][line] == 'e':
                color = (0, 255, 0)
            if main.game_map[column][line] == '@':
                color = (255, 0, 0)
            pygame.draw.rect(surface, color, pygame.Rect(line * 5, column * 5 + 20, 5, 5))

    # display player location
    pygame.draw.rect(surface, (40, 80, 80),
                     pygame.Rect(int(settings.playerX) * 5, int(settings.playerY) * 5 + 20, 5, 5))
    pygame.draw.line(surface, (40, 80, 80),
                     (int(settings.playerX) * 5 + 2, int(settings.playerY) * 5 + 22),
                     (int(int(settings.playerX) * 5 + 2 + (math.sin(settings.playerA) * 20)),
                      int(int(settings.playerY) * 5 + 22 + (math.cos(settings.playerA) * 20))))

    # display fps, coordinates
    surface.blit(pygame.font.SysFont("Arial", 12)
                 .render("Fps: " + str(int(1 / elapsed_time)) +
                         ", Angle: " + str(int((math.sin(settings.playerA)) * 180)) +
                         ", Location: (" + str(int(settings.playerX)) + ", " + str(int(settings.playerY)) + ")", False,
                         (255, 255, 0)), (0, 0))
