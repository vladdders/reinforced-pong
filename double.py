import pygame

import constants
from paddle import Paddle
from ball import Ball


class Game(object):
    # https://www.101computing.net/pong-tutorial-using-pygame-adding-a-referee-system/

    def __init__(self):
        pygame.init()

        self._is_running = True
        self._no_winner = True

        self._winning_screen_running = False

        self.score_font = pygame.font.Font(None, 74)
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)
        pygame.display.set_caption(constants.GAME_NAME)
        self.sprites_list = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(constants.WHITE, constants.PADDLE_W, constants.PADDLE_H)
        self.right_paddle = Paddle(constants.WHITE, constants.PADDLE_W, constants.PADDLE_H)

        self.ball = Ball(constants.WHITE, constants.BALL_WIDTH, constants.BALL_HEIGHT)

        self.sprites_list.add(self.left_paddle)
        self.sprites_list.add(self.right_paddle)
        self.sprites_list.add(self.ball)

        self.initialise_positions_and_scores()

    def initialise_positions_and_scores(self):
        self.left_paddle.rect.x = constants.LEFTPADDLE_X
        self.left_paddle.rect.y = constants.LEFTPADDLE_Y

        self.right_paddle.rect.x = constants.RIGHTPADDLE_X
        self.right_paddle.rect.y = constants.LEFTPADDLE_Y

        self.ball.rect.x = constants.BALL_X
        self.ball.rect.y = constants.BALL_Y

        self._score_left = 3
        self._score_right = 3

        self.sprites_list.update()

    def key_event_listener(self, winning_screen=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False

                if winning_screen:
                    self._winning_screen_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._is_running = False

                    if winning_screen:
                        self._winning_screen_running = False

            if winning_screen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._winning_screen_running = False

    def move_paddles(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move_up(constants.PADDLE_SPEED)
        if keys[pygame.K_s]:
            self.left_paddle.move_down(constants.PADDLE_SPEED)
        if keys[pygame.K_UP]:
            self.right_paddle.move_up(constants.PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down(constants.PADDLE_SPEED)

        self.sprites_list.update()

    def paddle_ball_collision(self):
        if pygame.sprite.collide_mask(self.ball, self.left_paddle) or \
                pygame.sprite.collide_mask(self.ball, self.right_paddle):
            self.ball.bounce()

    def referee(self):
        if self.ball.rect.x >= constants.X_LIMIT:
            self._score_left += 1
            self._score_right -= 1
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.x <= 0:
            self._score_left -= 1
            self._score_right += 1
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.y > constants.Y_LIMIT:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

    def display_scores(self):
        text = self.score_font.render(str(self._score_left), 1, constants.WHITE)
        self.screen.blit(text, constants.LEFTSCORE_POS)
        text = self.score_font.render(str(self._score_right), 1, constants.WHITE)
        self.screen.blit(text, constants.RIGHTSCORE_POS)

    def render_components(self):
        self.screen.fill(constants.BLACK)
        self.sprites_list.draw(self.screen)

    def get_winner(self):

        if self._score_left <= 0:
            self.show_winning_screen("Right won!(space to reset)")

        if self._score_right <= 0:
            self.show_winning_screen("Left won!(space to reset)")

    def show_winning_screen(self, string):
        self._winning_screen_running = True
        self.screen.fill(constants.BLACK)
        text_surface = self.score_font.render(string, 1, constants.WHITE)
        self.screen.blit(text_surface, (50, 200))
        pygame.display.flip()
        while self._winning_screen_running:
            self.key_event_listener(winning_screen=True)
            self.clock.tick(constants.FPS)

        self.initialise_positions_and_scores()

    def loop(self):

        while self._is_running:

            self.key_event_listener()

            self.move_paddles()

            self.referee()

            self.paddle_ball_collision()

            self.render_components()

            self.display_scores()

            self.get_winner()

            pygame.display.flip()
            self.clock.tick(constants.FPS)

        pygame.quit()


def main():
    a = Game()
    a.loop()


if __name__ == '__main__':
    main()
