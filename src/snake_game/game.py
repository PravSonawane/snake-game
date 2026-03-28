import pygame
import sys
import random

class SnakeGame:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initial snake setup
        self.block_size = 20
        self.snake_pos = [self.width // 2, self.height // 2]
        self.snake_color = (0, 255, 0)
        self.snake_vel_x = 0
        self.snake_vel_y = 0
        self.snake_speed = 2

        # Food setup
        self.food_color = (255, 0, 0)
        self.food_pos = [
            random.randrange(0, (self.width - self.block_size) // self.block_size) * self.block_size,
            random.randrange(0, (self.height - self.block_size) // self.block_size) * self.block_size
        ]
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.snake_vel_x = 0
                    self.snake_vel_y = -self.snake_speed
                elif event.key == pygame.K_DOWN:
                    self.snake_vel_x = 0
                    self.snake_vel_y = self.snake_speed
                elif event.key == pygame.K_LEFT:
                    self.snake_vel_x = -self.snake_speed
                    self.snake_vel_y = 0
                elif event.key == pygame.K_RIGHT:
                    self.snake_vel_x = self.snake_speed
                    self.snake_vel_y = 0

    def update(self):
        self.snake_pos[0] += self.snake_vel_x
        self.snake_pos[1] += self.snake_vel_y

    def draw(self):
        # Fill the screen with a dark background
        self.screen.fill((30, 30, 30))
        
        # Draw the snake
        pygame.draw.rect(
            self.screen, 
            self.snake_color, 
            pygame.Rect(
                self.snake_pos[0], 
                self.snake_pos[1], 
                self.block_size, 
                self.block_size
            )
        )

        # Draw the food
        pygame.draw.rect(
            self.screen,
            self.food_color,
            pygame.Rect(
                self.food_pos[0],
                self.food_pos[1],
                self.block_size,
                self.block_size
            )
        )
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
