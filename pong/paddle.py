import pygame

from pong import constants


class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super(Paddle, self).__init__()

        self.width = width
        self.height = height

        self._paddle_custom_speed = 60

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.BLACK)
        self.image.set_colorkey(constants.BLACK)

        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400

    def move_paddle_to_position(self, ball_y):

        while not self.rect.y < ball_y < self.rect.y + self.height and \
                0 < ball_y < constants.SCREEN_SIZE[1]:

            if ball_y > self.rect.y:
                self.move_down(self._paddle_custom_speed)

            elif ball_y < self.rect.y :
                self.move_up(self._paddle_custom_speed)

            else:
                break
