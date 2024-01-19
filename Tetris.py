import pygame
import os
import sys
import random

pygame.init()
fps = 60
block_size = 30
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
    grid = [[(255, 255, 255) for x in range(10)] for x in range(18)]
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
    free_cells = [[(j, i) for j in range(10) if grid[i][j] == (255, 255, 255)] for i in range(18)]
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


def draw_app(screen):
    for i in range(len(board)):
        for j in range(len(board[i])):
            pygame.draw.rect(screen, board[i][j],
                             (mx_left_x + j * block_size, mx_left_y + i * block_size, block_size, block_size), 0)
    draw_board(screen, 18, 10)


# class Tetris:
#     def __init__(self):
#         # возможные фигруы в тетрисе (игра создана изначально русским программистом на языке Pascal
#         # ее название символично ведь каждая фигура состоит из 4 кваратов\
#         # figures = ["O", "T", "L", "S", "J", "I", "Z"]


class Interface(pygame.sprite.Sprite):
    def __init__(self):  # отрисовка интерфейса при игре
        super().__init__()
        self.image = pygame.Surface([screen_width, screen_height])
        self.image.fill(pygame.Color("black"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 1, 1
        self.draw("GI", self.image)

    def load_image(self, name):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    def start_screen(self, type):
        if type == "start":
            intro_text = ["Tetris", "",
                          "Для начала игры нажмите на пробел",
                          f"Лучший счет - {best}"]
            filename = 'start_screen.jpg'
        else:
            intro_text = ["Tetris", "",
                          "Пауза",
                          "Для продолжения игры нажмите на пробел",
                          f"Ваш счет - {best}"]
            filename = 'start_screen.jpg'
        fon = pygame.transform.scale(self.load_image(filename), (block_size * 24, block_size * 24))
        screen.blit(fon, (0, 0))
        text_coord = block_size * 2
        for line in intro_text:
            font = pygame.font.Font(None, block_size * 2) if line == "Tetris" else pygame.font.Font(None,
                                                                                                    block_size * 1)
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += block_size
            intro_rect.top = text_coord
            intro_rect.x = block_size
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def print_text(self, surface, word, size, text_color, x, y):
        if word == "TETRIS":
            font = pygame.font.SysFont("yugothicui", size * block_size)
            t = font.render("T", 1, pygame.Color("#D30068"), pygame.Color("black"))
            e = font.render("E", 1, pygame.Color("#00737E"), pygame.Color("black"))
            r = font.render("R", 1, pygame.Color("#FF9F00"), pygame.Color("black"))
            i = font.render("I", 1, pygame.Color("#E60042"), pygame.Color("black"))
            s = font.render("S", 1, pygame.Color("#00737E"), pygame.Color("black"))
            tetris = {"t": t, "e": e, "s": s, "r": r, "i": i}
            for i, el in enumerate(list("tetris")):
                if el == "i":
                    screen.blit(tetris[el], (int(block_size * (9.5 + i + 0.5)), block_size))
                else:
                    screen.blit(tetris[el], (block_size * (9.5 + i), block_size))
        else:
            font = pygame.font.SysFont("yugothicui", int(size * block_size))
            follow = font.render(f"{word}", 0, pygame.Color(text_color), pygame.Color("black"))
            surface.blit(follow, (int(block_size * x), int(block_size * y)))

    def draw(self, filename, surface):
        figures = {"o": "#0F4FA8", "t": "#FFCA90", "l": "#D30068", "j": "#FF9F00", "s": "#00737E", "z": "#3F92D2",
                   "i": "#E60042", "-": "white"}
        filedata = open(f"data/{filename}.txt", mode="r").read().split("\n")
        indent = 0 if filename == "GI" else 7 * block_size
        data = [list(line) for line in filedata]
        end_up_border = 0
        border_line = {0: [0, block_size // 10, 0, 0], 1: [0, 0, 0, block_size // 10]}
        for y in range(len(data)):  # int(height / tile_size)
            for x in range(len(data[0])):  # int(width / tile_size)
                px = py = p0x = p0y = 0
                if data[y][x] in figures.keys():
                    color = figures[data[y][x]]
                    if data[y][x] == "-":
                        pygame.draw.rect(surface, pygame.Color(color),
                                         (x * block_size, y * block_size, block_size, block_size), block_size // 10)
                        if data[y].count("-") > 2:
                            p0x, p0y, px, py = border_line[end_up_border]
                        else:
                            p0x, p0y, px, py = [block_size // 10, 0, 0, 0] if x < len(data[y]) // 2 else [0, 0,
                                                                                                          block_size // 10,
                                                                                                          0]
                    else:
                        pygame.draw.rect(surface, pygame.Color(color),
                                         (indent + x * block_size, indent + y * block_size, block_size, block_size),
                                         block_size // 10)
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
                            px, p0x = block_size // 10, block_size // 10
                        elif 9 in p:
                            px, p0x = 0, block_size // 10
                        else:
                            px, p0x = block_size // 10, (block_size // 10) * 2

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
                            py, p0y = block_size // 10, block_size // 10
                        else:
                            py, p0y = block_size // 10, (block_size // 10) * 2
                elif data[y][x] == "." and data[y].count("-") > 2 and data[y].index("-") < x:
                    end_up_border = 1
                pygame.draw.rect(surface, pygame.Color("black"),
                                 (indent + x * block_size + px, indent + y * block_size + py, block_size - p0x,
                                  block_size - p0y), 0)


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

    screen_width = block_size * 24
    screen_height = block_size * 24
    tetris_width = block_size * 10
    tetris_height = block_size * 18
    mx_left_x = block_size * 7
    mx_left_y = block_size * 3
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('T E T R I S')
    icon = pygame.image.load("data\icon.png")
    pygame.display.set_icon(icon)
    global board
    score = 0
    fixed_pos = {}
    board = create_board(fixed_pos)
    change_piece = False
    run = True
    cur_figure = new_figure()
    clock = pygame.time.Clock()
    falling_time = 0
    type = "start"
    level_text = 'Level 1'
    speeds = open('data/speed.txt', 'r').readlines()
    best = open(f"data/best_score.txt", mode="r").read().split("\n")[0]
    all_sprites = pygame.sprite.Group()
    gi = Interface()
    gi.start_screen(type)
    all_sprites.add(gi)
    play = False
    while run:
        screen.fill((0,0,0))
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

                elif event.key == pygame.K_DOWN:
                    cur_figure.y += 1
                    if not free_cells(cur_figure, board):
                        cur_figure.y -= 1

                elif event.type == pygame.QUIT:
                    running = False

                if event.key == pygame.K_SPACE:
                    play = True
                    type = "pause"

                if event.key == pygame.K_ESCAPE:
                    play = False
                    type = "pause"

        if play:

            figure_cord = change_format(cur_figure)
            if score < 20:
                falling_speed = float(speeds[0][:-1])
            elif 20 <= score < 40:
                falling_speed = float(speeds[1][:-1])
                level_text = 'Level 2'
            elif 40 <= score:
                falling_speed = float(speeds[2][:-1])
                level_text = 'Level 3'
            board = create_board(fixed_pos)
            falling_time += clock.get_rawtime()
            clock.tick()
            if falling_time / 1000 >= falling_speed:
                falling_time = 0
                cur_figure.y += 1
                if not (free_cells(cur_figure, board)) and cur_figure.y > 0:
                    cur_figure.y -= 1
                    change_piece = True
            all_sprites.draw(screen)



            for i in range(len(figure_cord)):
                x, y = figure_cord[i]
                if y > -1:
                    board[y][x] = cur_figure.color

            if change_piece:
                for cords in figure_cord:
                    fixed_pos[(cords[0], cords[1])] = cur_figure.color
                cur_figure = new_figure()
                change_piece = False

                delete_rows(board, fixed_pos, score)
            gi.print_text(screen, "TETRIS", 2, "red", 9, 1)
            gi.print_text(screen, "BEST", 1, "#FFC200", 2, 4)
            gi.print_text(screen, best, 1, "white", len(best) - 3, 5)
            gi.print_text(screen, "YOUR SCORE", 0.75, "white", 4.2, 22.25)
            gi.print_text(screen, "By D&E ", 0.5, "white", 22.2, 23.2)
            gi.print_text(screen, score, 0.75, pygame.Color("#FFAA00"), 6.25, 23.2)
            draw_app(screen)
            pygame.display.update()
        else:
            gi.start_screen(type)
        pygame.display.flip()
        pygame.display.update()
pygame.quit()
