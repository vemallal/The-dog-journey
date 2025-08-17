"""
This file holds the code for the enemies and the falling leaves.
The Ghost class controls the movements of the enemies. It draws the enemies on the screen. It also uses the avatar
class to set and update the positions based on the velocity. It also determines if the player has collided with an enemy.
The ObstacleFloat class controls the movement of the leaves. It sets and updates the position of the leaves based on
its position on the y-axis. It also draws the leaves on the screen at a set position.
"""

import pygame
from everythingbutmain.Sprites import Avatar


class Ghosts:
    def __init__(self, game):
        """The logic for the collidable enemies."""
        self.game = game

        # Define ghost properties
        if self.game.currentMap == 'map.json':
            self.ghosts = [
                {'avatar': Avatar(self.game, 'ghost', (100, -35), (16, 16), 'left'), 'x': 100, 'y': -35,
                 'velocity_x': 2, 'range_x': (80, 240)},
                {'avatar': Avatar(self.game, 'ghost', (150, 50), (16, 16), 'left'), 'x': 150, 'y': 50, 'velocity_x': 2,
                 'range_x': (100, 260)},
                {'avatar': Avatar(self.game, 'ghost', (300, 70), (16, 16), 'left'), 'x': 300, 'y': 70, 'velocity_x': 2,
                 'range_x': (200, 400)}
            ]
        if self.game.currentMap == 'hell.json': 
            self.ghosts = [
               {'avatar': Avatar(self.game, 'dragon', (200, -28), (79, 45), 'left'), 'x': 200, 'y': -28,
                 'velocity_x': 2, 'range_x': (37, 248)}, # top (middle for level)
                {'avatar': Avatar(self.game, 'dragon', (270, 189), (79, 45), 'left'), 'x': 270, 'y': 189,
                 'velocity_x': 2,
                 'range_x': (180, 380)}, # where they stop and start Bottom for this
                {'avatar': Avatar(self.game, 'dragon', (160, -80), (79, 45), 'left'), 'x': 160, 'y': -80,
                 'velocity_x': 2,
                 'range_x': (120, 430)} # middle (top one for level)
            ]
        if self.game.currentMap == 'map2.json' or self.game.currentMap == 'heaven.json':

            # Define sea monster and dove properties
            self.ghosts = [
                {'avatar': Avatar(self.game, 'seaMonster', (200, -35), (16, 16), 'left'), 'x': 200, 'y': -35,
                 'velocity_x': 2, 'range_x': (37, 240)},
                {'avatar': Avatar(self.game, 'seaMonster', (150, 50), (16, 16), 'left'), 'x': 150, 'y': 50,
                 'velocity_x': 2,
                 'range_x': (37, 260)},
                {'avatar': Avatar(self.game, 'seaMonster', (300, 70), (16, 16), 'left'), 'x': 300, 'y': 70,
                 'velocity_x': 2,
                 'range_x': (37, 400)}
            ]

    def draw_ghosts(self, screen, distanceFromCamera=(0, 0)):
        """draw the enemies on the screen and move the enemies horizontally."""
        # Move each ghost horizontally within its defined x-axis range
        for ghost in self.ghosts:
            # Update x position based on velocity
            ghost['x'] += ghost['velocity_x']

            # Reverse direction if the ghost hits its horizontal boundary
            if ghost['x'] <= ghost['range_x'][0] or ghost['x'] >= ghost['range_x'][1]:
                ghost['velocity_x'] = -ghost['velocity_x']

            # Set the ghost's position (x, fixed y)
            ghost['avatar'].position = (ghost['x'], ghost['y'])

            # Draw the ghost at its current position
            if self.game.currentMap == 'map.json':
                screen.blit(
                    ghost['avatar'].sprite.current_image(),
                    (int(ghost['x'] - distanceFromCamera[0]), int(ghost['y'] - distanceFromCamera[1]))
                )
            if self.game.currentMap == 'map2.json':
                if ghost['velocity_x'] < 0:
                    flipped_image = pygame.transform.flip(self.game.resources['seaMonster'], True, False)
                    screen.blit(
                        flipped_image,
                        (int(ghost['x'] - distanceFromCamera[0]), int(ghost['y'] - distanceFromCamera[1]))
                    )
                else:
                    screen.blit(
                        self.game.resources['seaMonster'],
                        (int(ghost['x'] - distanceFromCamera[0]), int(ghost['y'] - distanceFromCamera[1]))
                    )
            if self.game.currentMap == 'heaven.json':
                if ghost['velocity_x'] < 0:
                    flipped_image = pygame.transform.flip(self.game.resources['dove'], True, False)
                    screen.blit(
                        flipped_image,
                        (int(ghost['x'] - distanceFromCamera[0]), int(ghost['y'] - distanceFromCamera[1]))
                    )
                else:
                    screen.blit(
                        self.game.resources['dove'],
                        (int(ghost['x'] - distanceFromCamera[0]), int(ghost['y'] - distanceFromCamera[1]))
                    )
            if self.game.currentMap == 'hell.json':
                if ghost['velocity_x'] < 0:
                    flipped_image = pygame.transform.flip(self.game.resources['dragon'], True, False)
                    screen.blit(
                        flipped_image,
                        (int(ghost['x'] - distanceFromCamera[0]), int(ghost['y'] - distanceFromCamera[1]))
                    )
                else:
                    screen.blit(
                        self.game.resources['dragon'],
                        (int(ghost['x'] - distanceFromCamera[0]), int(ghost['y'] - distanceFromCamera[1]))
                    )
        pygame.display.flip()

    def check_collision_with_ghosts(self, player_rect):
        """Check for collisions with any enemy."""
        for ghost in self.ghosts:
            if player_rect.colliderect(ghost['avatar'].rect()):
                return True
        return False


class ObstacleFloat:
    def __init__(self, maingame, floater):
        """Holds the logic for the leaves falling from the trees."""
        self.maingame = maingame
        self.floater = maingame.resources[floater]
        # where the tree is where they start
        if self.maingame.currentMap == 'map.json':
            # Tree Position [189, 70.3]
            self.position = [320.0, 40.0]
            self.pos2 = [174.0, 42.5]
        if self.maingame.currentMap == 'map2.json':
            # Tree Position [689, 6]
            self.position = [689, 6]
        # heaven stars
        # hell fire balls

    def update_pos(self, posx, posy):
        """Allows the leaves to fall down."""
        if self.maingame.currentMap == 'map.json':
            # the movement
            x = self.position[0] + 0.2 / 4
            y = self.position[1] - -0.3 / 2
            self.position = [x, y]

            x2 = self.pos2[0] - 0.2 / 4
            y2 = self.pos2[1] - -0.3 / 2
            self.pos2 = [x2, y2]
        if self.maingame.currentMap == 'map2.json':
            x = self.position[0] + 0.2 / 4
            y = self.position[1] - -0.3 / 2
            self.position = [x, y]

    def drawObstacle(self, surface, distanceFromCamera=(0, 0)):
        """Draws the leaves on the screen and determines their stating positions."""
        if self.maingame.currentMap == 'map.json':
            # puts the leaves for the second visible tree on the screen
            surface.blit(self.floater[0],
                         (self.position[0] + 6 - distanceFromCamera[0] + 20,
                          self.position[1] + 18 - distanceFromCamera[1]))

            surface.blit(self.floater[0],
                         (self.position[0] + 7 - distanceFromCamera[0] - 6, self.position[1] - distanceFromCamera[1]))
            self.update_pos(self.position[0], self.position[1])

            # puts the leaves for the first visible tree
            surface.blit(self.floater[0],
                         (self.pos2[0] + 6 - distanceFromCamera[0] + 20, self.pos2[1] + 18 - distanceFromCamera[1]))

            surface.blit(self.floater[0],
                         (self.pos2[0] + 9 - distanceFromCamera[0], self.pos2[1] - distanceFromCamera[1]))
            self.update_pos(self.pos2[0], self.pos2[1])

            # once the second leaves hit 100.0 they restart
            if self.position[1] >= 100.0:
                self.position = [320.0, 40.0]
                self.update_pos(self.position[0], self.position[1])
            # once the first leaves hit 90.0 they restart
            if self.pos2[1] >= 90.0:
                self.pos2 = [174.0, 42.5]
                self.update_pos(self.pos2[0], self.pos2[1])

        if self.maingame.currentMap == 'map2.json':
            surface.blit(
                self.floater[0],
                (self.position[0] + 6 - distanceFromCamera[0] + 20, self.position[1] + 18 - distanceFromCamera[1])
            )

            surface.blit(
                self.floater[0],
                (self.position[0] + 7 - distanceFromCamera[0] - 6, self.position[1] - distanceFromCamera[1])
            )
            self.update_pos(self.position[0], self.position[1])

            # restart the leaves when they hit 100.0
            if self.position[1] >= 20:
                self.position = [682, 0]
                self.update_pos(self.position[0], self.position[1])
