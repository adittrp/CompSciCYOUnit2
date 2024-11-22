import pygame
from queuemodule import Queue
import sys


class Flashcards:
    def __init__(self, screen, back_function):
        self.screen = screen
        self.back_function = back_function
        self.cards = {
            "Derivative": "Rate of change with respect to a certain variable.",
            "Integral": "The area under the curve of a function on a graph, the anti-derivative.",
            "Function": "A relation where each input has a single output.",
            "Limit": "The value a function approaches as the input approaches a given value.",
            "Variable": "A symbol used to represent a number in equations and expressions."
        }
        self.card_queue = Queue()
        for card in self.cards.items():
            self.card_queue.enqueue(card)
        self.current_card = None
        self.is_term_displayed = True
        self.card_number = 1
        self.total_cards = len(self.cards)
        self.show_add_popup = False
        self.new_term = ""
        self.new_definition = ""
        self.focused_box = None
        self.font = pygame.font.Font(None, 50)

    def next_card(self):
        self.card_queue.enqueue(self.card_queue.dequeue())
        self.card_number = (self.card_number % self.total_cards) + 1

    def prev_card(self):
        for i in range(self.total_cards - 1):
            self.card_queue.enqueue(self.card_queue.dequeue())
        self.card_number = (self.card_number - 2) % self.total_cards + 1

    def toggle_display(self):
        self.is_term_displayed = not self.is_term_displayed

    def add_card(self):
        if self.new_term.strip() and self.new_definition.strip():
            self.cards[self.new_term] = self.new_definition
            self.card_queue.enqueue((self.new_term, self.new_definition))
            self.total_cards += 1

        self.new_term = ""
        self.new_definition = ""
        self.focused_box = None
        self.show_add_popup = False

    def draw_ui(self):
        self.screen.fill((20, 25, 92))

        # Back button
        back_button = pygame.Rect(50, 50, 150, 100)
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, (85, 85))

        # Flashcard
        pygame.draw.rect(self.screen, (255, 255, 255), (300, 175, 1300, 700))
        card = self.card_queue.display()
        display_text = card[0] if self.is_term_displayed else card[1]
        status_text = "Term" if self.is_term_displayed else "Definition"

        # Status indicator
        status_surface = self.font.render(f"Status: {status_text}", True, (255, 255, 255))
        self.screen.blit(status_surface, (800, 100))

        # Card text
        card_surface = self.font.render(display_text, True, (0, 0, 0))
        card_rect = card_surface.get_rect(center=(960, 500))
        self.screen.blit(card_surface, card_rect)

        # Navigation arrows
        left_arrow = pygame.Rect(200, 440, 80, 80)
        right_arrow = pygame.Rect(1640, 440, 80, 80)
        pygame.draw.polygon(self.screen, (255, 255, 255), [(200, 480), (260, 440), (260, 520)])
        pygame.draw.polygon(self.screen, (255, 255, 255), [(1700, 480), (1640, 440), (1640, 520)])

        # Card number indicator
        num_surface = self.font.render(f"{self.card_number}/{self.total_cards}", True, (255, 255, 255))
        self.screen.blit(num_surface, (900, 900))

        # Add card button
        add_button = pygame.Rect(50, 950, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 255), add_button)
        add_text = self.font.render("Add Card", True, (255, 255, 255))
        self.screen.blit(add_text, (75, 960))

        return back_button, left_arrow, right_arrow, add_button

    def draw_add_popup(self):
        popup_rect = pygame.Rect(710, 225, 500, 350)
        pygame.draw.rect(self.screen, (200, 200, 200), popup_rect)

        # Term input box
        term_box = pygame.Rect(730, 250, 460, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), term_box)
        if self.focused_box == "term":
            pygame.draw.line(self.screen, (0, 0, 0), (term_box.x + 10 + self.font.size(self.new_term)[0], term_box.y + 5), (term_box.x + 10 + self.font.size(self.new_term)[0], term_box.y + 45), 2)

        term_text = self.font.render(self.new_term, True, (0, 0, 0))
        self.screen.blit(term_text, (740, 260))

        # Definition input box
        def_box = pygame.Rect(730, 325, 460, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), def_box)
        if self.focused_box == "definition":
            pygame.draw.line(self.screen, (0, 0, 0), (def_box.x + 10 + self.font.size(self.new_definition)[0], def_box.y + 5),(def_box.x + 10 + self.font.size(self.new_definition)[0], def_box.y + 45), 2)

        def_text = self.font.render(self.new_definition, True, (0, 0, 0))
        self.screen.blit(def_text, (740, 335))

        # Buttons
        add_button = pygame.Rect(730, 400, 200, 50)
        close_button = pygame.Rect(950, 400, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 255), add_button)
        pygame.draw.rect(self.screen, (255, 0, 0), close_button)

        add_text = self.font.render("Add Card", True, (255, 255, 255))
        close_text = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(add_text, (745, 410))
        self.screen.blit(close_text, (1030, 410))

        return term_box, def_box, add_button, close_button

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            if self.show_add_popup:
                term_box, def_box, add_button, close_button = self.draw_add_popup()
            else:
                back_button, left_arrow, right_arrow, add_button = self.draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_add_popup:
                        if term_box.collidepoint(mouse_pos):
                            self.focused_box = "term"
                        elif def_box.collidepoint(mouse_pos):
                            self.focused_box = "definition"
                        elif add_button.collidepoint(mouse_pos):
                            self.add_card()
                        elif close_button.collidepoint(mouse_pos):
                            self.show_add_popup = False
                    else:
                        if back_button.collidepoint(mouse_pos):
                            self.back_function()
                        elif left_arrow.collidepoint(mouse_pos):
                            self.prev_card()
                        elif right_arrow.collidepoint(mouse_pos):
                            self.next_card()
                        elif add_button.collidepoint(mouse_pos):
                            self.show_add_popup = True
                        elif pygame.Rect(300, 175, 1300, 700).collidepoint(mouse_pos):
                            self.toggle_display()
                elif event.type == pygame.KEYDOWN and self.show_add_popup and self.focused_box:
                    if event.key == pygame.K_BACKSPACE:
                        if self.focused_box == "term":
                            self.new_term = self.new_term[:-1]
                        elif self.focused_box == "definition":
                            self.new_definition = self.new_definition[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.add_card()
                    else:
                        if self.focused_box == "term":
                            self.new_term += event.unicode
                        elif self.focused_box == "definition":
                            self.new_definition += event.unicode

            pygame.display.flip()
