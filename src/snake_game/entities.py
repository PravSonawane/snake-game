import pygame
import random

class Snake:
    def __init__(self, block_size, start_x, start_y):
        self.block_size = int(block_size)
        self.positions = [[int(start_x), int(start_y)]]
        self.color = (52, 211, 153) # Tailwind Emerald 400
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = self.block_size

    def change_direction(self, dx, dy):
        """Update direction, ignoring reverse movements if snake length > 1."""
        if len(self.positions) > 1:
            if dx == -self.velocity_x and dx != 0:
                return
            if dy == -self.velocity_y and dy != 0:
                return
        self.velocity_x = dx
        self.velocity_y = dy
    
    def move(self):
        """Move snake forward and return the new head position."""
        head_x, head_y = self.positions[0]
        new_head = [head_x + self.velocity_x, head_y + self.velocity_y]
        self.positions.insert(0, new_head)
        return new_head
    
    def shrink(self):
        """Remove the last block of the snake's tail."""
        self.positions.pop()

    def check_self_collision(self, head):
        """Returns True if the head collides with any body part."""
        return head in self.positions[1:]

    def is_moving(self):
        """Returns True if the snake is currently moving."""
        return self.velocity_x != 0 or self.velocity_y != 0

    def draw(self, screen, offset_y):
        """Draw the snake blocks."""
        for block in self.positions:
            pygame.draw.rect(
                screen, 
                self.color, 
                pygame.Rect(
                    block[0], 
                    block[1] + offset_y, 
                    self.block_size, 
                    self.block_size
                )
            )

class Food:
    def __init__(self, block_size, width, height, color=(244, 63, 94)):
        self.block_size = block_size
        self.width = width
        self.height = height
        self.color = color
        self.position = [0, 0]
        self.respawn()

    def respawn(self):
        """Randomly reposition the food aligned with the grid."""
        self.position = [
            random.randrange(0, self.width // self.block_size) * self.block_size,
            random.randrange(0, self.height // self.block_size) * self.block_size
        ]

    def draw(self, screen, offset_y):
        """Draw the food."""
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.position[0],
                self.position[1] + offset_y,
                self.block_size,
                self.block_size
            )
        )
