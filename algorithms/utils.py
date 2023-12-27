from enum import Enum

import pygame
from pygame import Color


def set_caption(caption: str) -> None:
    """Set caption for pygame window"""
    pygame.display.set_caption(caption)


def should_quit() -> None:
    """Close pygame window if quit"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


class Colors(Enum):
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    GREY = Color(128, 128, 128)

    START = Color(250, 157, 0)
    END = Color(128, 0, 128)

    OPEN = Color(70, 130, 180)
    CLOSE = Color(92, 192, 219)

    PATH = Color(255, 255, 0)
