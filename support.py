from os import walk

import pygame.image


def import_folder(path):
    surface_list = []

    for _, __, image_list in walk(path):
        for image in image_list:
            full_path = f"{path}/{image}"
            surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(surface)

    return surface_list