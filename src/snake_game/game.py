import pygame
import sys
import random

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
        self.game_over = False
        self.game_over_selected_option = 0
        self.new_game_rect = pygame.Rect(0, 0, 0, 0)
        self.quit_rect = pygame.Rect(0, 0, 0, 0)

        # Initial snake setup
        self.block_size = 20
        self.snake_pos = [self.width // 2, self.height // 2]
        self.snake_body = [list(self.snake_pos)]
        self.snake_color = (52, 211, 153) # Tailwind Emerald 400
        self.snake_vel_x = 0
        self.snake_vel_y = 0
        self.snake_speed = self.block_size

        # Food setup
        self.food_color = (244, 63, 94) # Tailwind Rose 500
        self.food_pos = [
            random.randrange(0, self.width // self.block_size) * self.block_size,
            random.randrange(0, self.height // self.block_size) * self.block_size
        ]
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over:
                    if self.new_game_rect.collidepoint(event.pos):
                        self.reset_game()
                    elif self.quit_rect.collidepoint(event.pos):
                        self.running = False
            elif event.type == pygame.MOUSEMOTION:
                if self.game_over:
                    if self.new_game_rect.collidepoint(event.pos):
                        self.game_over_selected_option = 0
                    elif self.quit_rect.collidepoint(event.pos):
                        self.game_over_selected_option = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.game_over:
                    if event.key == pygame.K_UP:
                        self.game_over_selected_option = (self.game_over_selected_option - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        self.game_over_selected_option = (self.game_over_selected_option + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if self.game_over_selected_option == 0:
                            self.reset_game()
                        else:
                            self.running = False
                else:
                    if event.key == pygame.K_UP:
                        if len(self.snake_body) == 1 or self.snake_vel_y != self.snake_speed:
                            self.snake_vel_x = 0
                            self.snake_vel_y = -self.snake_speed
                    elif event.key == pygame.K_DOWN:
                        if len(self.snake_body) == 1 or self.snake_vel_y != -self.snake_speed:
                            self.snake_vel_x = 0
                            self.snake_vel_y = self.snake_speed
                    elif event.key == pygame.K_LEFT:
                        if len(self.snake_body) == 1 or self.snake_vel_x != self.snake_speed:
                            self.snake_vel_x = -self.snake_speed
                            self.snake_vel_y = 0
                    elif event.key == pygame.K_RIGHT:
                        if len(self.snake_body) == 1 or self.snake_vel_x != -self.snake_speed:
                            self.snake_vel_x = self.snake_speed
                            self.snake_vel_y = 0

    def reset_game(self):
        self.score = 0
        self.snake_pos = [self.width // 2, self.height // 2]
        self.snake_body = [list(self.snake_pos)]
        self.snake_vel_x = 0
        self.snake_vel_y = 0
        self.food_pos = [
            random.randrange(0, self.width // self.block_size) * self.block_size,
            random.randrange(0, self.height // self.block_size) * self.block_size
        ]
        self.game_over = False
        self.game_over_selected_option = 0

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
            self.score += 1
            self.food_pos = [
                random.randrange(0, self.width // self.block_size) * self.block_size,
                random.randrange(0, self.height // self.block_size) * self.block_size
            ]
        else:
            self.snake_body.pop()

    def draw(self):
        # Fill the screen with a dark background
        self.screen.fill((15, 23, 42)) # Tailwind Slate 900

        # Draw the score background
        pygame.draw.rect(self.screen, (30, 41, 59), pygame.Rect(0, 0, self.width, self.score_height)) # Slate 800

        # Draw the score text on top right
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {self.score}", True, (248, 250, 252)) # Slate 50
        score_rect = score_text.get_rect(topright=(self.width - 20, 10))
        self.screen.blit(score_text, score_rect)

        # Draw the snake
        for block in self.snake_body:
            pygame.draw.rect(
                self.screen, 
                self.snake_color, 
                pygame.Rect(
                    block[0], 
                    block[1] + self.score_height, 
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
                self.food_pos[1] + self.score_height,
                self.block_size,
                self.block_size
            )
        )
        
        if self.game_over:
            font = pygame.font.SysFont(None, 75)
            text = font.render("Game Over", True, (248, 113, 113)) # Tailwind Red 400
            text_rect = text.get_rect(center=(self.width // 2, self.score_height + self.height // 2 - 50))
            self.screen.blit(text, text_rect)

            option_font = pygame.font.SysFont(None, 50)
            
            # New Game option
            new_game_color = (255, 255, 255) if self.game_over_selected_option == 0 else (148, 163, 184)
            new_game_text = option_font.render("New Game", True, new_game_color)
            self.new_game_rect = new_game_text.get_rect(center=(self.width // 2, self.score_height + self.height // 2 + 20))
            self.screen.blit(new_game_text, self.new_game_rect)

            # Quit option
            quit_color = (255, 255, 255) if self.game_over_selected_option == 1 else (148, 163, 184)
            quit_text = option_font.render("Quit", True, quit_color)
            self.quit_rect = quit_text.get_rect(center=(self.width // 2, self.score_height + self.height // 2 + 70))
            self.screen.blit(quit_text, self.quit_rect)

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
