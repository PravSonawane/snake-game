import pygame
from abc import ABC, abstractmethod

class GameState(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class PlayingState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key == pygame.K_UP:
                    self.game.snake.change_direction(0, -self.game.snake.speed)
                elif event.key == pygame.K_DOWN:
                    self.game.snake.change_direction(0, self.game.snake.speed)
                elif event.key == pygame.K_LEFT:
                    self.game.snake.change_direction(-self.game.snake.speed, 0)
                elif event.key == pygame.K_RIGHT:
                    self.game.snake.change_direction(self.game.snake.speed, 0)

    def update(self):
        if not self.game.snake.is_moving():
            return

        new_head = self.game.snake.move()

        # Boundary collision
        if (new_head[0] < 0 or new_head[0] >= self.game.width or
            new_head[1] < 0 or new_head[1] >= self.game.height):
            self.game.change_state(GameOverState(self.game))
            return

        # Self collision
        if self.game.snake.check_self_collision(new_head):
            self.game.change_state(GameOverState(self.game))
            return

        # Eating Food
        if new_head == self.game.food.position:
            self.game.score += 1
            self.game.food.respawn()
        else:
            self.game.snake.shrink()

    def draw(self, screen):
        self.game.snake.draw(screen, self.game.score_height)
        self.game.food.draw(screen, self.game.score_height)

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.selected_option = 0
        self.new_game_rect = pygame.Rect(0, 0, 0, 0)
        self.quit_rect = pygame.Rect(0, 0, 0, 0)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.new_game_rect.collidepoint(event.pos):
                    self.game.reset()
                elif self.quit_rect.collidepoint(event.pos):
                    self.game.running = False
            elif event.type == pygame.MOUSEMOTION:
                if self.new_game_rect.collidepoint(event.pos):
                    self.selected_option = 0
                elif self.quit_rect.collidepoint(event.pos):
                    self.selected_option = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % 2
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        self.game.reset()
                    else:
                        self.game.running = False

    def update(self):
        pass # No updates needed in game over state

    def draw(self, screen):
        # Draw snake and food beneath the overlay
        self.game.snake.draw(screen, self.game.score_height)
        self.game.food.draw(screen, self.game.score_height)

        font = pygame.font.SysFont(None, 75)
        text = font.render("Game Over", True, (248, 113, 113)) # Tailwind Red 400
        text_rect = text.get_rect(center=(self.game.width // 2, self.game.score_height + self.game.height // 2 - 50))
        screen.blit(text, text_rect)

        option_font = pygame.font.SysFont(None, 50)
        
        # New Game option
        new_game_color = (255, 255, 255) if self.selected_option == 0 else (148, 163, 184)
        new_game_text = option_font.render("New Game", True, new_game_color)
        self.new_game_rect = new_game_text.get_rect(center=(self.game.width // 2, self.game.score_height + self.game.height // 2 + 20))
        screen.blit(new_game_text, self.new_game_rect)

        # Quit option
        quit_color = (255, 255, 255) if self.selected_option == 1 else (148, 163, 184)
        quit_text = option_font.render("Quit", True, quit_color)
        self.quit_rect = quit_text.get_rect(center=(self.game.width // 2, self.game.score_height + self.game.height // 2 + 70))
        screen.blit(quit_text, self.quit_rect)
