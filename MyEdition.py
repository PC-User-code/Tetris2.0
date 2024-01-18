import pygame
import os
import sys

tests = False
tile_size = 25
FPS = 60


class Tetris:
    def __init__(self, best):
        # возможные фигруы в тетрисе (игра создана изначально русским программистом на языке Pascal
        # ее название символично ведь каждая фигура состоит из 4 кваратов\
        figures = ["O", "T", "L", "S", "J", "I", "Z"]
        best_score = best
        figf =  {'S': [['.....',
                      '.....',
                      '..ss.',
                      '.ss..',
                      '.....'],
                     ['.....',
                      '..s..',
                      '..ss.',
                      '...s.',
                      '.....']],
               'Z': [['.....',
                      '.....',
                      '.zz..',
                      '..zz.',
                      '.....'],
                     ['.....',
                      '..z..',
                      '.zz..',
                      '.z...',
                      '.....']],
               'J': [['.....',
                      '.j...',
                      '.jjj.',
                      '.....',
                      '.....'],
                     ['.....',
                      '..jj.',
                      '..j..',
                      '..j..',
                      '.....'],
                     ['.....',
                      '.....',
                      '.jjj.',
                      '...j.',
                      '.....'],
                     ['.....',
                      '..j..',
                      '..j..',
                      '.jj..',
                      '.....']],
               'L': [['.....',
                      '...l.',
                      '.lll.',
                      '.....',
                      '.....'],
                     ['.....',
                      '..l..',
                      '..l..',
                      '..ll.',
                      '.....'],
                     ['.....',
                      '.....',
                      '.lll.',
                      '.l...',
                      '.....'],
                     ['.....',
                      '.ll..',
                      '..l..',
                      '..l..',
                      '.....']],
               'I': [['..i..',
                      '..i..',
                      '..i..',
                      '..i..',
                      '.....'],
                     ['.....',
                      '.....',
                      'iiii.',
                      '.....',
                      '.....']],
               'O': [['.....',
                      '.....',
                      '.oo..',
                      '.oo..',
                      '.....']],
               'T': [['.....',
                      '..t..',
                      '.ttt.',
                      '.....',
                      '.....'],
                     ['.....',
                      '..t..',
                      '..tt.',
                      '..t..',
                      '.....'],
                     ['.....',
                      '.....',
                      '.ttt.',
                      '..t..',
                      '.....'],
                     ['.....',
                      '..t..',
                      '.tt..',
                      '..t..',
                      '.....']]}


class Interface(pygame.sprite.Sprite):
    def __init__(self):  # отрисовка интерфейса при игре
        super().__init__()
        self.image = pygame.Surface([width, height])
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
        fon = pygame.transform.scale(self.load_image(filename), (tile_size * 24, tile_size * 24))
        screen.blit(fon, (0, 0))
        text_coord = tile_size * 2
        for line in intro_text:
            font = pygame.font.Font(None, tile_size * 2) if line == "Tetris" else pygame.font.Font(None, tile_size * 1)
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += tile_size
            intro_rect.top = text_coord
            intro_rect.x = tile_size
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

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
                    screen.blit(tetris[el], (int(tile_size * (9.5 + i + 0.5)), tile_size))
                else:
                    screen.blit(tetris[el], (tile_size * (9.5 + i), tile_size))
        else:
            font = pygame.font.SysFont("yugothicui", int(size * tile_size))
            follow = font.render(f"{word}", 0, pygame.Color(text_color), pygame.Color("black"))
            surface.blit(follow, (int(tile_size * x), int(tile_size * y)))

    def draw(self, filename, surface):
        filedata = open(f"data/{filename}.txt", mode="r").read().split("\n")
        indent = 0 if filename == "GI" else 7 * tile_size
        data = [list(line) for line in filedata]
        end_up_border = 0
        border_line = {0: [0, tile_size // 10, 0, 0], 1: [0, 0, 0, tile_size // 10]}
        for y in range(len(data)):  # int(height / tile_size)
            for x in range(len(data[0])):  # int(width / tile_size)
                px = py = p0x = p0y = 0
                if data[y][x] in figures.keys():
                    color = figures[data[y][x]]
                    if data[y][x] == "-":
                        pygame.draw.rect(surface, pygame.Color(color),
                                     (x * tile_size, y * tile_size, tile_size, tile_size), tile_size // 10)
                        if data[y].count("-") > 2:
                            p0x, p0y, px, py = border_line[end_up_border]
                        else:
                            p0x, p0y, px, py = [tile_size // 10, 0, 0, 0] if x < len(data[y]) // 2 else [0, 0, tile_size // 10, 0]
                    else:
                        pygame.draw.rect(surface, pygame.Color(color),
                                     (indent + x * tile_size, indent + y * tile_size, tile_size, tile_size), tile_size // 10)
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
                            px, p0x = tile_size // 10, tile_size // 10
                        elif 9 in p:
                            px, p0x = 0, tile_size // 10
                        else:
                            px, p0x = tile_size // 10, (tile_size // 10) * 2

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
                            py, p0y = tile_size // 10, tile_size // 10
                        else:
                            py, p0y = tile_size // 10, (tile_size // 10) * 2
                elif data[y][x] == "." and data[y].count("-") > 2 and data[y].index("-") < x:
                    end_up_border = 1
                pygame.draw.rect(surface, pygame.Color("black"),
                                 (indent + x * tile_size + px, indent + y * tile_size + py, tile_size - p0x,
                                  tile_size - p0y), 0)


if __name__ == "__main__":
    figures = {"o": "#0F4FA8", "t": "#FFCA90", "l": "#D30068", "j": "#FF9F00", "s": "#00737E", "z": "#3F92D2",
               "i": "#E60042", "-": "white"}
    best = open(f"data/best_score.txt", mode="r").read().split("\n")[0]
    tt = Tetris(best)
    pygame.init()
    pygame.display.set_caption("T E T R I S")
    icon = pygame.image.load("data\icon.png")
    pygame.display.set_icon(icon)
    size = width, height = tile_size * 24, tile_size * 24
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    gi = Interface()
    all_sprites.add(gi)
    running = True
    play = False
    type = "start"
    if not tests:
        score = 1058
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    play = True
                    type = "pause"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if not play:
                        running = False
                    else:
                        play = False
                        type = "pause"
            if play:
                screen.fill((0, 0, 0))
                all_sprites.draw(screen)
                gi.print_text(screen, "TETRIS", 2, "red", 9, 1)
                gi.print_text(screen, "BEST", 1, "#FFC200", 2, 4)
                gi.print_text(screen, best, 1, "white", len(best) - 3, 5)
                gi.print_text(screen, "YOUR SCORE", 0.75, "white", 4.2, 22.25)
                gi.print_text(screen, "By D&E ", 0.5, "white", 22.2, 23.2)
                gi.print_text(screen, score, 0.75, pygame.Color("#FFAA00"), 6.25, 23.2)
            else:
                gi.start_screen(type)
            pygame.display.flip()
            clock.tick(FPS)
    pygame.quit()