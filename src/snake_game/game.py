import pygame
import sys
from snake_game.entities import Snake, Food
from snake_game.states import PlayingState

class SnakeGame:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.score_height = 40
        self.score = 0
        self.screen = pygame.display.set_mode((self.width, self.height + self.score_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.block_size = 20
        self.snake = Snake(self.block_size, self.width // 2, self.height // 2)
        self.food = Food(self.block_size, self.width, self.height)

        self.current_state = PlayingState(self)

    def change_state(self, new_state):
        self.current_state = new_state

    def reset_game(self):
        self.score = 0
        self.snake = Snake(self.block_size, self.width // 2, self.height // 2)
        self.food.respawn()
        self.current_state = PlayingState(self)

    # Alias for ease of use in GameState
    def reset(self):
        self.reset_game()

    def handle_events(self):
        events = pygame.event.get()
        self.current_state.handle_events(events)

    def update(self):
        self.current_state.update()

    def draw(self):
        # Fill the screen with a dark background
        self.screen.fill((15, 23, 42)) # Slate 900

        # Draw the score background
        pygame.draw.rect(self.screen, (30, 41, 59), pygame.Rect(0, 0, self.width, self.score_height)) # Slate 800

        # Draw the score text on top right
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {self.score}", True, (248, 250, 252)) # Slate 50
        score_rect = score_text.get_rect(topright=(self.width - 20, 10))
        self.screen.blit(score_text, score_rect)

        # Delegate rest of drawing to current state
        self.current_state.draw(self.screen)

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
