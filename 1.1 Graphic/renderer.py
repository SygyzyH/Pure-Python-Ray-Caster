import math

import main
import pygame

import settings

playerHealth = 100
depth_buffer = None


def render_solids(display_surface):
    """
    Renders everything in the "solid" category (i.e anything that needs to be ray-traced).
    :param display_surface: pygame surface
    :return: None
    """

    global depth_buffer
    if depth_buffer is None:
        depth_buffer = [0] * display_surface.get_width()

    map_width = len(main.game_map)
    map_height = len(main.game_map[0])
    for x in range(display_surface.get_width()):
        # figure out the ray angle
        ray_angle = (settings.playerA - settings.FOV / 2) + (x / display_surface.get_width()) * settings.FOV

        # initialize flags
        dist_player_to_wall = 0
        hit_wall = False
        boundary = False
        hit_portal = False
        hit_enemy = False
        last_sector = (-1, -1)

        eye_x = math.sin(ray_angle)
        eye_y = math.cos(ray_angle)

        sector_offset_x = 0
        sector_offset_y = 0
        current_ray_step = settings.RAY_STEP

        # move ray until it hits something
        while not hit_wall and not hit_portal and not hit_enemy:
            # ray acceleration
            dist_player_to_wall += current_ray_step
            if settings.ray_acceleration:
                current_ray_step += settings.RAY_STEP / 20

            # figure out roughly where the ray is at
            test_x = int(sector_offset_x + settings.playerX + eye_x * dist_player_to_wall)
            test_y = int(sector_offset_y + settings.playerY + eye_y * dist_player_to_wall)

            # check if the ray intersects with anything on the map
            if 0 > test_x >= map_width or 0 > test_y >= map_height:
                hit_wall = True
                dist_player_to_wall = settings.DEPTH

            elif dist_player_to_wall > settings.DEPTH:
                hit_wall = True
                dist_player_to_wall = settings.DEPTH

            elif (test_x, test_y) in [_.location for _ in settings.sectors]:
                sector = [_ for _ in settings.sectors if _.location == (test_x, test_y)][0]
                if sector.location != last_sector:
                    sector_offset_x -= sector.location[0] - sector.vector[0]
                    sector_offset_y -= sector.location[1] - sector.vector[1]
                    last_sector = sector.vector

            elif main.game_map[test_y][test_x] == "#":
                hit_wall = True

                # check if corner
                vector = []
                # all 4 corners
                for tx in range(2):
                    for ty in range(2):
                        vy = (test_y - sector_offset_y) + ty - settings.playerY
                        vx = (test_x - sector_offset_x) + tx - settings.playerX
                        d = math.sqrt(vx*vx + vy*vy)
                        dot = (eye_x * vx / d) + (eye_y * vy / d)
                        vector.append((d, dot))

                # sort vector by closest distance
                def sort_vector(e):
                    # sorting function
                    return e[0]
                vector.sort(key=sort_vector)

                if math.acos(vector[0][1]) < settings.BOUND:
                    boundary = True
                if math.acos(vector[1][1]) < settings.BOUND:
                    boundary = True

            elif main.game_map[test_y][test_x] == "@":
                hit_portal = True

            elif main.game_map[test_y][test_x] == "e":
                hit_enemy = True

        ceil = display_surface.get_height() / 2 - display_surface.get_height() / dist_player_to_wall
        flor = display_surface.get_height() - ceil

        # add solid to depth buffer, not including sectors
        depth_buffer[x] = dist_player_to_wall

        # calculate colors based off distance and fade factor
        color = int(settings.MAX_FADE - (dist_player_to_wall / settings.DEPTH * settings.MAX_FADE))
        wall_shade = (color, color, color)

        # if hit a boundary
        if boundary:
            wall_shade = (0, 0, 0)

        if hit_portal:
            wall_shade = (255, 0, 0)

        if hit_enemy:
            wall_shade = (0, 255, 0)

        # optimization for drawing lines instead of by pixel
        pygame.draw.line(display_surface, (0, 0, 0), (x, 0), (x, ceil))
        pygame.draw.line(display_surface, wall_shade, (x, ceil), (x, flor))
        pygame.draw.line(display_surface, (0, 0, 255), (x, flor), (x, display_surface.get_height()))


def render_sprites(display_surface):
    """
    Renders all sprites.
    :param display_surface: pygame surface
    :return: None
    """

    for sprite in settings.sprites:
        image = pygame.image.load("sprites/" + str(sprite.vector[2])).convert_alpha()
        # find distance between sprite and player
        vec_x = sprite.location[0] - settings.playerX
        vec_y = sprite.location[1] - settings.playerY
        distance_from_player = math.sqrt(vec_x * vec_x + vec_y * vec_y)

        eye_x = math.sin(settings.playerA)
        eye_y = math.cos(settings.playerA)

        # calculate sprite angle relatively to player
        sprite_angle = math.pi / 2
        if eye_x != 0:
            sprite_angle = math.atan2(eye_y, eye_x) - math.atan2(vec_y, vec_x)
        if sprite_angle < -math.pi:
            sprite_angle += math.pi * 2
        if sprite_angle > math.pi:
            sprite_angle -= math.pi * 2

        # if sprite is in view of player, render it
        if math.fabs(sprite_angle) < settings.FOV / 2 and .1 <= distance_from_player < settings.DEPTH:
            # find the ceiling of the sprite based on distance (like drawing the walls)
            sprite_ceil = display_surface.get_height() / 2 - display_surface.get_height() / distance_from_player
            # height is just the rest of the screen - floor
            sprite_height = display_surface.get_height() - sprite_ceil * 2
            # finding the width is simply using the height and maintaining aspect ratio of original sprite
            sprite_width = sprite_height / (image.get_height() / image.get_width())
            # finding the middle of the sprite is taking the middle of the relative angle and offsetting it by width
            sprite_midl = ((sprite_angle / (settings.FOV / 2)) / 2 + .5) * display_surface.get_width()
            # find the starting x position by offsetting the middle
            sprite_relative_x = int(sprite_midl - (sprite_width / 2))

            if depth_buffer[int(sprite_midl)] >= distance_from_player:
                # rescale and display final image
                image = pygame.transform.scale(image, (int(sprite_width), int(sprite_height)))
                display_surface.blit(image, (sprite_relative_x, sprite_ceil))
                depth_buffer[int(sprite_midl)] = distance_from_player
