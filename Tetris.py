import pygame
import os
import sys

tests = False
tile_size = 20
FPS = 60


class Tetris:
    def __init__(self):
        # возможные фигруы в тетрисе (игра создана изначально русским программистом на языке Pascal
        # ее название символично ведь каждая фигура состоит из 4 кваратов\
        figures = ["O", "T", "L", "S", "J", "I", "Z"]


class Interface(pygame.sprite.Sprite):
    def __init__(self):  # отрисовка интерфейса при игре
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("black"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 1, 1
        draw("GI", self.image)


def draw(filename, surface):
    filedata = open(f"data/{filename}.txt", mode="r").read().split("\n")
    indent = 0 if filename == "GI" else 7 * tile_size
    data = [list(line) for line in filedata]
    for y in range(len(data)):  # int(height / tile_size)
        for x in range(len(data[0])):  # int(width / tile_size)
            if data[y][x] in figures.keys():
                color = figures[data[y][x]]
                pygame.draw.rect(surface, pygame.Color(color),
                                 (indent + x * tile_size, indent + y * tile_size, tile_size, tile_size), 2)
                p = []  # список расположений вокруг блока (направления по часовым стрелкам)
                # Проверка блока справа и слева
                if x > 0 and x < len(data[0]) - 1:  # int(width / tile_size)
                    if data[y][x + 1] == data[y][x]:
                        p.append(3)
                    if data[y][x - 1] == data[y][x]:
                        p.append(9)
                elif x == 0:
                    if data[y][x + 1] == data[y][x]:
                        p.append(3)
                elif x == len(data[0]) - 1:  # int(width / tile_size)
                    if data[y][x - 1] == data[y][x]:
                        p.append(9)

                if 3 in p and 9 in p:
                    px, p0x = 0, 0
                elif 3 in p:
                    px, p0x = 2, 2
                elif 9 in p:
                    px, p0x = 0, 2
                else:
                    px, p0x = 2, 4

                # Проверка блока сверху и снизу
                if y > 0 and y < len(data) - 1:  # int(height / tile_size)
                    if data[y + 1][x] == data[y][x]:
                        p.append(6)
                    if data[y - 1][x] == data[y][x]:
                        p.append(12)
                elif y == 0:
                    if data[y + 1][x] == data[y][x]:
                        p.append(6)
                elif y == len(data) - 1:  # int(height/ tile_size)
                    if data[y - 1][x] == data[y][x]:
                        p.append(12)

                if 12 in p and 6 in p:
                    py, p0y = 0, 0
                elif 12 in p:
                    py, p0y = 0, 2
                elif 6 in p:
                    py, p0y = 2, 2
                else:
                    py, p0y = 2, 4

            else:
                px = py = p0x = p0y = 0
            pygame.draw.rect(surface, pygame.Color("black"),
                             (indent + x * tile_size + px, indent + y * tile_size + py, tile_size - p0x,
                              tile_size - p0y), 0)

if __name__ == "__main__":
    figures = {"o": "#0F4FA8", "t": "#FFCA90", "l": "#D30068", "j": "#FF9F00", "s": "#00737E", "z": "#3F92D2",
               "i": "#E60042"}
    pygame.init()
    pygame.display.set_caption("Tetris")
    icon = pygame.image.load("data\icon.png")
    pygame.display.set_icon(icon)
    size = width, height = tile_size * 24, tile_size * 24
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    gi = Interface()
    all_sprites.add(gi)
    running = True
    if not tests:
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
