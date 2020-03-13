import pygame

from pong import constants
from pong.ball import Ball
from pong.paddle import Paddle


class Game(object):
    '''
    The game was built following the tutorial:
    https://www.101computing.net/pong-tutorial-using-pygame-adding-a-referee-system/
    '''

    def __init__(self):
        pygame.init()

        self.terminal = False
        self.reward = .1

        self._is_running = True

        self.score_font = pygame.font.Font(None, 75)
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)
        pygame.display.set_caption(constants.GAME_NAME)
        self.sprites_list = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(constants.WHITE, constants.PADDLE_W, constants.PADDLE_H)
        self.right_paddle = Paddle(constants.GREEN, constants.PADDLE_W, constants.PADDLE_H)

        self.ball = Ball(constants.WHITE, constants.BALL_WIDTH, constants.BALL_HEIGHT)

        self.sprites_list.add(self.left_paddle)
        self.sprites_list.add(self.right_paddle)
        self.sprites_list.add(self.ball)

        self.initialise_positions()

    def initialise_positions(self):
        self.left_paddle.rect.x = constants.LEFTPADDLE_X
        self.left_paddle.rect.y = constants.LEFTPADDLE_Y

        self.right_paddle.rect.x = constants.RIGHTPADDLE_X
        self.right_paddle.rect.y = constants.LEFTPADDLE_Y

        self.ball.rect.x = constants.BALL_X
        self.ball.rect.y = constants.BALL_Y

    def key_event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._is_running = False

    def _get_ball_y(self):
        return self.ball.rect.y

    def move_paddles(self, input_action):

        if input_action[0] == 1:
            self.left_paddle.move_up(constants.PADDLE_SPEED)
        if input_action[2] == 1:
            self.left_paddle.move_down(constants.PADDLE_SPEED)

        ball_y = self._get_ball_y()
        self.right_paddle.move_paddle_to_position(ball_y)

    def paddle_ball_collision(self):

        if self.right_paddle.rect.x == self.ball.rect.x or \
                self.left_paddle.rect.x == self.ball.rect.x:
            self.ball.rect.x -= 2

        if pygame.sprite.collide_rect(self.ball, self.left_paddle):
            self.ball.bounce()
            self.reward = 1

        if pygame.sprite.collide_rect(self.ball, self.right_paddle):
            self.ball.bounce()

    def referee(self):
        if self.ball.rect.x >= constants.X_LIMIT:
            self.reward = 1
            self.ball.velocity[0] = -self.ball.velocity[0]

        if self.ball.rect.x <= 0:
            self.terminal = True
            self.__init__()
            self.reward = -1
            self.ball.velocity[0] = -self.ball.velocity[0]

        if self.ball.rect.y >= constants.Y_LIMIT:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y <= 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

    def render_components(self):
        self.screen.fill(constants.BLACK)
        self.sprites_list.draw(self.screen)

    def frame_step(self, input_action):

        self.move_paddles(input_action)

        self.referee()

        self.paddle_ball_collision()

        self.sprites_list.update()

        self.render_components()

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        self.clock.tick(constants.FPS)

        return image_data, self.reward, self.terminal
