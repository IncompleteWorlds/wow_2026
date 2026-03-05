from dataclasses import dataclass

import pygame


@dataclass
class Exit:
    """Container for exit-related data.

    This represents a single exit in the game world.
    """
    name: str
    room: str
    rectangle: pygame.Rect

