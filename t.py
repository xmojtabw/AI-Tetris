import pygame
import pygame_menu
from pygame_menu import themes

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Menu settings
menu_width = 600
menu_height = SCREEN_HEIGHT

# Game area dimensions
game_width = SCREEN_WIDTH - menu_width
game_height = SCREEN_HEIGHT

# Create a menu
menu = pygame_menu.Menu(
    title="Tetris",
    width=menu_width,
    height=menu_height,
    theme=themes.THEME_DARK,
)

# Score variable
score = 0


def increase_score():
    global score
    score += 10
    # Update the label dynamically
    menu.get_widget("score_label").set_title(f"Score: {score}")


# Add widgets to the menu
menu.add.label("Welcome to Tetris", label_id="welcome").set_position(10, 10)
menu.add.label(f"Score: {score}", label_id="score_label")
menu.add.button("Increase Score", increase_score)
menu.add.button("Quit", pygame_menu.events.EXIT)


def draw_game_area():
    """Draw the game area on the left side of the screen."""
    # game_rect = pygame.Rect(0, 0, game_width, game_height)
    # pygame.draw.rect(screen, (50, 50, 50), game_rect)  # Game area background
    # pygame.draw.rect(screen, (255, 255, 255), game_rect, 2)  # Outline


def main():
    while True:
        screen.fill((0, 0, 0))

        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw the game area
        draw_game_area()

        # Render the menu in its area
        menu_surface = pygame.Surface((menu_width, menu_height))
        menu.update(events)
        menu.draw(menu_surface)
        screen.blit(menu_surface, (game_width, 0))

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
