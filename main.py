import pygame
import sys
from calculator import DerivativeCalculator

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
BACKGROUND_COLOR = (20, 25, 92)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 100, 200)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 74)

# Screen setup
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Math Tutor")


# Helper function to draw buttons
def draw_button(surface, text, rect, is_hovered):
    pygame.draw.rect(surface, BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR, rect)
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def main_page():
    while True:
        window.fill(BACKGROUND_COLOR)

        # Button rect
        calculator_btn = pygame.Rect((WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50), (400, 100))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons
        draw_button(window, "Calculator", calculator_btn, calculator_btn.collidepoint(mouse_pos))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and calculator_btn.collidepoint(mouse_pos):
                DerivativeCalculator(window, main_page).run()

        pygame.display.flip()


# Run the main page
main_page()
