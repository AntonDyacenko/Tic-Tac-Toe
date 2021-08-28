import pygame
import random

pygame.init()
size0 = width, height = 601, 601
screen = pygame.display.set_mode(size0)
running = True
move = 0

coordinate = {(0, 0): 'N', (1, 0): 'N', (2, 0): 'N', (0, 1): 'N', (1, 1): 'N', (2, 1): 'N', (0, 2): 'N', (1, 2): 'N',
              (2, 2): 'N'}


def append_in_matrix(pos, name):
    coordinate[search_coordinate(pos)] = name


def search_game_over():
    if len([i for i in coordinate if coordinate[i] == 'N']) == 0:
        return 'Game over!'
    else:
        return False


def search_win():
    with_x = [[], []]
    x = []
    with_o = [[], []]
    o = []
    for i in coordinate:
        if coordinate[i] == 'X':
            x.append(i)
            with_x[0].append(i[0])
            with_x[1].append(i[1])
        elif coordinate[i] == 'O':
            o.append(i)
            with_o[0].append(i[0])
            with_o[1].append(i[1])
    if with_x[0].count(0) == 3 or with_x[0].count(1) == 3 or with_x[0].count(2) == 3 or with_x[1].count(0) == 3 or \
            with_x[1].count(1) == 3 or with_x[1].count(2) == 3:
        return 'Human win!'
    elif with_o[0].count(0) == 3 or with_o[0].count(1) == 3 or with_o[0].count(2) == 3 or with_o[1].count(0) == 3 or \
            with_o[1].count(1) == 3 or with_o[1].count(2) == 3:
        return 'Bot win!'
    elif ((0, 0) in x and (1, 1) in x and (2, 2) in x) or ((2, 0) in x and (1, 1) in x and (0, 2) in x):
        return 'Human win!'
    elif ((0, 0) in o and (1, 1) in o and (2, 2) in o) or ((2, 0) in o and (1, 1) in o and (0, 2) in o):
        return 'Bot win!'
    else:
        return False


def draw_table():
    for x in range(5):
        pygame.draw.line(screen, (255, 255, 255), ((width - 1) / 3 * x, 0), ((width - 1) / 3 * x, width - 1))
    for y in range(5):
        pygame.draw.line(screen, (255, 255, 255), (0, (height - 1) / 3 * y), (height - 1, (height - 1) / 3 * y))


def draw_X(pos):
    pygame.draw.line(screen, (255, 0, 0), (pos[0] + 1, pos[1] + 10),
                     (pos[0] - 1 + (width // 3), pos[1] + height // 3 - 10), 20)
    pygame.draw.line(screen, (255, 0, 0), (pos[0] + 1, pos[1] + height // 3 - 10),
                     (pos[0] - 1 + (width // 3), pos[1] + 10), 20)


def draw_O(pos):
    if pos != -1:
        pygame.draw.circle(screen, (0, 255, 0), (pos[0] + width // 6, pos[1] + height // 6), width // 6 - 1, 20)


def search_coordinate(pos):
    return (pos[0] * 3 // width, pos[1] * 3 // height)


class Bot:
    def __init__(self):
        pass

    def detect_couple(self, name):
        with_name = [[], []]
        name_coordinate = []
        ans = []
        for i in coordinate:
            if coordinate[i] == name:
                name_coordinate.append(i)
                with_name[0].append(i[0])
                with_name[1].append(i[1])
        for i in range(2):
            for j in range(3):
                if with_name[i].count(j) == 2:  # в X или Y повторяющихся == 2
                    c = [a for a in name_coordinate if j == a[i]]
                    ans.append(c)
        c = [a for a in name_coordinate if a[0] == a[1]]
        if len(c) == 2:
            ans.append(c)
        c = [a for a in name_coordinate if a[1] == 2 - a[0]]
        if len(c) == 2:
            ans.append(c)
        if ans:
            for i in ans:
                d = [0, 1, 2]
                if i[0][0] == i[1][0]:
                    f = [i[0][1], i[1][1]]
                    a = (i[0][0], [v for v in d if v not in f][0])
                    if coordinate[a] == 'N':
                        i.append(a)
                elif i[0][1] == i[1][1]:
                    f = [i[0][0], i[1][0]]
                    a = ([v for v in d if v not in f][0], i[0][1])
                    if coordinate[a] == 'N':
                        i.append(a)
                elif i[0][0] == i[0][1] and i[1][0] == i[1][1]:
                    f = [i[0][0], i[1][0]]
                    a = [v for v in d if v not in f][0]
                    if coordinate[(a, a)] == 'N':
                        i.append((a, a))
                elif i[0][1] == 2 - i[0][0] and i[1][1] == 2 - i[1][0]:
                    f = [i[0][0], i[1][0]]
                    a = [v for v in d if v not in f][0]
                    if coordinate[(a, 2 - a)] == 'N':
                        i.append((a, 2 - a))
        ans = [i for i in ans if coordinate[i[-1]] == 'N']
        if ans:
            return [name, ans]
        else:
            return False

    def calculate_free(self, pos_sp):
        sp = []
        for pos in pos_sp:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= i + pos[0] <= 2 and 0 <= j + pos[1] <= 2:
                        if coordinate[(i + pos[0], j + pos[1])] == 'N':
                            sp.append((i + pos[0], j + pos[1]))
        return random.choice(sp)

    def angle_detect(self):
        if coordinate[(1, 2)] == coordinate[(2, 1)] == 'X':
            if coordinate[(2, 2)] == 'N':
                return (2, 2)
        elif coordinate[(2, 1)] == coordinate[(1, 0)] == 'X':
            if coordinate[(2, 0)] == 'N':
                return (2, 0)
        elif coordinate[(1, 0)] == coordinate[(0, 1)] == 'X':
            if coordinate[(0, 0)] == 'N':
                return (0, 0)
        elif coordinate[(0, 1)] == coordinate[(1, 2)] == 'X':
            if coordinate[(0, 2)] == 'N':
                return (0, 2)
        else:
            return False

    def diagonal_detect(self):
        if coordinate[(0, 0)] == coordinate[(2, 2)] == 'X' or coordinate[(0, 2)] == coordinate[(2, 0)] == 'X':
            if coordinate[(1, 2)] == 'N':
                return (1, 2)
        else:
            return False

    def g_detect(self):
        if coordinate[(0, 0)] == coordinate[(1, 2)] == 'X':
            if coordinate[(0, 2)] == 'N':
                return (0, 2)
        elif coordinate[(0, 0)] == coordinate[(2, 1)] == 'X':
            if coordinate[(2, 0)] == 'N':
                return (2, 0)
        elif coordinate[(2, 0)] == coordinate[(1, 2)] == 'X':
            if coordinate[(2, 2)] == 'N':
                return (2, 2)
        elif coordinate[(2, 0)] == coordinate[(0, 1)] == 'X':
            if coordinate[(0, 0)] == 'N':
                return (0, 0)
        elif coordinate[(2, 2)] == coordinate[(1, 0)] == 'X':
            if coordinate[(2, 1)] == 'N':
                return (2, 1)
        elif coordinate[(2, 2)] == coordinate[(0, 1)] == 'X':
            if coordinate[(0, 2)] == 'N':
                return (0, 2)
        elif coordinate[(0, 2)] == coordinate[(2, 1)] == 'X':
            if coordinate[(1, 2)] == 'N':
                return (1, 2)
        elif coordinate[(0, 2)] == coordinate[(1, 0)] == 'X':
            if coordinate[(0, 1)] == 'N':
                return (0, 1)
        else:
            return False

    def search_line(self):
        if coordinate[(1, 1)] == coordinate[(2, 2)] == 'X':
            if coordinate[(0, 2)] == 'N':
                return (0, 2)
            else:
                return False

    def go(self):
        if move == 1:
            if coordinate[(1, 1)] == 'X':
                coordinate[(0, 0)] = 'O'
            else:
                coordinate[(1, 1)] = 'O'

        elif move == 3:
            if self.angle_detect():
                coordinate[self.angle_detect()] = 'O'
            elif self.diagonal_detect():
                coordinate[self.diagonal_detect()] = 'O'
            elif self.search_line():
                coordinate[self.search_line()] = 'O'
            elif self.g_detect():
                coordinate[self.g_detect()] = 'O'
            elif self.detect_couple('O'):
                coordinate[self.detect_couple('O')[-1][-1][-1]] = 'O'
            elif self.detect_couple('X'):
                coordinate[self.detect_couple('X')[-1][-1][-1]] = 'O'
            else:
                coordinate[self.calculate_free([i for i in coordinate if coordinate[i] == 'O'])] = 'O'

        else:
            if self.detect_couple('O'):
                coordinate[self.detect_couple('O')[-1][-1][-1]] = 'O'
            elif self.detect_couple('X'):
                coordinate[self.detect_couple('X')[-1][-1][-1]] = 'O'
            elif self.angle_detect():
                coordinate[self.angle_detect()] = 'O'
            else:
                coordinate[self.calculate_free(([i for i in coordinate if coordinate[i] == 'O']))] = 'O'


bot = Bot()
while running:
    screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not search_win() and not search_game_over():
                if coordinate[search_coordinate(event.pos)] == 'N':
                    append_in_matrix(event.pos, 'X')
                    move += 1
            else:
                coordinate = {(0, 0): 'N', (1, 0): 'N', (2, 0): 'N', (0, 1): 'N', (1, 1): 'N', (2, 1): 'N', (0, 2): 'N',
                              (1, 2): 'N',
                              (2, 2): 'N'}
                move = 0
    for i in coordinate:
        if coordinate[i] == 'X':
            draw_X((i[0] * width // 3, i[1] * height // 3))
        elif coordinate[i] == 'O':
            draw_O((i[0] * width // 3, i[1] * height // 3))
    if not search_win() and not search_game_over():
        if move % 2 != 0:
            bot.go()

            move += 1
    elif search_game_over():
        t = search_game_over()
        f1 = pygame.font.Font(None, 70)
        text1 = f1.render(t, 1, (255, 255, 0))
        place = text1.get_rect(center=(width // 2, height // 2))
        text2 = f1.render(t, 1, (100, 100, 0))
        place2 = text1.get_rect(center=((width + 5) // 2, (height + 5) // 2))
        screen.blit(text2, place2)
        screen.blit(text1, place)
    else:
        t = search_win()
        f1 = pygame.font.Font(None, 70)
        text1 = f1.render(t, 1, (255, 255, 0))
        place = text1.get_rect(center=(width // 2, height // 2))
        text2 = f1.render(t, 1, (100, 100, 0))
        place2 = text1.get_rect(center=((width + 5) // 2, (height + 5) // 2))
        screen.blit(text2, place2)
        screen.blit(text1, place)
    draw_table()
    pygame.display.flip()
