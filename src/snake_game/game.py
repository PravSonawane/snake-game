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
        self.game_over = False

        # Initial snake setup
        self.block_size = 20
        self.snake_pos = [self.width // 2, self.height // 2]
        self.snake_body = [list(self.snake_pos)]
        self.snake_color = (0, 255, 0)
        self.snake_vel_x = 0
        self.snake_vel_y = 0
        self.snake_speed = self.block_size

        # Food setup
        self.food_color = (255, 0, 0)
        self.food_pos = [
            random.randrange(0, self.width // self.block_size) * self.block_size,
            random.randrange(0, self.height // self.block_size) * self.block_size
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
        if self.game_over:
            return

        # Do not update game state if the snake hasn't started moving
        if self.snake_vel_x == 0 and self.snake_vel_y == 0:
            return

        self.snake_pos[0] += self.snake_vel_x
        self.snake_pos[1] += self.snake_vel_y

        # Boundary collision
        if (self.snake_pos[0] < 0 or self.snake_pos[0] >= self.width or
            self.snake_pos[1] < 0 or self.snake_pos[1] >= self.height):
            self.game_over = True
            return

        # Self collision
        if list(self.snake_pos) in self.snake_body:
            self.game_over = True
            return

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.food_pos = [
                random.randrange(0, self.width // self.block_size) * self.block_size,
                random.randrange(0, self.height // self.block_size) * self.block_size
            ]
        else:
            self.snake_body.pop()

    def draw(self):
        # Fill the screen with a dark background
        self.screen.fill((30, 30, 30))

        # Draw the snake
        for block in self.snake_body:
            pygame.draw.rect(
                self.screen, 
                self.snake_color, 
                pygame.Rect(
                    block[0], 
                    block[1], 
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
        
        if self.game_over:
            font = pygame.font.SysFont(None, 75)
            text = font.render("Game Over", True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            # Lower tick rate for grid-based discrete movement
            self.clock.tick(10)
        
        pygame.quit()
        sys.exit()
