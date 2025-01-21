import pygame

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600  # Total screen dimensions
MENU_WIDTH = 100  # Width of the menu panel
BOARD_WIDTH = SCREEN_WIDTH - MENU_WIDTH  # Width of the game board

CELL_SIZE = 30  # Size of each block in pixels

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris with Menu")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Example Tetris piece
piece = {
    "x": 120,  # X-coordinate of the top-left corner
    "y": 50,   # Y-coordinate of the top-left corner
    "color": BLUE,
    "shape": [
        ["X", "X", "X"],
        [".", "X", "."],
    ],
}

# Draw the game board
def draw_board(screen):
    board_rect = pygame.Rect(0, 0, BOARD_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, GRAY, board_rect)
    pygame.draw.rect(screen, WHITE, board_rect, 2)  # Outline the board

# Draw the menu panel
def draw_menu(screen):
    menu_rect = pygame.Rect(BOARD_WIDTH, 0, MENU_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, BLACK, menu_rect)
    pygame.draw.rect(screen, WHITE, menu_rect, 2)  # Outline the menu panel

    # Example menu text
    font = pygame.font.Font(None, 36)
    text = font.render("Menu", True, WHITE)
    screen.blit(text, (BOARD_WIDTH + 10, 10))

# Draw the Tetris piece
def draw_piece(screen, piece):
    for row_idx, row in enumerate(piece["shape"]):
        for col_idx, cell in enumerate(row):
            if cell == "X":  # Draw only filled cells
                x = piece["x"] + col_idx * CELL_SIZE
                y = piece["y"] + row_idx * CELL_SIZE
                pygame.draw.rect(
                    screen,
                    piece["color"],
                    (x, y, CELL_SIZE, CELL_SIZE),
                )
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

# Main game loop
def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Draw the board and menu
        draw_board(screen)
        draw_menu(screen)

        # Draw the Tetris piece
        draw_piece(screen, piece)

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
