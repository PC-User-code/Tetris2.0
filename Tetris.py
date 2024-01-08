import pygame
import os
import sys

settings = [816, 816, 32]               # width, height, size_title
FPS = 60

class Tetris:
    def __init__(self):
        figures = ["O", "T", "L", "S", "J", "I", "Z"]    # возможные фигруы в тетрисе (игра создана изначально русским программистом на языке Pascal
                                                # ее название символично ведь каждая фигура состоит из 4 кваратов\

class Interface(pygame.sprite.Sprite):
    def __init__(self):             #отрисовка интерфейса при игре
            super().__init__()
            self.image = pygame.Surface([width, height])
            self.image.fill(pygame.Color("black"))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = 1, 1
            pygame.draw.rect(self.image, pygame.Color("#E60042"), (10, 50, tile_size, tile_size * 4), 2)       #I

            pygame.draw.rect(self.image, pygame.Color("#0F4FA8"), (52, 50, tile_size * 2, tile_size * 2), 2)   #O

            pygame.draw.polygon(self.image, pygame.Color("#D30068"),
                                ((126, 50), (126 + tile_size, 50), (126 + tile_size, 50 + tile_size * 2), (126 + tile_size * 2, 50 + tile_size*2),
                                        (126 + tile_size * 2, 50 + tile_size * 3), (126, 50 + tile_size * 3)), 2)   #L

            pygame.draw.polygon(self.image, pygame.Color("#FF9F00"),
                                ((232, 50), (232 + tile_size, 50), (232 + tile_size, 50 + tile_size * 3), (232 - tile_size, 50 + tile_size*3),
                                        (232 - tile_size, 50 + tile_size * 2), (232, 50 + tile_size * 2)), 2)       #J

            pygame.draw.polygon(self.image, pygame.Color("#FFCA90"),
                                ((274, 50), (274 + tile_size, 50), (274 + tile_size, 50 + tile_size), (274 + tile_size * 2, 50 + tile_size),
                                        (274 + tile_size * 2, 50 + tile_size), (274 + tile_size * 2, 50 + tile_size * 2), (274 + tile_size, 50 + tile_size * 2), (274 + tile_size, 50 + tile_size * 3), (274, 50 + tile_size * 3)), 2)# T

            pygame.draw.polygon(self.image, pygame.Color("#00737E"),
                                ((348, 50), (348 + tile_size, 50), (348 + tile_size, 50 + tile_size), (348 + tile_size * 2, 50 + tile_size),
                                 (348 + tile_size * 2, 50 + tile_size * 3), (348 + tile_size * 2, 50 + tile_size * 3), (348 + tile_size, 50 + tile_size * 3),
                                 (348 + tile_size, 50 + tile_size * 2), (348, 50 + tile_size * 2)), 2)  # S

            pygame.draw.polygon(self.image, pygame.Color("#3F92D2"),
                                ((454, 50), (454 + tile_size, 50), (454 + tile_size, 50 + tile_size * 2), (454, 50 + tile_size * 2), (454, 50 + tile_size * 3),
                                 (454 - tile_size, 50 + tile_size * 3), (454 - tile_size, 50 + tile_size), (454, 50 + tile_size)), 2)  # Z

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    icon = pygame.image.load("data\icon.png")
    pygame.display.set_icon(icon)
    size = width, height = settings[0], settings[1]
    tile_size = settings[2]
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    gi = Interface()
    all_sprites.add(gi)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()