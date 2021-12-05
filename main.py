import pygame
import sys
import pathlib
import random

pygame.init()
WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("project")

WHITE = 255, 255, 255
print(sys.argv[0])
print(pathlib.Path(sys.argv[0]))
BASE = pathlib.Path(sys.argv[0]).parent
FPS = 60
FONT = pygame.font.SysFont("Arial", 30)
P1_W = FONT.render("Hráč vyhrál.", True, (0, 0, 0))
C1_W = FONT.render("Počítač vyhrál.", True, (0, 0, 0))
P1 = FONT.render("HRÁČ", True, (0, 0, 0))
C1 = FONT.render("POČÍTAČ", True, (0, 0, 0))


class Cross(pygame.Rect):
    def __init__(self, x, y, w, h):
        self.chosen = False
        self.shot = False
        self.watered = False
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Board:
    def __init__(self, name: str, top_left: tuple = (0, 0)):
        self.name = name
        self.top_left = top_left
        self.won = False
        self.number_of_pairs_chosen = 0
        self.number_of_pairs_limit = 10

        self.rectangles = [[0] * 10 for _ in range(10)]
        for w in range(10):
            for i in range(10):
                self.rectangles[w][i] = Cross(
                    i * 35 + self.top_left[0], w * 35 + self.top_left[1], 30, 30)

    def draw(self):
        for w in range(10):
            for i in range(10):
                if self.rectangles[w][i].chosen:
                    pygame.draw.rect(WIN, (255, 0, 0), self.rectangles[w][i])
                else:
                    pygame.draw.rect(WIN, (0, 0, 0), self.rectangles[w][i])
        pygame.display.update()

    def on_click(self):
        if self.number_of_pairs_chosen == 10:
            player_turn()
        else:
            for w in range(10):
                for i in range(10):
                    if self.rectangles[w][i].collidepoint(mouse_pos) and self.number_of_pairs_chosen < self.number_of_pairs_limit and not self.rectangles[w][i].chosen:
                        self.number_of_pairs_chosen += 1
                        self.rectangles[w][i].chosen = True
                        if self.number_of_pairs_chosen == 10:
                            enemy_choice()
                    if self.rectangles[w][i].chosen:
                        pygame.draw.rect(WIN, (255, 0, 0),
                                         self.rectangles[w][i])
            pygame.display.update()

    def get_rectangles_shot(self):
        a = 0
        for w in range(10):
            for i in range(10):
                if self.rectangles[w][i].shot:
                    a += 1
        return a


def enemy_choice():
    for i, y in get_enemy_coordinates():
        b.rectangles[i][y].chosen = True


def player_turn():
    for w in range(10):
        for i in range(10):
            if b.rectangles[w][i].collidepoint(mouse_pos) and not b.rectangles[w][i].watered:
                computer_turn()
                b.rectangles[w][i].watered = True
                pygame.draw.rect(WIN, (0, 0, 255), b.rectangles[w][i])
                if b.rectangles[w][i].chosen:
                    b.rectangles[w][i].shot = True
                    pygame.draw.rect(WIN, (0, 255, 0), b.rectangles[w][i])
    if a.get_rectangles_shot() == 10:
        global won
        won = True
        WIN.blit(C1_W, (500, 440))
    if b.get_rectangles_shot() == 10:
        won = True
        WIN.blit(P1_W, (500, 440))
    pygame.display.update()


def computer_turn():
    e = 0
    while e < 1:
        w = random.randint(0, 9)
        i = random.randint(0, 9)
        if a.rectangles[w][i].watered:
            continue
        a.rectangles[w][i].watered = True
        pygame.draw.rect(WIN, (0, 0, 255), a.rectangles[w][i])
        if a.rectangles[w][i].chosen:
            a.rectangles[w][i].watered = True
            a.rectangles[w][i].shot = True
            pygame.draw.rect(WIN, (0, 255, 0), a.rectangles[w][i])
        e += 1
    if a.get_rectangles_shot() == 10:
        global won
        won = True
        WIN.blit(C1_W, (500, 440))
    if b.get_rectangles_shot() == 10:
        won = True
        WIN.blit(P1_W, (500, 440))
    pygame.display.update()


def get_enemy_coordinates():
    enemy = [[None] * 2 for _ in range(10)]
    e = 0
    while e < 10:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if [x, y] not in enemy:
            enemy[e][0] = x
            enemy[e][1] = y
            e += 1
    return enemy


def draw_window():
    WIN.fill(WHITE)
    WIN.blit(P1, (100, 380))
    WIN.blit(C1, (600, 380))
    pygame.display.update()


def main():
    global mouse_pos
    global b
    global a
    global won
    won = False
    clock = pygame.time.Clock()
    run = True
    a = Board("hrac", (20, 20))
    b = Board("pocitac", (500, 20))
    draw_window()
    a.draw()
    b.draw()
    while run:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not won:
                a.on_click()

    pygame.quit()


if __name__ == "__main__":
    main()
