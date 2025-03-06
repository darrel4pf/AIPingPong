import pygame
import math
import random


class PongBall:  # Renamed from Ball
    MAX_SPEED = 5  # Renamed from MAX_VEL
    SIZE = 7  # Renamed from RADIUS

    def __init__(self, x, y):
        self.x = self.start_x = x  # Renamed from original_x
        self.y = self.start_y = y  # Renamed from original_y
        
        angle = self._generate_launch_angle(-30, 30, [0])  # Renamed from _get_random_angle
        direction = 1 if random.random() < 0.5 else -1  # Renamed from pos

        self.velocity_x = direction * abs(math.cos(angle) * self.MAX_SPEED)  # Renamed from x_vel
        self.velocity_y = math.sin(angle) * self.MAX_SPEED  # Renamed from y_vel

    def _generate_launch_angle(self, min_angle, max_angle, excluded):  # Renamed from _get_random_angle
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, window):  # Renamed parameter from win to window
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), self.SIZE)

    def update_position(self):  # Renamed from move
        self.x += self.velocity_x
        self.y += self.velocity_y

    def reset_position(self):  # Renamed from reset
        self.x = self.start_x
        self.y = self.start_y

        angle = self._generate_launch_angle(-30, 30, [0])
        speed_x = abs(math.cos(angle) * self.MAX_SPEED)  # Renamed from x_vel
        speed_y = math.sin(angle) * self.MAX_SPEED  # Renamed from y_vel

        self.velocity_y = speed_y
        self.velocity_x *= -1