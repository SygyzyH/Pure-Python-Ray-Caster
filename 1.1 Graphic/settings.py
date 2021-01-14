import math

import pygame

import type_enumerator

# structs, these will be loaded once the map is loaded
portals = []
sectors = []
sprites = []
# TODO make enemy AI work with object struct instead of map pointers
enemies = [type_enumerator.GamePiece(type_enumerator.PieceType.ENEMY, (1, 2))]

# hyper-parameters
playerX = 1.000001
playerY = 1.000001
playerA = 0

# hyper-constants
SENSITIVITY = 6
WALKING_SPEED = 4
DEPTH = 16
FOV = math.pi / 4
BOUND = 0.007
RAY_STEP = .0777
MAX_FADE = 230
VISION_GRID_SIZE = 11
SOLIDS = ['#', 'e', 's']

BUTTON_BINDS = {
                pygame.K_SPACE: 0,
                pygame.K_r: 1,
                pygame.K_w: 2,
                pygame.K_s: 3,
                pygame.K_d: 4,
                pygame.K_a: 5
            }

# optimizations
active_raytracing_optimization = False
ray_acceleration = True
