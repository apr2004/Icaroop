"""
Centralized asset loading.

Before this module existed, every ColumnBase/ColumnBody called
pygame.image.load(...) inside its own __init__. Since a new column pair
spawns roughly every 1.1 seconds (config.COLUMN_FREQUENCY), that meant
re-reading the same PNGs from disk over and over during gameplay.

Here every image is loaded and scaled exactly ONCE, right after
pygame.init(), and the resulting surfaces are handed to the sprites
that need them.
"""
import pygame
import config


class Assets:
    def __init__(self):
        # --- Column pieces (base, shaft, head), already scaled ---
        self.column_base = self._load_scaled("base.png", config.COLUMN_SCALE)
        self.column_shaft = self._load_scaled("fuste.png", config.COLUMN_SCALE)
        self.column_head = self._load_scaled("cabeza.png", config.COLUMN_SCALE)

        # --- Icarus animation frames ---
        self.icarus_frames = [
            pygame.transform.scale(
                pygame.image.load(f"{config.IMAGE_PATH}icarus{num}.png").convert_alpha(),
                (config.ICARUS_WIDTH, config.ICARUS_HEIGHT),
            )
            for num in range(1, 4)
        ]

        # --- Ground / ceiling (scaled to fit config.ENV_HEIGHT, keeping ratio) ---
        self.ground_image = self._load_platform_image("suelo.png")
        self.ceiling_image = self._load_platform_image("techo.jpeg")

        # --- Background (with fallback in case it's missing) ---
        self.background = self._load_background()

    @staticmethod
    def _load_scaled(filename, scale):
        path = f"{config.IMAGE_PATH}{filename}"
        image = pygame.image.load(path).convert_alpha()
        new_width = int(image.get_width() * scale)
        new_height = int(image.get_height() * scale)
        return pygame.transform.scale(image, (new_width, new_height))

    @staticmethod
    def _load_platform_image(filename):
        path = f"{config.IMAGE_PATH}{filename}"
        original = pygame.image.load(path).convert_alpha()
        scale_factor = config.ENV_HEIGHT / original.get_height()
        new_width = int(original.get_width() * scale_factor)
        return pygame.transform.scale(original, (new_width, config.ENV_HEIGHT))

    @staticmethod
    def _load_background():
        try:
            bg = pygame.image.load(f"{config.IMAGE_PATH}fondo.png").convert()
            bg = pygame.transform.scale(bg, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except (pygame.error, FileNotFoundError):
            bg = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            bg.fill((135, 206, 235))
        return bg