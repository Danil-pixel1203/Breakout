from time import sleep

import pygame as pg
import sys
from random import randrange

from pygame.mixer import Sound


class Game:
    def __init__(self):
        pg.init()
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption('Breakout')

        self.paddle = Paddle(self)
        self.ball = Ball(self)
        self.sound = pg.mixer.Sound("joshua-mclean-mountain-trials.mp3")
        self.sound.set_volume(0.2)
        self.sound.play(-1)

        self.sound2 = pg.mixer.Sound("0961f580f9e00da (1).mp3")
        self.sound2.set_volume(0.2)
        self.FPS = 120  # FPS
        self.clock = pg.time.Clock()

        self.image = pg.image.load('bg.jpg').convert()

        self.block_list = [pg.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)] # список блоков

        self.color_list = [(randrange(30, 256), randrange(30, 256), randrange(30, 256)) for _ in range(10) for _ in range(4)] # список цветов блоков

    def update(self):
        self.paddle.update()
        self.ball.update()
        pg.display.flip()
        self.clock.tick(self.FPS)

    def draw(self):
        self.screen.blit(self.image, (0, 0))

        for color, block in enumerate(self.block_list):
            pg.draw.rect(self.screen, self.color_list[color], block)

        self.paddle.draw()
        self.ball.draw()

    def check_game_over(self):
        if self.ball.ball.bottom > self.HEIGHT:
            self.sound.stop()
            self.sound2.play()
            sleep(1.5)
            self.sound2.stop()
            print('GAME OVER!')
            sleep(1)
            game = Game()
            game.run()
        elif not len(self.block_list):
            print('WIN!!!')
            sleep(1)
            game = Game()
            game.run()

    @staticmethod
    def check_events():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()



    def run(self):
        while True:
            self.check_game_over()
            self.check_events()
            self.update()
            self.draw()


class Paddle:
    def __init__(self, root: Game):
        self.game = root
        self.paddle_w = 250
        self.paddle_h = 30
        self.paddle_speed = 15
        self.rect = pg.Rect(root.WIDTH // 2 - self.paddle_w // 2,
                            root.HEIGHT - self.paddle_h - 10,
                            self.paddle_w, self.paddle_h)

        self.color = pg.Color(200, 130, 50)

    def draw(self):
        pg.draw.rect(self.game.screen, self.color, self.rect)

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_a] and self.rect.left > 0:
            self.rect.left -= self.paddle_speed
        elif key[pg.K_d] and self.rect.right < self.game.WIDTH:
            self.rect.right += self.paddle_speed

class Ball:
    def __init__(self, root: Game):
        self.game = root
        self.radius = 20
        self.speed = 6

        self.rect = int(self.radius * 2 ** 0.5)

        self.ball = pg.Rect(randrange(self.rect, self.game.WIDTH- self.rect),
                            self.game.HEIGHT // 2, self.rect, self.rect)
        self.dx, self.dy = 1, -1
        self.sound1 = pg.mixer.Sound("jg-032316-sfx-8-bit-hit-6.mp3")
        self.sound1.set_volume(0.2)
    def draw(self):
        pg.draw.circle(self.game.screen,
                       pg.Color(255, 255, 255),
                       self.ball.center,
                       self.radius)

    def move(self):
        self.ball.x += self.speed * self.dx
        self.ball.y += self.speed * self.dy

    def check_collisions(self):
        if self.ball.centerx < self.radius or self.ball.centerx > self.game.WIDTH - self.radius:
            self.dx = -self.dx

        if self.ball.centery < self.radius:
            self.dy = -self.dy

    def calculate_movement(self, rect):
        if self.dx > 0:
            delta_x = self.ball.right - rect.left
        else:
            delta_x = rect.right - self.ball.left

        if self.dy > 0:
            delta_y = self.ball.bottom - rect.top
            self.sound1.play()
        else:
            delta_y = rect.bottom - self.ball.top

        if abs(delta_x - delta_y) < 10:
            self.dx, self.dy = -self.dx, -self.dy

        elif delta_x > delta_y:
            self.dy = -self.dy

        elif delta_x < delta_y:
            self.dx = -self.dx

    def check_paddle(self):
        if self.ball.colliderect(self.game.paddle) and self.dy > 0:

            self.calculate_movement(self.game.paddle.rect)

    def check_block_collision(self):
        hit_index = self.ball.collidelist(self.game.block_list)

        if hit_index != -1:
            hit_rect = self.game.block_list.pop(hit_index)
            self.game.color_list.pop(hit_index)
            self.calculate_movement(hit_rect)
            self.game.FPS += 2

    def update(self):
        self.move()
        self.check_collisions()
        self.check_paddle()
        self.check_block_collision()

if __name__ == '__main__':
    game = Game()
    game.run()