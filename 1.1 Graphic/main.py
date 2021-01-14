import math
import time

import enemy_pathfind
import hud
import pygame

import map_loader
import renderer
import settings
import type_enumerator
from settings import portals, SENSITIVITY, WALKING_SPEED, active_raytracing_optimization

__author__ = "Nadav 'Rafi' Hashamay"
__credits__ = "Jonathan Tuval"
__version__ = "1.1.0"
__email__ = "loginnada12@gmail.com"

"""
To run the engine, run this file.
This is a 2.5D render of a 2D space. Enemy AI is yet to be implemented. Maps and sprites should 
be in the appropriate folders, but can be freely modified...

Map size can really be anything. Here's a quick explanation of how the engine is structured:
- Portals: teleport the player from their own position to the position specified in their secondary vector.
  The teleportation only changes the integer location of the player, keeping the decimals after the dot the same.
  This makes the teleport seamless, as long as its subtle. how do you make the portal subtle? glad you asked!
- Sectors: just like in the Wolfenstein 3D engine, sectors allow projections of other perspectives.
  The perspective is shifted from their location to their secondary vector. This mechanism allows making non-euclidean
  spaces. If the illusion is setup properly, rooms can look bigger in the inside, or a corridor can look different 
  depending on from where you look at it. Sectors can be made solids in the settings file, or, if used with portals,
  can make the player see and be able to interact with said non-euclidean spaces.
- Sprites: 2D images drawn with perspective in mind, using a technique called "Billboarding" (look it up its kinda cool)
  Billboarding is kinda lazy though, meaning sprites must be radiely symmetrical to make sense.
  
Map file structure:
- The map itself: walls are marked as "#", portals as "@", sectors can be marked as "s". Separate with spaces. Really,
  any sign can be used as empty space, if it helps you mark out what you want in the map. Any sign can also be 
  designated as "SOLID" in the settings file, making it an invisible wall.
- Map data: must always be marked as "d: ", otherwise it will be treated as a map pointer. The map data must contain:
    - Portals
    - Sectors
    - Sprites
  And they should be constructed in this manner:
  d: Portals - (x1, y1): (vectorA1, vectorB1); (x2, y2): (vectorA2, vectorB2);
  Sprites also need an image pointer as vectorC, thus sprites will be formatted in this manner:
  d: Sprites - (x1, y1): (vectorA1, vectorB1, "image_name.png");
  images can be either PNG, JPG, or BMP format.
To change maps, simply call the map_loader and pass the map name as a parameter. for example;
  map_loader("level2")
Try it! but make sure the player isn't inside a wall.

Settings file:
  The settings file contains a lot of variables you can freely change and mess around with, here is a quick explenation:
    Parameters:
      - playerX: starting x for player
      - playerY: starting y for player
      - playerA: starting angle for player
    Constants:
      - SENSITIVITY: mouse sensitivity
      - WALKING_SPEED: walking speed in units (units are completely arbitrary distances)
      - DEPTH: vision depth. Any ray that passes this distance value will be deleted and determined as "infinitely away"
      - FOV: field of view, in radians!
      - BOUND: the bounding angle for two close rays used to draw box outline
      - RAY_STEP: this is no longer constant if active_raytracing_optimization is set to True. This will be the step
        each ray takes every time it has to move forward 
      - MAX_SHADE: the highest shade of grey allowed in the wall coloring equations
      - VISION_GRID_SIZE: not currently used. The vision grid for the enemy AI
      - SOLIDS: a list of all signs the player cannot pass through
      - BUTTON_BINDS: the binds between each button and its actions
    Optimizations:
      - active_raytracing_optimization: uses an algorithm to actively change ray step size based on performance. Can
        cause visual instability in some cases, so its off by default. If you're really struggling to run this, turn
        this on. 
      - ray_acceleration: makes rays accelerate as the move forward by a small fraction of their default RAY_STEP. This
        makes far away objects render less than close ones. Really no downsides, on by default
      - coming soon! (maybe)
      
One more thing: did I mention im lazy?
There's barely, if any, error checking. So if the game crashes, it might be a little difficult to understand what went
wrong and how to fix it. But from my testing, everything is really stable (other than the un-implemented enemy AI), so
usually its not my fault. If it is, let me know - or don't!
"""

game_map = None


class Game:
    def __init__(self):
        """
        Object initialization.
        """

        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self._active_keys = [False, False, False, False, False, False]
        self.elapsed_time = 0
        self.last_enemy_move = self.last_avg_fps = time.time()
        self.avg_fps = (60, 60)

    def on_init(self):
        """
        Initialization function for anything that is not object related
        :return: None
        """

        global game_map
        pygame.init()
        pygame.font.init()
        game_map = map_loader.init()
        pygame.display.set_caption("1995 Doom Like Game Engine")
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA)
        self._running = True

    def on_event(self, event):
        """
        Main event handler. when an event is invoked, this will handle it appropriately.
        :param event: event type
        :return: None
        """

        # handle button bind map
        def set_key(index: int, state: bool):
            if index is not None:
                self._active_keys[index] = state

        if event.type == pygame.KEYDOWN:
            set_key(settings.BUTTON_BINDS.get(event.key), True)
            if event.key == pygame.K_SPACE:
                # shoot gunz
                settings.sprites.append(type_enumerator.GamePiece(type_enumerator.PieceType.SPRITE, (settings.playerX, settings.playerY), (math.sin(settings.playerA) / 2, math.cos(settings.playerA) / 2, "bullet.png")))

        if event.type == pygame.KEYUP:
            set_key(settings.BUTTON_BINDS.get(event.key), False)

        # handle quitting
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.K_ESCAPE == event.key):
            self._running = False

    def move_player(self, offset: int, pos_multiplier: int, starfe_pen: int):
        next_pos_x = settings.playerX + pos_multiplier * \
                     (math.sin(offset + settings.playerA) * (WALKING_SPEED / starfe_pen) * self.elapsed_time)
        next_pos_y = settings.playerY + pos_multiplier * \
                     (math.cos(offset + settings.playerA) * (WALKING_SPEED / starfe_pen) * self.elapsed_time)

        if game_map[int(next_pos_y)][int(next_pos_x)] not in settings.SOLIDS:
            settings.playerX = next_pos_x
            settings.playerY = next_pos_y

    def on_loop(self):
        """
        Main game loop. takes care of player movement and enemy AI.
        :return: None
        """

        # move player angle
        settings.playerA += (.8 * (self.elapsed_time / SENSITIVITY) * pygame.mouse.get_rel()[0]) / SENSITIVITY

        # move player position
        if self._active_keys[2] is True:
            self.move_player(0, 1, 1)
        if self._active_keys[3] is True:
            self.move_player(0, -1, 1)
        if self._active_keys[4] is True:
            self.move_player(90, 1, 2)
        if self._active_keys[5] is True:
            self.move_player(90, -1, 2)

        # move enemies position
        # im too lazy to do this 4 now, i just wanna get a version out
        # maybe ill do it in the future, ask me if you really need it
        if time.time() > self.last_enemy_move:
            self.last_enemy_move = time.time() + 1
            # enemy_pathfind.move_enemy()

        # teleport player in case hes in a portal
        if (int(settings.playerX), int(settings.playerY)) in [portal.location for portal in settings.portals]:
            # get portal the player passed through
            portal = next((_ for _ in settings.portals if _.location == (int(settings.playerX), int(settings.playerY))), None)

            # get player position fraction
            fraction_x = math.modf(settings.playerX)[0]
            fraction_y = math.modf(settings.playerY)[0]

            # change player position based on fraction and portal pointer
            settings.playerX = portal.vector[0] + fraction_x
            settings.playerY = portal.vector[1] + fraction_y

        # sprite management
        for sprite in settings.sprites:
            # move sprite through its vector
            sprite.location = (sprite.location[0] + sprite.vector[0], sprite.location[1] + sprite.vector[1])
            # check if sprite is in bounds and not in a wall
            if sprite.location[0] > len(game_map) or sprite.location[1] > len(game_map[0]) or \
                    game_map[int(sprite.location[1])][int(sprite.location[0])] in settings.SOLIDS:
                settings.sprites.remove(sprite)

    def on_render(self):
        """
        Main renderer. draws HUD, vision, and optimizes rendering.
        :return: None
        """

        # render from renderer
        renderer.render_solids(self._display_surf)

        # render sprites from renderer
        renderer.render_sprites(self._display_surf)

        # display hud
        hud.display(self._display_surf, self.elapsed_time)

        # update display (I love pygame)
        pygame.display.update()

        # optimize renderer based on performance
        fps = 1 / self.elapsed_time
        if time.time() > self.last_avg_fps and active_raytracing_optimization:
            self.last_avg_fps = time.time() + .1
            renderer.RAY_STEP = max(min((1 + -((self.avg_fps[0] / self.avg_fps[1]) / 100 * 2 - 1))/2 * 0.2, 0.2), 0.03)
            self.avg_fps = (1, 1)
        else:
            self.avg_fps = (self.avg_fps[0] + fps, self.avg_fps[1] + 1)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        """
        Main game loop container.
        :return: None
        """

        if self.on_init() is False:
            self._running = False
        last_time = time.time() - 1
        while self._running:
            current_time = time.time()
            self.elapsed_time = current_time - last_time
            last_time = current_time
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    game = Game()
    game.on_execute()
