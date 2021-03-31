import os
import pygame
import random


class Window:
    WIDTH = 1000
    HEIGHT = 800

    COLOR = {'white': (255, 255, 255),
             'black': (0, 0, 0),
             'yellow': (255, 255, 0)}

    NEW_LEVEL = ['Score:', 'Circles:', 'Squares:']

    RULES = {'Circle: 30': 'Press: c',
             'Square: 20': 'Press: s',
             'Score booster: 100': 'Press: b'}

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Clicker")
        self.screen.fill(self.COLOR['black'])
        self.template()
        pygame.display.flip()

    def draw_obj(self, shape, color, x, y):
        if shape == 'circle':
            pygame.draw.circle(self.screen, color, [x, y], 25)
        if shape == 'square':
            pygame.draw.rect(self.screen, color, [x, y, 50, 50])

    def template(self, score=0, level=1):
        font = pygame.font.Font('freesansbold.ttf', 40)

        score_text = font.render('Your score is: {}'.format(score), True,
                                 self.COLOR['white'], self.COLOR['black'])
        level_text = font.render('Level: {}'.format(level), True,
                                 self.COLOR['white'], self.COLOR['black'])

        self.screen.blit(score_text, (5, 15))
        self.screen.blit(level_text, (500, 15))

    def win(self):
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render('You are winner! Well done!',
                           True, self.COLOR['white'], self.COLOR['black'])
        self.screen.blit(text, (200, 400))

    def next_level(self, args):
        font = pygame.font.Font('freesansbold.ttf', 20)

        text = font.render('To next level you need:',
                           True, self.COLOR['white'], self.COLOR['black'])

        self.screen.blit(text, (750, 5))

        for i in range(len(self.NEW_LEVEL)):
            text = font.render('{} {}'.format(self.NEW_LEVEL[i], args[i]),
                               True, self.COLOR['white'], self.COLOR['black'])
            self.screen.blit(text, (750, 25 * (i + 1)))

    def rules(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        i = 0
        for item in self.RULES:
            text = font.render(item, True,
                               self.COLOR['white'], self.COLOR['black'])
            text_press = font.render(self.RULES[item], True,
                                     self.COLOR['white'], self.COLOR['black'])

            self.screen.blit(text, (50 + 300 * i, 710))
            self.screen.blit(text_press, (50 + 300 * i, 745))
            i += 1


class Object:
    Vx = 2
    Vy = 2
    x = 500
    y = 400
    colors = [(0, 225, 0), (0, 0, 255), (255, 0, 0),
              (255, 0, 255), (0, 255, 255), (255, 255, 0)]

    def __init__(self, shape):
        self.color = random.choice(self.colors)
        self.Vx = random.randint(1, 5)
        self.Vy = random.randint(1, 3)
        self.shape = shape

    def change_v(self, x1, y1, x2, y2):
        if self.x >= x1 or self.x <= x2:
            self.Vx = -self.Vx
        if self.y >= y1 or self.y <= y2:
            self.Vy = -self.Vy

    def move(self):
        self.x += self.Vx
        self.y += self.Vy
        if self.shape == 'circle':
            self.change_v(975, 680, 25, 120)
        else:
            self.change_v(950, 660, 0, 110)

    def draw(self):
        self.move()
        return [self.shape, self.color, self.x, self.y]


class Game(Window):
    win = False
    score = 0
    level = 1
    boost = 2
    obj = [[], []]
    cost = {pygame.K_c: [30, ['circle', 0]],
            pygame.K_s: [20, ['square', 1]],
            pygame.K_b: [100, 2]}
    # score, circles, squares
    levels = [[100 * 10 ** i, 4 * i + 5, 7 * i + 4] for i in range(5)]

    def __init__(self):
        super().__init__()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.win:
                        if event.key == pygame.K_SPACE:
                            self.score += self.boost
                        else:
                            try:
                                t = event.key
                                if self.score >= self.cost[t][0]:
                                    self.score -= self.cost[t][0]
                                    L = self.cost[t][1]
                                    if isinstance(L, type([])):
                                        self.obj[L[1]].append(Object(L[0]))
                                    else:
                                        self.boost += 2
                            except Exception:
                                pass
                    else:
                        if event.key == pygame.K_SPACE:
                            self.boost = 2
                            self.score = 0
                            self.level = 1
                            self.win = False
                            self.obj[0].clear()
                            self.obj[1].clear()

            self.screen.fill((0, 0, 0))
            super().template(self.score, self.level)
            super().rules()

            for array in self.obj:
                for figure in array:
                    l = figure.draw()
                    super().draw_obj(l[0], l[1], l[2], l[3])

            if self.level >= 5:
                self.win = True
                super().win()
            else:
                if self.score >= self.levels[self.level - 1][0]:
                    if len(self.obj[0]) >= self.levels[self.level - 1][1]:
                        if len(self.obj[1]) >= self.levels[self.level - 1][2]:
                            self.level += 1
                            self.obj[0].clear()
                            self.obj[1].clear()
                            self.score = 0
                level = self.levels[self.level - 1]
                super().next_level([max(level[0] - self.score, 0),
                                    max(level[1] - len(self.obj[0]), 0),
                                    max(level[2] - len(self.obj[1]), 0)])

            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
