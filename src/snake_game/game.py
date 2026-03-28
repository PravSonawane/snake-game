import pygame
import sys

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

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
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
