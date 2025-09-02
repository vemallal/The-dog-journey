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

