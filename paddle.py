import pygame

import constants


class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super(Paddle, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLACK)
        self.image.set_colorkey(constants.BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400