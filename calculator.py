import pygame
import sys
from button import Button
from stack import Stack


class DerivativeCalculator:
    def __init__(self, screen, back_function):
        self.screen = screen
        self.running = True
        self.current_input = ""
        self.result = ""
        self.font = pygame.font.Font(None, 74)
        self.buttons = []
        self.back_function = back_function
        self.create_buttons()

    def create_buttons(self):
        # 2D array (tuple) for button labels
        button_labels = (
            ('7', '8', '9', 'C'),
            ('4', '5', '6', 'AC'),
            ('1', '2', '3', '+'),
            ('x', 'x^2', 'x^3', '-'),
            ('0', 'x^4', 'Solve', 'Back'),
        )
        start_x, start_y = 725, 425
        button_width, button_height = 100, 100
        spacing = 20

        for row_index, row in enumerate(button_labels):
            for col_index, label in enumerate(row):
                x = start_x + col_index * (button_width + spacing)
                y = start_y + row_index * (button_height + spacing)
                self.buttons.append(Button(label, x, y, button_width, button_height))

    def handle_input(self, label):
        if label.isdigit():
            self.current_input += label
        elif label == 'C':
            self.current_input = self.current_input[:-1]
        elif label == 'AC':
            self.current_input = ""
            self.result = ""
        elif label in {'+', '-'}:
            self.current_input += label
        elif label in {'x', 'x^2', 'x^3', 'x^4'}:
            self.current_input += label
        elif label == 'Solve':
            self.result = self.solve()
        elif label == 'Back':
            self.back_function()

    def solve(self):
        if not self.current_input:
            return "ERROR"

        try:
            terms = self.convert(self.current_input)
        except ValueError:
            return "ERROR"

        # If it's just a constant, return 0
        if len(terms) == 1 and terms[0][1] == 0:
            return "0"

        # Solve the derivative using the power rule
        derivative_terms = []
        for coefficient, power in terms:
            if power > 0:
                new_coefficient = coefficient * power
                new_power = power - 1
                if new_power == 0:
                    derivative_terms.append(f"{new_coefficient}")
                elif new_power == 1:
                    derivative_terms.append(f"{new_coefficient}x")
                else:
                    derivative_terms.append(f"{new_coefficient}x^{new_power}")

        result = " + ".join(derivative_terms).replace("+ -", "- ")
        return result

    def convert(self, expression):
        stack = Stack()
        i = 0
        sign = 1

        while i < len(expression):
            if expression[i] in {'+', '-'}:
                sign = -1 if expression[i] == '-' else 1
                i += 1
            elif expression[i].isdigit():
                num = ""
                while i < len(expression) and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                if i < len(expression) and expression[i] == 'x':
                    coefficient = sign * int(num)
                    power = 1
                    i += 1
                    if i < len(expression) and expression[i] == '^':
                        i += 1
                        power_str = ""
                        while i < len(expression) and expression[i].isdigit():
                            power_str += expression[i]
                            i += 1
                        power = int(power_str)
                    stack.push((coefficient, power))
                else:
                    stack.push((sign * int(num), 0))
                sign = 1
            elif expression[i] == 'x':
                coefficient = sign
                power = 1
                i += 1
                if i < len(expression) and expression[i] == '^':
                    i += 1
                    power_str = ""
                    while i < len(expression) and expression[i].isdigit():
                        power_str += expression[i]
                        i += 1
                    power = int(power_str)
                stack.push((coefficient, power))
                sign = 1

        terms = []
        while stack.available:
            terms.insert(0, stack.pop())

        return terms

    def draw_ui(self):
        # Background
        self.screen.fill((20, 25, 92))

        # Display box for input
        pygame.draw.rect(self.screen, (255, 255, 255), (710, 225, 500, 80))
        input_surface = self.render_expression(self.current_input, (0, 0, 0))
        self.screen.blit(input_surface, (725, 240))

        # Display box for result
        pygame.draw.rect(self.screen, (255, 255, 255), (710, 325, 500, 80))
        result_surface = self.render_expression(self.result, (0, 0, 0))
        self.screen.blit(result_surface, (725, 340))

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

    def render_expression(self, expression, color):
        surface = pygame.Surface((500, 80), pygame.SRCALPHA)
        x_offset = 0

        for char in expression:
            if char == '^':
                continue
            if char in {'2', '3', '4'} and expression[x_offset - 1:x_offset] == '^':
                exponent_surface = self.font.render(char, True, color)
                surface.blit(exponent_surface, (x_offset, -20))
                x_offset += exponent_surface.get_width()
            else:
                char_surface = self.font.render(char, True, color)
                surface.blit(char_surface, (x_offset, 0))
                x_offset += char_surface.get_width()

        return surface

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_hovered():
                            self.handle_input(button.label)

            self.draw_ui()
            pygame.display.flip()
