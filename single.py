import pygame

import constants
from paddle import Paddle
from ball import Ball


class Game(object):

    def __init__(self):
        pygame.init()

        self._no_winner = True

        self._winning_screen_running = False

        self.score_font = pygame.font.Font(None, 74)
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)
        pygame.display.set_caption(constants.GAME_NAME)
        self.sprites_list = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(constants.WHITE, constants.PADDLE_W, constants.PADDLE_H)

        self.ball = Ball(constants.WHITE, constants.BALL_WIDTH, constants.BALL_HEIGHT)

        self.sprites_list.add(self.left_paddle)
        self.sprites_list.add(self.ball)

        self.initialise_positions_and_scores()

    def initialise_positions_and_scores(self):
        self.left_paddle.rect.x = constants.LEFTPADDLE_X
        self.left_paddle.rect.y = constants.LEFTPADDLE_Y

        self.ball.rect.x = constants.BALL_X
        self.ball.rect.y = constants.BALL_Y

        self.reward = .1
        self.terminal = False

        self.score = 1

        self.sprites_list.update()

    def key_event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._is_running = False


    def move_paddles(self, input_action):
        if input_action[0] == 1:
            self.left_paddle.move_up(constants.PADDLE_SPEED)
        elif input_action[1] == 1:
            self.left_paddle.move_down(constants.PADDLE_SPEED)

        self.sprites_list.update()

    def paddle_ball_collision(self):
        if pygame.sprite.collide_mask(self.ball, self.left_paddle):
            self.ball.bounce()
            self.reward = 1

    def referee(self):
        if self.ball.rect.x >= constants.X_LIMIT:
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.x <= 0:
            self.score -= 1
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.y > constants.Y_LIMIT:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

    def display_scores(self):
        text = self.score_font.render(str(self.score), 1, constants.WHITE)
        self.screen.blit(text, constants.LEFTSCORE_POS)

    def render_components(self):
        self.screen.fill(constants.BLACK)
        self.sprites_list.draw(self.screen)

    def get_winner(self):

        if self.score <= 0:
            self.terminal = True
            self.__init__()
            self.reward = -1

    def frame_step(self, input_action):

        self.key_event_listener()

        self.move_paddles(input_action)

        self.referee()

        self.paddle_ball_collision()

        self.render_components()

        self.get_winner()

        pygame.display.flip()
        self.clock.tick(9999999999999999999)

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())

        return image_data, self.reward, self.terminal
