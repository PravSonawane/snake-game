# Snake Game

A hello world Python project setup that is buildable and testable.

## Setup

Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the project with development dependencies:
```bash
pip install -e ".[dev]"
```

## Running the application

```bash
snake-game
```
Or run the entrypoint directly:
```bash
python -m snake_game.main
```

## Running tests

```bash
pytest
```
