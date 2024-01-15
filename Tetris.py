import pygame
import os
import sys
import random

tests = False
FPS = 60
screen_width = 800
screen_height = 700
play_width = 300
play_height = 600
tile_size = 25
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height
figures1 = {'S': [['.....',
                   '.....',
                   '..00.',
                   '.00..',
                   '.....'],
                  ['.....',
                   '..0..',
                   '..00.',
                   '...0.',
                   '.....']],
            'Z': [['.....',
                   '.....',
                   '.00..',
                   '..00.',
                   '.....'],
                  ['.....',
                   '..0..',
                   '.00..',
                   '.0...',
                   '.....']],
            'J': [['.....',
                   '.0...',
                   '.000.',
                   '.....',
                   '.....'],
                  ['.....',
                   '..00.',
                   '..0..',
                   '..0..',
                   '.....'],
                  ['.....',
                   '.....',
                   '.000.',
                   '...0.',
                   '.....'],
                  ['.....',
                   '..0..',
                   '..0..',
                   '.00..',
                   '.....']],
            'L': [['.....',
                   '...0.',
                   '.000.',
                   '.....',
                   '.....'],
                  ['.....',
                   '..0..',
                   '..0..',
                   '..00.',
                   '.....'],
                  ['.....',
                   '.....',
                   '.000.',
                   '.0...',
                   '.....'],
                  ['.....',
                   '.00..',
                   '..0..',
                   '..0..',
                   '.....']],
            'I': [['..0..',
                   '..0..',
                   '..0..',
                   '..0..',
                   '.....'],
                  ['.....',
                   '.....',
                   '0000.',
                   '.....',
                   '.....']],
            'O': [['.....',
                   '.....',
                   '.00..',
                   '.00..',
                   '.....']],
            'T': [['.....',
                   '..0..',
                   '.000.',
                   '.....',
                   '.....'],
                  ['.....',
                   '..0..',
                   '..00.',
                   '..0..',
                   '.....'],
                  ['.....',
                   '.....',
                   '.000.',
                   '..0..',
                   '.....'],
                  ['.....',
                   '..0..',
                   '.00..',
                   '..0..',
                   '.....']]}


class Board:
    def __init__(self, play_width, play_height):
        self.width = play_width
        self.height = play_height
        self.board = [[0] * play_width for _ in range(play_height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x = (x - self.left) // self.cell_size
        y = (y - self.top) // self.cell_size
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return x, y

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)


class Tetris:
    def __init__(self):
        # возможные фигруы в тетрисе (игра создана изначально русским программистом на языке Pascal
        # ее название символично ведь каждая фигура состоит из 4 кваратов\
        figures = ["O", "T", "L", "S", "J", "I", "Z"]


class Interface(pygame.sprite.Sprite):
    def __init__(self):  # отрисовка интерфейса при игре
        super().__init__()
        self.image = pygame.Surface([screen_width, screen_height])
        self.image.fill(pygame.Color("black"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 1, 1
        self.draw("GI", self.image)

    def print_text(self, surface, word, size, text_color, x, y):
        if word == "TETRIS":
            font = pygame.font.SysFont("yugothicui", size * tile_size)
            t = font.render("T", 1, pygame.Color("#D30068"), pygame.Color("black"))
            e = font.render("E", 1, pygame.Color("#00737E"), pygame.Color("black"))
            r = font.render("R", 1, pygame.Color("#FF9F00"), pygame.Color("black"))
            i = font.render("I", 1, pygame.Color("#E60042"), pygame.Color("black"))
            s = font.render("S", 1, pygame.Color("#00737E"), pygame.Color("black"))
            tetris = {"t": t, "e": e, "s": s, "r": r, "i": i}
            for i, el in enumerate(list("tetris")):
                if el == "i":
                    screen.blit(tetris[el], (int(tile_size * (9 + i + 0.5)), tile_size))
                else:
                    screen.blit(tetris[el], (tile_size * (9 + i), tile_size))
        else:
            font = pygame.font.SysFont("yugothicui", int(size * tile_size))
            follow = font.render(f"{word}", 0, pygame.Color(text_color), pygame.Color("black"))
            surface.blit(follow, (int(tile_size * x), int(tile_size * y)))

    def draw(self, filename, surface):
        filedata = open(f"data/{filename}.txt", mode="r").read().split("\n")
        indent = 0 if filename == "GI" else 7 * tile_size
        data = [list(line) for line in filedata]
        for y in range(len(data)):  # int(height / tile_size)
            for x in range(len(data[0])):  # int(width / tile_size)
                if data[y][x] in figures.keys():
                    color = figures[data[y][x]]
                    pygame.draw.rect(surface, pygame.Color(color),
                                     (indent + x * tile_size, indent + y * tile_size, tile_size, tile_size),
                                     tile_size // 10)
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


def load_level(tick):
    cur_fig = None
    with open('data/figures.txt', 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    shape = random.choice(list(figures1.keys()))
    figure = random.choice(figures1.get(shape))
    for k in range(len(level_map)):
        last_line_x = set()
        if tick == 1000:
            for j in range(4, -1, -1):
                if '0' in figure[j]:
                    last_line = figure[j]  # ..00.
                    break
            for i in range(5):
                if last_line[i] == '0':
                    last_line_x.append(i)  # (2,3)
            level_last_x = set()
            if level_map[k + 1] in level_map:
                for i in range(5):
                    if level_map[k + 1] == '0':
                        last_line_x.append(i)
            if len(last_line_x.intersection(
                    level_last_x)) == 0:  # если на последней строке фигуры с 0 индекс 0 совпадает
                for i in range(5):  # с индексом 0 на следующей строке файла цикл прекращается
                    new_line = 10 * '.' + figure[i] + 10 * '.'
                    level_map[i] = new_line
                mapFile.close()
                a = open('data/figures.txt', mode='w', encoding='utf-8')
                for el in level_map:
                    a.write(el + '\n')
            else:
                break
            a.close()


def start_screen():
    pass


if __name__ == "__main__":
    figures = {"o": "#0F4FA8", "t": "#FFCA90", "l": "#D30068", "j": "#FF9F00", "s": "#00737E", "z": "#3F92D2",
               "i": "#E60042"}
    pygame.init()
    size = screen_width, screen_height
    screen = pygame.display.set_mode(size)
    board = Board(10, 20)
    pygame.display.set_caption("Tetris")
    icon = pygame.image.load("data\icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    # all_sprites = pygame.sprite.Group()
    # gi = Interface()
    # all_sprites.add(gi)
    load_level()
    fps = 30
    # start_screen()
    running = True
    # if not tests:
    #     score = 1058
    #         while running:
    #             events = pygame.event.get()
    #             for event in events:
    #                 if event.type == pygame.QUIT:
    #                     running = False
    #             screen.fill((0, 0, 0))
    #             # all_sprites.draw(screen)
    #             # gi.print_text(screen, "TETRIS", 2, "red", 9, 1)
    #             # gi.print_text(screen, "By D&E ", 0.5, "white", 22.2, 23.2)
    #             # gi.print_text(screen, "YOUR SCORE", 0.75, "white", 4.2, 22.25)
    #             # gi.print_text(screen, score, 0.75, pygame.Color("#FFAA00"), 6.25, 23.2)
    #             pygame.display.flip()
    #             clock.tick(FPS)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(board.get_cell(event.pos))
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
pygame.quit()
