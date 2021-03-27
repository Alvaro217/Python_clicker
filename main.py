import os
import pygame
import random


class Window:
    WIDTH = 1000
    HEIGHT = 800

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Clicker")
        self.screen.fill((255, 255, 0))
        self.write_template()
        pygame.display.flip()

    def draw_obj(self, shape, color, x, y):
        if shape == 'circle':
            pygame.draw.circle(self.screen, color, [x, y], 25)
        if shape == 'square':
            pygame.draw.rect(self.screen, color, [x, y, 50, 50])

    def write_template(self, score=0, level=1):
        font = pygame.font.Font('freesansbold.ttf', 40)
        score_text = font.render('Your score is: {}'.format(score), True, (255, 255, 255), (0, 0, 0))
        level_text = font.render('Level: {}'.format(level), True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(score_text, (5, 15))
        self.screen.blit(level_text, (500, 15))

    def write_win(self):
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render('You are winner! Well done!', True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (200, 400))

    def write_next_level(self, score, circles, squares):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('To next level you need:', True, (255, 255, 255), (0, 0, 0))
        score_text = font.render('Score: {}'.format(score), True, (255, 255, 255), (0, 0, 0))
        circle_text = font.render('Circles: {}'.format(circles), True, (255, 255, 255), (0, 0, 0))
        square_text = font.render('Squares: {}'.format(squares), True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (750, 5))
        self.screen.blit(score_text, (750, 25))
        self.screen.blit(circle_text, (750, 50))
        self.screen.blit(square_text, (750, 75))

    def write_rules(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        score_text = font.render('Score booster: 100', True, (255, 255, 255), (0, 0, 0))
        circle_text = font.render('Circle: 30', True, (255, 255, 255), (0, 0, 0))
        square_text = font.render('Square: 20', True, (255, 255, 255), (0, 0, 0))
        score_press = font.render('Press: b', True, (255, 255, 255), (0, 0, 0))
        circle_press = font.render('Press: c', True, (255, 255, 255), (0, 0, 0))
        square_press = font.render('Press: s', True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(score_text, (50, 710))
        self.screen.blit(circle_text, (400, 710))
        self.screen.blit(square_text, (700, 710))
        self.screen.blit(score_press, (50, 745))
        self.screen.blit(circle_press, (400, 745))
        self.screen.blit(square_press, (700, 745))


class Object:
    Vx = 2
    Vy = 2
    x = 500
    y = 400
    colors = [(0, 225, 0), (0, 0, 255), (255, 0, 0), (255, 0, 255), (0, 255, 255), (255, 255, 0)]

    def __init__(self, shape):
        self.color = random.choice(self.colors)
        self.Vx = random.randint(1, 5)
        self.Vy = random.randint(1, 3)
        self.shape = shape

    def move(self):
        self.x += self.Vx
        self.y += self.Vy
        if self.shape == 'circle':
            if self.x >= 975 or self.x <= 25:
                self.Vx = -self.Vx
            if self.y >= 680 or self.y <= 120:
                self.Vy = -self.Vy
        else:
            if self.x >= 950 or self.x <= 0:
                self.Vx = -self.Vx
            if self.y >= 660 or self.y <= 110:
                self.Vy = -self.Vy

    def draw(self):
        self.move()
        return [self.shape, self.color, self.x, self.y]


class Game(Window):
    win = False
    score = 0
    level = 1
    boost = 2
    circles = []
    squares = []
    # score, circles, squares
    levels = [[100, 1, 1],
              [1000, 5, 10],
              [10000, 30, 25],
              [100000, 45, 60],
              [1000000, 100, 100]]

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
                        if event.key == pygame.K_c:
                            if self.score >= 30:
                                self.circles.append(Object('circle'))
                                self.score -= 30
                        if event.key == pygame.K_s:
                            if self.score >= 20:
                                self.squares.append((Object('square')))
                                self.score -= 20
                        if event.key == pygame.K_b:
                            if self.score >= 100:
                                self.boost += 2
                                self.score -= 100
                    else:
                        if event.key == pygame.K_SPACE:
                            self.boost = 2
                            self.score = 0
                            self.level = 1
                            self.win = False
                            self.circles.clear()
                            self.squares.clear()

            self.screen.fill((0, 0, 0))
            super().write_template(self.score, self.level)
            super().write_rules()

            for figure in self.circles:
                l = figure.draw()
                super().draw_obj(l[0], l[1], l[2], l[3])

            for figure in self.squares:
                l = figure.draw()
                super().draw_obj(l[0], l[1], l[2], l[3])

            if self.level >= 5:
                self.win = True
                super().write_win()
            else:
                if self.score >= self.levels[self.level - 1][0]:
                    if len(self.circles) >= self.levels[self.level - 1][1]:
                        if len(self.squares) >= self.levels[self.level - 1][2]:
                            self.level += 1
                            self.squares.clear()
                            self.circles.clear()
                            self.score = 0
                super().write_next_level(max(self.levels[self.level - 1][0] - self.score, 0),
                                         max(self.levels[self.level - 1][1] - len(self.circles), 0),
                                         max(self.levels[self.level - 1][2] - len(self.squares), 0))

            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
