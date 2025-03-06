from .paddle import PlayerPaddle
from .ball import PongBall  # Updated import
import pygame
import random
pygame.init()


class MatchStats:  # Renamed from GameInformation
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class PongMatch:  # Renamed from Game
    """
    To use this class, initialize an instance and call the .update() method
    inside a pygame event loop (i.e., while loop). Inside your event loop,
    you can call the .render() and .move_player() methods according to your use case.
    Use the information returned from .update() to determine when to end the game by calling
    .reset().
    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.left_player = PlayerPaddle(  # Renamed from left_paddle
            10, self.window_height // 2 - PlayerPaddle.HEIGHT // 2)
        self.right_player = PlayerPaddle(  # Renamed from right_paddle
            self.window_width - 10 - PlayerPaddle.WIDTH, self.window_height // 2 - PlayerPaddle.HEIGHT // 2)
        self.ball = PongBall(self.window_width // 2, self.window_height // 2)  # Updated class name

        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.window = window

    def _render_score(self):  # Renamed from _draw_score
        left_score_text = self.SCORE_FONT.render(
            f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(
            f"{self.right_score}", 1, self.WHITE)
        self.window.blit(left_score_text, (self.window_width //
                                           4 - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, (self.window_width * (3 / 4) -
                                            right_score_text.get_width() // 2, 20))

    def _render_hits(self):  # Renamed from _draw_hits
        hits_text = self.SCORE_FONT.render(
            f"{self.left_hits + self.right_hits}", 1, self.RED)
        self.window.blit(hits_text, (self.window_width //
                                     2 - hits_text.get_width() // 2, 10))

    def _render_divider(self):  # Renamed from _draw_divider
        for i in range(10, self.window_height, self.window_height // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.window, self.WHITE, (self.window_width // 2 - 5, i, 10, self.window_height // 20))

    def _handle_ball_collision(self):  # Renamed from _handle_collision
        ball = self.ball
        left_player = self.left_player  # Renamed from left_paddle
        right_player = self.right_player  # Renamed from right_paddle

        if ball.y + ball.SIZE >= self.window_height:  # Updated from RADIUS to SIZE
            ball.velocity_y *= -1  # Updated from y_vel to velocity_y
        elif ball.y - ball.SIZE <= 0:
            ball.velocity_y *= -1

        if ball.velocity_x < 0:  # Updated from x_vel to velocity_x
            if ball.y >= left_player.y and ball.y <= left_player.y + PlayerPaddle.HEIGHT:
                if ball.x - ball.SIZE <= left_player.x + PlayerPaddle.WIDTH:
                    ball.velocity_x *= -1

                    middle_y = left_player.y + PlayerPaddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (PlayerPaddle.HEIGHT / 2) / ball.MAX_SPEED  # Updated from MAX_VEL to MAX_SPEED
                    y_vel = difference_in_y / reduction_factor
                    ball.velocity_y = -1 * y_vel
                    self.left_hits += 1

        else:
            if ball.y >= right_player.y and ball.y <= right_player.y + PlayerPaddle.HEIGHT:
                if ball.x + ball.SIZE >= right_player.x:
                    ball.velocity_x *= -1

                    middle_y = right_player.y + PlayerPaddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (PlayerPaddle.HEIGHT / 2) / ball.MAX_SPEED
                    y_vel = difference_in_y / reduction_factor
                    ball.velocity_y = -1 * y_vel
                    self.right_hits += 1

    def render(self, draw_score=True, draw_hits=False):  # Renamed from draw
        self.window.fill(self.BLACK)

        self._render_divider()

        if draw_score:
            self._render_score()

        if draw_hits:
            self._render_hits()

        for player in [self.left_player, self.right_player]:  # Renamed from paddle to player
            player.draw(self.window)

        self.ball.draw(self.window)

    def move_player(self, left=True, up=True):  # Renamed from move_paddle
        """
        Move the left or right player.

        :returns: boolean indicating if player movement is valid.
                  Movement is invalid if it causes the player to go
                  off the screen.
        """
        if left:
            if up and self.left_player.y - PlayerPaddle.SPEED < 0:
                return False
            if not up and self.left_player.y + PlayerPaddle.HEIGHT > self.window_height:
                return False
            self.left_player.move(up)
        else:
            if up and self.right_player.y - PlayerPaddle.SPEED < 0:
                return False
            if not up and self.right_player.y + PlayerPaddle.HEIGHT > self.window_height:
                return False
            self.right_player.move(up)

        return True

    def update(self):  # Renamed from loop
        """
        Executes a single game loop.

        :returns: MatchStats instance stating score
                  and hits of each player.
        """
        self.ball.update_position()  # Renamed from move
        self._handle_ball_collision()

        if self.ball.x < 0:
            self.ball.reset_position()  # Renamed from reset
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset_position()
            self.left_score += 1

        match_stats = MatchStats(  # Renamed from GameInformation
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return match_stats

    def reset(self):
        """Resets the entire game."""
        self.ball.reset_position()  # Renamed from reset
        self.left_player.reset()
        self.right_player.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0