import pygame
import pytest
from snake_game.game import SnakeGame

def test_initialization():
    game = SnakeGame(800, 600)
    assert game.width == 800
    assert game.height == 600
    assert game.running is True
    assert game.block_size == 20
    assert game.snake_pos == [400, 300]
    assert game.snake_vel_x == 0
    assert game.snake_vel_y == 0
    assert game.snake_speed == 2
    assert game.food_color == (255, 0, 0)

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

def test_update():
    game = SnakeGame()
    game.snake_pos = [100, 100]
    game.snake_vel_x = game.snake_speed
    game.snake_vel_y = 0
    game.update()
    assert game.snake_pos == [100 + game.snake_speed, 100]

def test_draw():
    # Simple check to ensure draw doesn't completely blow up
    game = SnakeGame()
    game.draw()
    # If no exceptions are raised it indicates `draw` logic 
    # executes successfully on the headless display.
    assert True
