import pygame
import sys
from calculator import DerivativeCalculator
from flashcard import Flashcards
from schedule import Schedule

pygame.init()

window_width, window_height = 1920, 1080
background_color = (95, 158, 160)
button_color = (0, 128, 255)
button_hover_color = (0, 100, 200)
text_color = (255, 255, 255)
font = pygame.font.Font(None, 74)

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Math Tutor")

flashcards = None
der_calculator = None
scheduler = None


def draw_button(surface, text, rect, is_hovered):
    pygame.draw.rect(surface, button_hover_color if is_hovered else button_color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def main_page():
    global flashcards, scheduler, der_calculator
    while True:
        window.fill(background_color)

        flashcard_btn = pygame.Rect((window_width // 2 - 350, window_height // 2 - 250), (700, 150))
        calculator_btn = pygame.Rect((window_width // 2 - 350, window_height // 2), (700, 150))
        schedule_btn = pygame.Rect((window_width // 2 - 350, window_height // 2 + 250), (700, 150))

        mouse_pos = pygame.mouse.get_pos()

        draw_button(window, "Flashcards", flashcard_btn, flashcard_btn.collidepoint(mouse_pos))
        draw_button(window, "Derivative Calculator", calculator_btn, calculator_btn.collidepoint(mouse_pos))
        draw_button(window, "Schedule", schedule_btn, schedule_btn.collidepoint(mouse_pos))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flashcard_btn.collidepoint(mouse_pos):
                    if flashcards is None:
                        flashcards = Flashcards(window, main_page)

                    flashcards.run()
                elif calculator_btn.collidepoint(mouse_pos):
                    if der_calculator is None:
                        der_calculator = DerivativeCalculator(window, main_page)

                    der_calculator.run()
                elif schedule_btn.collidepoint(mouse_pos):
                    if scheduler is None:
                        scheduler = Schedule(window, main_page)

                    scheduler.run()

        pygame.display.flip()


main_page()
