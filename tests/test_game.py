import pygame
import pytest
from snake_game.game import SnakeGame

def test_initialization():
    game = SnakeGame(800, 600)
    assert game.width == 800
    assert game.height == 600
    assert game.running is True
    assert game.game_over is False
    assert game.game_over_selected_option == 0
    assert game.new_game_rect == pygame.Rect(0, 0, 0, 0)
    assert game.quit_rect == pygame.Rect(0, 0, 0, 0)
    assert game.block_size == 20
    assert game.snake_pos == [400, 300]
    assert game.snake_body == [[400, 300]]
    assert game.snake_vel_x == 0
    assert game.snake_vel_y == 0
    assert game.snake_speed == game.block_size
    assert game.snake_color == (52, 211, 153)
    assert game.food_color == (244, 63, 94)
    assert game.score == 0
    assert game.score_height == 40

    # Food bounds and constraints
    assert 0 <= game.food_pos[0] < game.width
    assert 0 <= game.food_pos[1] < game.height
    assert game.food_pos[0] % game.block_size == 0
    assert game.food_pos[1] % game.block_size == 0

def test_handle_events_quit():
    game = SnakeGame()
    event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(event)
    game.handle_events()
    assert game.running is False

def test_handle_events_escape():
    game = SnakeGame()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    pygame.event.post(event)
    game.handle_events()
    assert game.running is False

def test_handle_events_movement():
    game = SnakeGame()

    # Move up
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    pygame.event.post(event)
    game.handle_events()
    assert game.snake_vel_x == 0
    assert game.snake_vel_y == -game.snake_speed

    # Move down
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    pygame.event.post(event)
    game.handle_events()
    assert game.snake_vel_x == 0
    assert game.snake_vel_y == game.snake_speed

    # Move left
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
    pygame.event.post(event)
    game.handle_events()
    assert game.snake_vel_x == -game.snake_speed
    assert game.snake_vel_y == 0

    # Move right
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
    pygame.event.post(event)
    game.handle_events()
    assert game.snake_vel_x == game.snake_speed
    assert game.snake_vel_y == 0

def test_handle_events_ignore_opposite_direction():
    game = SnakeGame()
    game.snake_body = [[100, 100], [80, 100]] # length > 1
    
    # Moving right currently
    game.snake_vel_x = game.snake_speed
    game.snake_vel_y = 0

    # Try to move left, should be ignored
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
    pygame.event.post(event)
    game.handle_events()
    assert game.snake_vel_x == game.snake_speed
    assert game.snake_vel_y == 0

def test_update():
    game = SnakeGame()
    game.snake_pos = [100, 100]
    game.snake_body = [[100, 100]]
    game.snake_vel_x = game.snake_speed
    game.snake_vel_y = 0
    game.update()
    assert game.snake_pos == [100 + game.snake_speed, 100]
    assert game.snake_body == [[100 + game.snake_speed, 100]]

def test_update_eats_food():
    game = SnakeGame()
    game.snake_pos = [100, 100]
    game.snake_body = [[100, 100]]
    game.food_pos = [100 + game.snake_speed, 100]
    game.snake_vel_x = game.snake_speed
    game.snake_vel_y = 0
    game.score = 0
    game.update()
    assert game.snake_pos == [100 + game.snake_speed, 100]
    assert len(game.snake_body) == 2
    assert game.snake_body == [[100 + game.snake_speed, 100], [100, 100]]
    assert game.food_pos != [100 + game.snake_speed, 100]
    assert game.score == 1

def test_draw():
    # Simple check to ensure draw doesn't completely blow up
    game = SnakeGame()
    game.draw()
    # If no exceptions are raised it indicates `draw` logic 
    # executes successfully on the headless display.
    assert True

def test_update_boundary_collision():
    game = SnakeGame(800, 600)
    game.snake_pos = [780, 100]
    game.snake_vel_x = game.snake_speed
    game.snake_vel_y = 0
    game.update()
    # at next step, x becomes 800, and width is 800. 800 >= 800 so collision!
    assert game.game_over is True

def test_update_game_over_state_does_not_move():
    game = SnakeGame(800, 600)
    game.game_over = True
    game.snake_pos = [100, 100]
    game.snake_vel_x = game.snake_speed
    game.snake_vel_y = 0
    game.update()
    assert game.snake_pos == [100, 100]

def test_update_self_collision():
    game = SnakeGame(800, 600)
    # Simulate a snake with a body spanning 5 blocks
    game.snake_pos = [100, 100]
    game.snake_body = [[100, 100], [80, 100], [80, 80], [100, 80], [120, 80]] 
    # Moving up into its own body: new head would be [100, 80], which is in snake_body
    game.snake_vel_x = 0
    game.snake_vel_y = -game.snake_speed
    game.update()
    assert game.game_over is True

def test_reset_game():
    game = SnakeGame()
    game.score = 10
    game.game_over = True
    game.game_over_selected_option = 1
    game.snake_vel_x = game.snake_speed
    game.snake_body = [[100, 100], [80, 100]]
    
    game.reset_game()
    assert game.score == 0
    assert game.game_over is False
    assert game.game_over_selected_option == 0
    assert game.snake_vel_x == 0
    assert game.snake_vel_y == 0
    assert len(game.snake_body) == 1

def test_game_over_options_keyboard():
    game = SnakeGame()
    game.game_over = True
    
    # Down key
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    pygame.event.post(event)
    game.handle_events()
    assert game.game_over_selected_option == 1 # Quit

    # Up key
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    pygame.event.post(event)
    game.handle_events()
    assert game.game_over_selected_option == 0 # New Game
    
    # Enter key to reset
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    pygame.event.post(event)
    game.handle_events()
    assert game.game_over is False

    # Enter key to quit
    game.game_over = True
    game.game_over_selected_option = 1
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    pygame.event.post(event)
    game.handle_events()
    assert game.running is False

def test_game_over_options_mouse():
    game = SnakeGame()
    game.game_over = True
    game.new_game_rect = pygame.Rect(100, 100, 50, 50)
    game.quit_rect = pygame.Rect(100, 200, 50, 50)
    
    # Hover Quit
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(120, 220))
    pygame.event.post(event)
    game.handle_events()
    assert game.game_over_selected_option == 1

    # Hover New Game
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(120, 120))
    pygame.event.post(event)
    game.handle_events()
    assert game.game_over_selected_option == 0
    
    # Click Quit
    game.game_over_selected_option = 0
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(120, 220))
    pygame.event.post(event)
    game.handle_events()
    assert game.running is False

    # Click New Game
    game.running = True
    game.game_over = True
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(120, 120))
    pygame.event.post(event)
    game.handle_events()
    assert game.game_over is False

