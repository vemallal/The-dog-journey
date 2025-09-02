import pygame
import sys


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
        from MainGame import load_picture, Adventure # to avoid curricular import
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

