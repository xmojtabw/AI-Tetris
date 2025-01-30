import pygame
import pygame.examples
from board import Board 



# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600  # Full game window dimensions
BOARD_WIDTH, BOARD_HEIGHT = 300, 600   # Play area dimensions
SIDE_PANEL_WIDTH = SCREEN_WIDTH - BOARD_WIDTH  # Width of the side panel
CELL_SIZE = 30  # Size of each block in pixels

# Colors
BLACK = (0, 0, 0)
GRAY = (128,128,128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = None
clock = None


def init_the_screen():
    global screen
    global clock
    # Initialize Pygame
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()

# Draw the board background
def draw_board_background(screen):
    pygame.draw.rect(screen, GRAY, (0, 0, BOARD_WIDTH, BOARD_HEIGHT))


# Draw the side panel background
def draw_side_panel(screen):
    pygame.draw.rect(screen, BLACK, (BOARD_WIDTH, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT))

def draw_board(screen,board:Board):
    reversed_board = board.board[::-1]
    for i in range(board.height):
        for j in range(board.width):
            x = j * CELL_SIZE 
            y = i * CELL_SIZE 
            if reversed_board[i][j]["fill"]:
                pygame.draw.rect(
                    screen,
                    reversed_board[i][j]["color"],
                    (x, y, CELL_SIZE, CELL_SIZE),
                )
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

# Draw the labels on the side panel
def draw_labels(screen, labels):
    # Score
    score_text = pygame.font.Font(None,20).render(f"Score: {labels['score']}", True, WHITE)
    screen.blit(score_text, (BOARD_WIDTH + 20, 80))

    # Additional Info
    lines_text = pygame.font.Font(None,25).render(f"Lines Cleared: {labels['lines']}", True, WHITE)
    screen.blit(lines_text, (BOARD_WIDTH + 20, 100))

    lines_text = pygame.font.Font(None,25).render(f"Evaluation: {labels['eval']}", True, WHITE)
    screen.blit(lines_text, (BOARD_WIDTH + 20, 120))

    # wait ... 
    if labels['wait']:
        lines_text = pygame.font.Font(None, 25).render(f"{labels['wait']}", True, WHITE)
        screen.blit(lines_text, (BOARD_WIDTH + 20, 140))

# Draw the menu panel
def draw_panel(screen):
    menu_rect = pygame.Rect(BOARD_WIDTH, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, BLACK, menu_rect)
    pygame.draw.rect(screen, WHITE, menu_rect, 2)  # Outline the menu panel

    # Example menu text
    font = pygame.font.Font(None, 36)
    text = font.render("Panel", True, WHITE)
    screen.blit(text, (BOARD_WIDTH + 10, 10))


# Main game loop
def display(board : Board,labels=None):
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

    # Clear the screen
    screen.fill(GRAY)

    # Draw the Tetris piece
    draw_board(screen, board)
    # Draw the panel
    draw_panel(screen)
    # Draw the labels
    draw_labels(screen=screen, labels=labels)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(50)
    if quit:
        pygame.quit()
        return False
    else:
        return True


