import pygame
import os
import sys
import random

pygame.init()
screen_width = 800
screen_height = 700
tetris_width = 300
tetris_height = 600
block_size = 30
mx_left_x = (screen_width - tetris_width) // 2
mx_left_y = screen_height - tetris_height
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
T = [['.....',
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
      '.....'],
     ]
L = [['.....',
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
      '.....']]
J = [['.....',
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
      '.000.', '...0.', '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

figures = [O, T, L, J, S, Z, I]
colors = ["#0F4FA8", "#FFCA90", "#D30068", "#FF9F00", "#00737E", "#3F92D2", "#E60042"]


def create_board(fixed_positions={}):
    grid = [[(255, 255, 255) for x in range(10)] for x in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in fixed_positions:
                c = fixed_positions[(j, i)]

                grid[i][j] = c
    return grid


def draw_board(screen, row, column):
    for i in range(row):
        pygame.draw.line(screen, (0, 0, 0), (mx_left_x, mx_left_y + i * block_size),
                         (mx_left_x + tetris_width, mx_left_y + i * block_size))
        for j in range(column):
            pygame.draw.line(screen, (0, 0, 0), (mx_left_x + j * block_size, mx_left_y),
                             (mx_left_x + j * block_size, mx_left_y + tetris_height))


class Block:

    def __init__(self, column, row, figure):
        self.x = column
        self.y = row
        self.figure = figure
        self.color = colors[figures.index(figure)]
        self.rotation = 0


def change_format(figure):
    cords = []
    format = figure.figure[figure.rotation % len(figure.figure)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                cords.append((figure.x + j, figure.y + i))

    for i, pos in enumerate(cords):
        cords[i] = (pos[0] - 2, pos[1] - 2)

    return cords


def free_cells(shape, grid):
    free_cells = [[(j, i) for j in range(10) if grid[i][j] == (255, 255, 255)] for i in range(20)]
    free_cells = [j for sub in free_cells for j in sub]
    changed = change_format(shape)

    for cord in changed:
        if cord not in free_cells:
            if cord[1] > 0:
                return False

    return True


def game_over(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def new_figure():
    global figures, colors
    return Block(5, 0, random.choice(figures))


def delete_rows(board, fixed, score):
    full_rows = 0
    for i in range(len(board) - 1, -1, -1):
        row = board[i]
        if (255, 255, 255) not in row:
            full_rows += 1
            last_y = i
            score[0] = score[0] + 10
            print(score[0])  # повысить уровень
            for j in range(len(row)):
                del fixed[(j, i)]  # остаются только белые клетки

    if full_rows > 0:
        for key in sorted(list(fixed), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < last_y:
                new_key = (x, y + full_rows)
                fixed[new_key] = fixed.pop(key)


def draw_score(screen, score):
    x = mx_left_x + tetris_width + 50
    y = mx_left_y + tetris_height / 2 - 100
    font = pygame.font.SysFont('yugothicui', 30)
    text = font.render("SCORE", 1, (255, 255, 255))
    score_txt = font.render(str(score[0]), 1, (255, 255, 255))
    screen.blit(text, (x + 35, y + 150))
    screen.blit(score_txt, (x + 70, y + 180))


def draw_app(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('yugothicui', 60)
    text = font.render('T E T R I S', 1, (255, 255, 255))
    screen.blit(text, (mx_left_x + tetris_width / 2 - (text.get_width() / 2), 30))
    for i in range(len(board)):
        for j in range(len(board[i])):
            pygame.draw.rect(screen, board[i][j],
                             (mx_left_x + j * block_size, mx_left_y + i * block_size, block_size, block_size), 0)
    draw_board(screen, 20, 10)


# class Tetris:
#     def __init__(self):
#         # возможные фигруы в тетрисе (игра создана изначально русским программистом на языке Pascal
#         # ее название символично ведь каждая фигура состоит из 4 кваратов\
#         # figures = ["O", "T", "L", "S", "J", "I", "Z"]


# class Interface(pygame.sprite.Sprite):
#     def __init__(self):  # отрисовка интерфейса при игре
#         super().__init__()
#         self.image = pygame.Surface([screen_width, screen_height])
#         self.image.fill(pygame.Color("black"))
#         self.rect = self.image.get_rect()
#         self.rect.x, self.rect.y = 1, 1
#         self.draw("GI", self.image)
#
#     def print_text(self, surface, word, size, text_color, x, y):
#         if word == "TETRIS":
#             font = pygame.font.SysFont("yugothicui", size * tile_size)
#             t = font.render("T", 1, pygame.Color("#D30068"), pygame.Color("black"))
#             e = font.render("E", 1, pygame.Color("#00737E"), pygame.Color("black"))
#             r = font.render("R", 1, pygame.Color("#FF9F00"), pygame.Color("black"))
#             i = font.render("I", 1, pygame.Color("#E60042"), pygame.Color("black"))
#             s = font.render("S", 1, pygame.Color("#00737E"), pygame.Color("black"))
#             tetris = {"t": t, "e": e, "s": s, "r": r, "i": i}
#             for i, el in enumerate(list("tetris")):
#                 if el == "i":
#                     screen.blit(tetris[el], (int(tile_size * (9 + i + 0.5)), tile_size))
#                 else:
#                     screen.blit(tetris[el], (tile_size * (9 + i), tile_size))
#         else:
#             font = pygame.font.SysFont("yugothicui", int(size * tile_size))
#             follow = font.render(f"{word}", 0, pygame.Color(text_color), pygame.Color("black"))
#             surface.blit(follow, (int(tile_size * x), int(tile_size * y)))
#
#     def draw(self, filename, surface):
#         filedata = open(f"data/{filename}.txt", mode="r").read().split("\n")
#         indent = 0 if filename == "GI" else 7 * tile_size
#         data = [list(line) for line in filedata]
#         for y in range(len(data)):  # int(height / tile_size)
#             for x in range(len(data[0])):  # int(width / tile_size)
#                 if data[y][x] in figures.keys():
#                     color = figures[data[y][x]]
#                     pygame.draw.rect(surface, pygame.Color(color),
#                                      (indent + x * tile_size, indent + y * tile_size, tile_size, tile_size),
#                                      tile_size // 10)
#                     p = []  # список расположений вокруг блока (направления по часовым стрелкам)
#                     # Проверка блока справа и слева
#                     if x > 0 and x < len(data[0]) - 1:  # int(width / tile_size)
#                         if data[y][x + 1] == data[y][x]:
#                             p.append(3)
#                         if data[y][x - 1] == data[y][x]:
#                             p.append(9)
#                     elif x == 0:
#                         if data[y][x + 1] == data[y][x]:
#                             p.append(3)
#                     elif x == len(data[0]) - 1:  # int(width / tile_size)
#                         if data[y][x - 1] == data[y][x]:
#                             p.append(9)
#
#                     if 3 in p and 9 in p:
#                         px, p0x = 0, 0
#                     elif 3 in p:
#                         px, p0x = 2, 2
#                     elif 9 in p:
#                         px, p0x = 0, 2
#                     else:
#                         px, p0x = 2, 4
#
#                     # Проверка блока сверху и снизу
#                     if y > 0 and y < len(data) - 1:  # int(height / tile_size)
#                         if data[y + 1][x] == data[y][x]:
#                             p.append(6)
#                         if data[y - 1][x] == data[y][x]:
#                             p.append(12)
#                     elif y == 0:
#                         if data[y + 1][x] == data[y][x]:
#                             p.append(6)
#                     elif y == len(data) - 1:  # int(height/ tile_size)
#                         if data[y - 1][x] == data[y][x]:
#                             p.append(12)
#
#                     if 12 in p and 6 in p:
#                         py, p0y = 0, 0
#                     elif 12 in p:
#                         py, p0y = 0, 2
#                     elif 6 in p:
#                         py, p0y = 2, 2
#                     else:
#                         py, p0y = 2, 4
#
#                 else:
#                     px = py = p0x = p0y = 0
#                 pygame.draw.rect(surface, pygame.Color("black"),
#                                  (indent + x * tile_size + px, indent + y * tile_size + py, tile_size - p0x,
#                                   tile_size - p0y), 0)


# def load_level(tick):
#     cur_fig = None
#     with open('data/figures.txt', 'r') as mapFile:
#         level_map = [line.strip() for line in mapFile]
#     shape = random.choice(list(figures.keys()))
#     figure = random.choice(figures.get(shape))
#     for k in range(len(level_map)):
#         last_line_x = set()
#         if tick == 1000:
#             for j in range(4, -1, -1):
#                 if '0' in figure[j]:
#                     last_line = figure[j]  # ..00.
#                     break
#             for i in range(5):
#                 if last_line[i] == '0':
#                     last_line_x.append(i)  # (2,3)
#             level_last_x = set()
#             if level_map[k + 1] in level_map:
#                 for i in range(5):
#                     if level_map[k + 1] == '0':
#                         last_line_x.append(i)
#             if len(last_line_x.intersection(
#                     level_last_x)) == 0:  # если на последней строке фигуры с 0 индекс 0 совпадает
#                 for i in range(5):  # с индексом 0 на следующей строке файла цикл прекращается
#                     new_line = 10 * '.' + figure[i] + 10 * '.'
#                     level_map[i] = new_line
#                 mapFile.close()
#                 a = open('data/figures.txt', mode='w', encoding='utf-8')
#                 for el in level_map:
#                     a.write(el + '\n')
#             else:
#                 break
#             a.close()

if __name__ == "__main__":
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('T E T R I S')
    global board
    Score = [0]
    fixed_pos = {}
    board = create_board(fixed_pos)
    change_piece = False
    run = True
    cur_figure = new_figure()
    clock = pygame.time.Clock()
    falling_time = 0

    while run:
        falling_speed = 0.3
        board = create_board(fixed_pos)
        falling_time += clock.get_rawtime()
        clock.tick()

        if falling_time / 1000 >= falling_speed:
            falling_time = 0
            cur_figure.y += 1
            if not (free_cells(cur_figure, board)) and cur_figure.y > 0:
                cur_figure.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cur_figure.x -= 1
                    if not free_cells(cur_figure, board):
                        cur_figure.x += 1

                elif event.key == pygame.K_RIGHT:
                    cur_figure.x += 1
                    if not free_cells(cur_figure, board):
                        cur_figure.x -= 1
                elif event.key == pygame.K_UP:
                    cur_figure.rotation = cur_figure.rotation + 1 % len(cur_figure.figure)
                    if not free_cells(cur_figure, board):
                        cur_figure.rotation = cur_figure.rotation - 1 % len(cur_figure.figure)

                if event.key == pygame.K_DOWN:
                    cur_figure.y += 1
                    if not free_cells(cur_figure, board):
                        cur_figure.y -= 1

        figure_cord = change_format(cur_figure)

        for i in range(len(figure_cord)):
            x, y = figure_cord[i]
            if y > -1:
                board[y][x] = cur_figure.color

        if change_piece:
            for cords in figure_cord:
                fixed_pos[(cords[0], cords[1])] = cur_figure.color
            cur_figure = new_figure()
            change_piece = False

            delete_rows(board, fixed_pos, Score)

        draw_app(screen)
        score = str(Score[0])
        draw_score(screen, score)
        pygame.display.update()

        if game_over(fixed_pos):
            run = False
        pygame.display.update()

# if __name__ == "__main__":
#     # figures = {"o": "#0F4FA8", "t": "#FFCA90", "l": "#D30068", "j": "#FF9F00", "s": "#00737E", "z": "#3F92D2",
#     #            "i": "#E60042"}
#     pygame.init()
#     size = screen_width, screen_height
#     screen = pygame.display.set_mode(size)
#     pygame.display.set_caption("Tetris")
#     icon = pygame.image.load("data\icon.png")
#     pygame.display.set_icon(icon)
#     clock = pygame.time.Clock()
#     # all_sprites = pygame.sprite.Group()
#     # gi = Interface()
#     # all_sprites.add(gi)
#     # load_level(1)
#     fps = 30
#     # start_screen()
#     running = True
#     # if not tests:
#     #     score = 1058
#     #         while running:
#     #             events = pygame.event.get()
#     #             for event in events:
#     #                 if event.type == pygame.QUIT:
#     #                     running = False
#     #             screen.fill((0, 0, 0))
#     #             # all_sprites.draw(screen)
#     #             # gi.print_text(screen, "TETRIS", 2, "red", 9, 1)
#     #             # gi.print_text(screen, "By D&E ", 0.5, "white", 22.2, 23.2)
#     #             # gi.print_text(screen, "YOUR SCORE", 0.75, "white", 4.2, 22.25)
#     #             # gi.print_text(screen, score, 0.75, pygame.Color("#FFAA00"), 6.25, 23.2)
#     #             pygame.display.flip()
#     #             clock.tick(FPS)
#     while running:
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             create_board()
#             draw_board(screen, 10, 20)
#         pygame.display.flip()
# pygame.quit()
