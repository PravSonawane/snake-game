import os
import pytest

@pytest.fixture(autouse=True, scope="session")
def setup_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    import pygame
    pygame.init()
    yield
    pygame.quit()
