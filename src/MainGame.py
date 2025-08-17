"""
This file holds the code that runs the entire game and the title screen.
It loads the pictures into the game and draws them onto the screen. It also loads in sound and a .json map. It pulls in
other classes from the other py files so the functions can be used in the game loop. It also pulls from the pygame,
sys, json, and os libraries. It deciphers the .json map and places the tiles on the screen. While the game is
running the visuals will update based on the direction the dog is going. When the game detects that the user completed
the game it will display a congratulation sign.
"""

from everythingbutmain.Sprites import Avatar, AnimationSequence
from everythingbutmain.FunkyFeatures import Artifacts, NPCs, NPCMessage
from everythingbutmain.AdvancedMovement import Ghosts, ObstacleFloat
#from TitleScreen import Title
import sys
import json
import pygame
import os

BASE_IMAGE_DIR = 'artifacts/images/'


def load_picture(file):
    """Loads in only one picture."""
    picture = pygame.image.load(BASE_IMAGE_DIR + file).convert()
    picture.set_colorkey((0, 0, 0))
    return picture


def load_pictures(file):
    """Loads in a sprite."""
    pictures = []
    png_filesNjpg_Files = [f for f in os.listdir(BASE_IMAGE_DIR + file) if f.endswith('.png') or f.endswith('.jpg')]
    for img_name in sorted(png_filesNjpg_Files):
        pictures.append(load_picture(file + '/' + img_name))
    return pictures


ADJACENT_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone', 'cloud', 'magma'}


class Title:
    def __init__(self):
        """The starting screen."""
        pygame.init()
        pygame.display.set_caption('Main Menu')
        self.screen = pygame.display.set_mode((640, 480))

    def write(self, msg, size, color, coordinates):
        # set message, and size
        font = pygame.font.SysFont('Times New Roman', size, bold=True)
        # render font and color
        msgobj = font.render(msg, True, color)
        # display message
        self.screen.blit(msgobj, coordinates)

    def title_screen(self):
        """title screen game loop"""
        while True:
            # display background, start and exit buttons
            self.screen.blit(load_picture("titleBackground.png"), (0, 0))
            start_button = self.screen.blit(load_picture("start.png"), (220, 305))
            exit_button = self.screen.blit(load_picture("exit.png"), (220, 370))

            # write title, start, and exit buttons
            self.write('A Dog\'s Journey', 50, 'white', (140, 100))
            self.write('Home', 50, 'white', (260, 155))
            self.write('Start', 35, 'white', (285, 310))
            self.write('Exit', 35, 'white', (290, 375))

            # get mouse position
            a, b = pygame.mouse.get_pos()

            button_pressed = False
            # event handler for button clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        button_pressed = True

            # check for collisions with buttons
            if start_button.collidepoint(a, b):
                if button_pressed:
                    Adventure().run()

            if exit_button.collidepoint(a, b):
                if button_pressed:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


class Adventure:
    def __init__(self, currentMap='heaven.json'): # change the name of the starting map here
        """Loads in everything for the game and runs the entire game."""
        pygame.init()
        pygame.display.set_caption('Dog\'s Journey Home')
# Music
        self.channel1 = pygame.mixer.Channel(0)
        self.channel1.set_volume(0.4)  # Set volume to 40% of maximum (0.2 is 20%)
        # self.channel1.play(pygame.mixer.Sound('artifacts/backgroundmusic.mp3'))
        
        # for the sounds jumping and falling
        self.channel2 = pygame.mixer.Channel(1)
        self.channel2.set_volume(0.1)

        self.channel3 = pygame.mixer.Channel(2)
        self.channel3.set_volume(0.1)

        # self.channel4 = pygame.mixer.Channel(4)
        #self.channel4.set_volume(0.1)
        self.currentMap = currentMap
        if self.currentMap == 'heaven.json':
            self.channel1.play(pygame.mixer.Sound('artifacts/heaven.mp3'), loops=1 ) # loops 2 times
        if self.currentMap == 'hell.json':
            self.channel1.play(pygame.mixer.Sound('artifacts/backgroundmusic.mp3'), loops=1)
        if self.currentMap == 'map.json':
            self.channel1.play(pygame.mixer.Sound('artifacts/backgroundmusic.mp3'), loops=1)
        if self.currentMap == 'map2.json':
            self.channel1.play(pygame.mixer.Sound('artifacts/backgroundmusic.mp3'), loops=1)
        
# for the game
        self.tile_dimension = 16
        self.tile_layout = {}
        self.exterior_tiles = []
        self.window = pygame.display.set_mode((640, 480))
        self.render_surface = pygame.Surface((320, 240))
        self.character_type = 'avatar'
        self.timer = pygame.time.Clock()
        self.movement_status = [False, False]
        self.resources = {
            'decor': load_pictures('tiles/decor'),
            'grass': load_pictures('tiles/grass'),
            'large_decor': load_pictures('tiles/large_decor'),
            'stone': load_pictures('tiles/stone'),
            'lava': load_pictures('tiles/lava'),
            'magma': load_pictures('tiles/magma'),
            'player': load_picture('entities/player/player.png'),
            
            'background': load_picture('background.jpg'),
            'forest-background': load_picture('forest-background.png'),
            'heaven-sunset': load_picture('heaven-sunset.png'),
            'hell': load_picture('hell-landscape.png'),

            'water': load_pictures('tiles/water'),
            'artifacts': load_pictures('artifacts'),
            'cloud': load_pictures('tiles/cloud'),

            'player/thing': AnimationSequence(load_pictures('entities/player/thing')),
            'player/run': AnimationSequence(load_pictures('entities/player/run'), 4),
            
            'NPC/tomato': AnimationSequence(load_pictures('entities/NPC/tomato')),
            'NPC/Chipmunk': AnimationSequence(load_pictures('entities/NPC/Chipmunk')),
            'NPC/willowisp':AnimationSequence(load_pictures('entities/NPC/willowisp')),
            'NPC/fluffy':AnimationSequence(load_pictures('entities/NPC/fluffy')),
            
            'player/idle': AnimationSequence(load_pictures('entities/player/idle'), 4),
            'player/jump': AnimationSequence(load_pictures('entities/player/jump'), 4),
            'float': load_pictures('float'),
            
            'ghost/down': AnimationSequence(load_pictures('entities/ghost/down'), 0.5),
            'ghost/up': AnimationSequence(load_pictures('entities/ghost/up'), 0.5),
            'ghost/left': AnimationSequence(load_pictures('entities/ghost/left'), 0.5),
            'ghost/right': AnimationSequence(load_pictures('entities/ghost/right'), 0.5),
            'seaMonster': load_picture('entities/seaMonster/0.png'),
            'dove': load_picture('entities/dove/0.png'),
            'dragon': load_picture('entities/dragon/0.png'),
        }
        self.load_game('src/' + self.currentMap)
        self.scroll_offset = [0, 0]
        self.avatar = Avatar(self, 'player', (0, 0), (10, 10), 'thing')
        self.artifacts = Artifacts(self)
        self.chipmunk = NPCs(self, 'NPC/Chipmunk', (742, 6), (16, 16))

        self.tomato = NPCs(self, 'NPC/tomato', (419, 86.1), (16, 16))
        self.wisp = NPCs(self, 'NPC/willowisp', (1359, -26.2), (18, 18)) # this controls where it is
        self.fluffy = NPCs(self, 'NPC/fluffy', (640, 231), (30, 30))
        self.current_animation = self.resources['player/thing'].duplicate()
        self.current_animation_Chipmunk = self.resources['NPC/Chipmunk'].duplicate()
        self.current_animation_tomato = self.resources['NPC/tomato'].duplicate()
        self.current_animation_wisp = self.resources['NPC/willowisp'].duplicate()
        self.current_animation_fluffy = self.resources['NPC/fluffy'].duplicate()
        self.current_action = 'thing'
        if self.currentMap == 'heaven.json':
            self.message = NPCMessage(self, 1359, -100, False)
        if self.currentMap == 'hell.json':
            self.message = NPCMessage(self, 667, 188, False)
        if self.currentMap == 'map.json':
            self.message = NPCMessage(self, 419, 20, False)
        if self.currentMap == 'map2.json':
            self.message = NPCMessage(self, 770, -20, False)
        self.ghosts = Ghosts(self)
        self.obstacle = ObstacleFloat(self, 'float')

    def surrounding_tiles(self, position):
        """Makes sure none of the tiles are on top of each other."""
        tiles = []
        tile_position = (int(position[0] // self.tile_dimension), int(position[1] // self.tile_dimension))
        for offset in ADJACENT_OFFSETS:
            check_position = str(tile_position[0] + offset[0]) + ';' + str(tile_position[1] + offset[1])
            if check_position in self.tile_layout:
                tiles.append(self.tile_layout[check_position])
        return tiles

    def display_congratulations(self, screen):
        """Render the congratulations banner."""
        banner_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())  # hight was 100
        banner_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

        # Draw banner background
        pygame.draw.rect(screen, pygame.Color('gold'), banner_rect)
        pygame.draw.rect(screen, pygame.Color('black'), banner_rect, 5)  # Border

        # Render text
        font = pygame.font.SysFont('Arial', 17, bold=True)  # size was 15
        text_surface = font.render("Congratulations! You reached home!", True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=banner_rect.center)

        # Display text
        screen.blit(text_surface, text_rect)

    def save_game(self, file):
        """Allows the dimensions and exterior tiles to be added to the map."""
        f = open(file, 'w')
        json.dump({'tile_layout': self.tile_layout, 'tile_dimension': self.tile_dimension,
                   'exterior_tiles': self.exterior_tiles}, f)
        f.close()

    def load_game(self, file):
        """Loads in the map."""
        f = open(file, 'r')
        level_data = json.load(f)
        f.close()
        self.tile_layout = level_data['tilemap']
        self.tile_dimension = level_data['tile_size']
        self.exterior_tiles = level_data['offgrid']

    def physics_rectangles(self, position):
        """Sets the solid tiles."""
        rectangles = []
        for tile in self.surrounding_tiles(position):
            if tile['type'] in PHYSICS_TILES:
                rectangles.append(
                    pygame.Rect(tile['pos'][0] * self.tile_dimension, tile['pos'][1] * self.tile_dimension,
                                self.tile_dimension, self.tile_dimension)
                )
        return rectangles

    def render(self, surface, offset=(0, 0)):
        """Puts the tiles on the background."""
        for tile in self.exterior_tiles:
            surface.blit(self.resources[tile['type']][tile['variant']],
                         (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        for x in range(offset[0] // self.tile_dimension, (offset[0] + surface.get_width()) // self.tile_dimension + 1):
            for y in range(offset[1] // self.tile_dimension,
                           (offset[1] + surface.get_height()) // self.tile_dimension + 1):
                location = str(x) + ';' + str(y)
                if location in self.tile_layout:
                    tile = self.tile_layout[location]
                    surface.blit(self.resources[tile['type']][tile['variant']],
                                 (tile['pos'][0] * self.tile_dimension - offset[0],
                                  tile['pos'][1] * self.tile_dimension - offset[1]))

    def run(self):
        """Runs the entire game. Renders all the resources on the visible screen."""
        play_game = True
        while play_game is True:
            # background must be 320X240 
            if self.currentMap == 'heaven.json':
                self.render_surface.blit(self.resources['heaven-sunset'], (0, 0))
            if self.currentMap == 'hell.json':
                # TODO: background
                self.render_surface.blit(self.resources['hell'], (0, 0))
            if self.currentMap == 'map.json':
                self.render_surface.blit(self.resources['background'], (0, 0))
            if self.currentMap == 'map2.json':
                self.render_surface.blit(self.resources['forest-background'], (0, 0))

            if self.avatar.avatar_velocity[1] > 2.5:
                print(self.avatar.position[0], self.avatar.position[1])
                # Check if the sound is not already playing
                if not self.channel3.get_busy():
                    self.channel3.play(pygame.mixer.Sound('artifacts/artifacts_falling.mp3'))

            if self.avatar.position[1] >= 250:
                Adventure(self.currentMap).run()
            self.scroll_offset[0] += (self.avatar.rect().centerx - self.render_surface.get_width() / 2 -
                                      self.scroll_offset[0]) / 30
            self.scroll_offset[1] += (self.avatar.rect().centery - self.render_surface.get_height() / 2 -
                                      self.scroll_offset[1]) / 30
            render_scroll = (int(self.scroll_offset[0]), int(self.scroll_offset[1]))
            self.obstacle.drawObstacle(self.render_surface, distanceFromCamera=render_scroll)
            if self.currentMap == 'heaven.json':
                self.wisp.update_NPC()
                self.wisp.render(self.render_surface, offset=render_scroll)
            if self.currentMap == 'hell.json':
                self.fluffy.update_NPC()
                self.fluffy.render(self.render_surface, offset=render_scroll)
            if self.currentMap == 'map.json':
                self.tomato.update_NPC()
                self.tomato.render(self.render_surface, offset=render_scroll)
            if self.currentMap == 'map2.json':
                self.chipmunk.update_NPC()
                self.chipmunk.render(self.render_surface, offset=render_scroll)
# make wisp a NPC for heaven
            self.render(self.render_surface, offset=render_scroll)
            self.avatar.update_avatar(self.tile_layout, (self.movement_status[1] - self.movement_status[0], 0))
            self.avatar.render(self.render_surface, offset=render_scroll)

            self.artifacts.drawArtifacts(self.render_surface, distanceFromCamera=render_scroll)
            
            if self.wisp.check_collision_with_NPC(self.avatar.rect(), self.render_surface,
                                                    distanceFromCamera=render_scroll) and self.currentMap == 'heaven.json':
                self.message.drawMessage(self.render_surface, distanceFromCamera=render_scroll)
                
                if self.artifacts.canDogMoveOn and not self.currentMap == 'map.json': # change this the hell
                    Adventure('map.json').run()
           
            if self.currentMap == 'heaven.json' and self.avatar.position[1] >= 249:
                Adventure('hell.json').run()

            if self.fluffy.check_collision_with_NPC(self.avatar.rect(), self.render_surface,
                                                    distanceFromCamera=render_scroll) and self.currentMap == 'hell.json':
                self.message.drawMessage(self.render_surface, distanceFromCamera=render_scroll)
                if self.artifacts.canDogMoveOn and not self.currentMap == 'map.json':
                    Adventure('map.json').run()
# making currently 
            if self.tomato.check_collision_with_NPC(self.avatar.rect(), self.render_surface,
                                                    distanceFromCamera=render_scroll) and self.currentMap == 'map.json':
                self.message.drawMessage(self.render_surface, distanceFromCamera=render_scroll)

                if self.artifacts.canDogMoveOn and not self.currentMap == 'map2.json': 
                    Adventure('map2.json').run() 
            
            if self.chipmunk.check_collision_with_NPC(self.avatar.rect(), self.render_surface,
                                                    distanceFromCamera=render_scroll) and self.currentMap == 'map2.json':
                self.message.drawMessage(self.render_surface, distanceFromCamera=render_scroll)

            pygame.display.update()
            self.artifacts.check_collision_with_artifacts(self.avatar.rect())
            self.ghosts.draw_ghosts(self.render_surface, distanceFromCamera=render_scroll)
            self.ghosts.check_collision_with_ghosts(self.avatar.rect())
            if self.ghosts.check_collision_with_ghosts(self.avatar.rect()):
                Adventure(self.currentMap).run()
            if self.currentMap == 'map2.json' and self.avatar.position[0] >= 1004 and self.artifacts.canDogMoveOn:
                self.display_congratulations(self.render_surface)
                # self.channel1.pause()
                # self.channel4.play(pygame.mixer.Sound('artifacts/fireworks.mp3'))
                # self.channel1.unpause()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_status[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement_status[1] = True
                    if event.key == pygame.K_UP:
                        self.channel2.play(pygame.mixer.Sound('artifacts/jump-sound.mp3'))
                        self.avatar.avatar_velocity[1] = -2
                    # exit game back to main menu
                    if event.key == pygame.K_ESCAPE:
                        play_game = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_status[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement_status[1] = False
            self.window.blit(pygame.transform.scale(self.render_surface, self.window.get_size()), (0, 0))
            pygame.display.update()

            self.timer.tick(60)
        if not play_game:
            self.channel1.pause() # stop the background music when esc is hit
            Title().title_screen()


Title().title_screen()
