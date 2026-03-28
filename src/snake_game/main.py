import sys
from snake_game.game import SnakeGame

def main():
    game = SnakeGame()
    try:
        game.run()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
