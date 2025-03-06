import pygame


class PlayerPaddle:  # Renamed from Paddle
    SPEED = 4  # Renamed from VEL
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, x, y):
        self.x = self.start_x = x  # Renamed from original_x
        self.y = self.start_y = y  # Renamed from original_y

    def draw(self, window):  # Renamed parameter from win to window
        pygame.draw.rect(
            window, (255, 255, 255), (self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self, up=True):
        if up:
            self.y -= self.SPEED
        else:
            self.y += self.SPEED

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y