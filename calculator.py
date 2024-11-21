import pygame
import sys
from button import Button
from collections import deque

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
        if label.isdigit():  # Numbers
            self.current_input += label
        elif label == 'C':  # Backspace
            self.current_input = self.current_input[:-1]
        elif label == 'AC':  # Clear
            self.current_input = ""
            self.result = ""
        elif label in {'+', '-'}:  # Operators
            self.current_input += label
        elif label in {'x', 'x^2', 'x^3', 'x^4'}:  # Polynomial terms
            self.current_input += label
        elif label == 'Solve':  # Solve for derivative
            self.result = self.solve()
        elif label == 'Back':  # Return to main page
            self.back_function()

    def solve(self):
        """
        Solve the derivative of the polynomial represented by self.current_input.
        Returns the derivative as a string.
        """
        if not self.current_input:
            return "ERROR"  # Return an error if the input is empty

        try:
            # Tokenize the input into terms
            terms = self.tokenize(self.current_input)
        except ValueError:
            return "ERROR"  # Return an error for invalid input

        # If it's just a constant, return 0
        if len(terms) == 1 and terms[0][1] == 0:
            return "0"

        # Compute the derivative using the power rule
        derivative_terms = []
        for coeff, power in terms:
            if power > 0:  # Apply power rule: d/dx [c * x^n] = n * c * x^(n-1)
                new_coeff = coeff * power
                new_power = power - 1
                if new_power == 0:
                    derivative_terms.append(f"{new_coeff}")
                elif new_power == 1:
                    derivative_terms.append(f"{new_coeff}x")
                else:
                    derivative_terms.append(f"{new_coeff}x^{new_power}")

        # Join terms together, ensuring no redundant '+' or '-' signs
        result = " + ".join(derivative_terms).replace("+ -", "- ")
        return result

    def tokenize(self, expression):
        """
        Parse a polynomial input string into a list of (coefficient, power) tuples.
        Handles positive and negative terms, proper placement of coefficients,
        and ensures valid syntax.
        """
        stack = deque()
        i = 0
        sign = 1
        last_was_operator = True

        while i < len(expression):
            if expression[i] in {'+', '-'}:
                sign = -1 if expression[i] == '-' else 1
                last_was_operator = True
                i += 1
            elif expression[i].isdigit():
                num = ""
                while i < len(expression) and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                if i < len(expression) and expression[i] == 'x':  # If followed by 'x'
                    coeff = sign * int(num)  # Use the parsed number as coefficient
                    power = 1  # Default power for 'x' is 1
                    i += 1  # Skip 'x'
                    if i < len(expression) and expression[i] == '^':  # Handle powers
                        i += 1  # Skip '^'
                        power_str = ""
                        while i < len(expression) and expression[i].isdigit():
                            power_str += expression[i]
                            i += 1
                        power = int(power_str)
                    stack.append((coeff, power))
                else:  # If not followed by 'x', it's a constant
                    stack.append((sign * int(num), 0))
                sign = 1
                last_was_operator = False
            elif expression[i] == 'x':
                coeff = sign  # Default coefficient is 1 (or -1 based on sign)
                power = 1
                i += 1
                if i < len(expression) and expression[i] == '^':  # Handle powers
                    i += 1  # Skip '^'
                    power_str = ""
                    while i < len(expression) and expression[i].isdigit():
                        power_str += expression[i]
                        i += 1
                    power = int(power_str)
                stack.append((coeff, power))
                sign = 1
                last_was_operator = False
            else:
                raise ValueError(f"Invalid character in expression: {expression[i]}")

        return list(stack)

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
        """Render an expression with raised exponents."""
        surface = pygame.Surface((500, 80), pygame.SRCALPHA)
        x_offset = 0
        for char in expression:
            if char == '^':  # Render exponent slightly raised
                continue
            if char in {'2', '3', '4'} and expression[x_offset - 1:x_offset] == '^':
                exponent_surface = self.font.render(char, True, color)
                surface.blit(exponent_surface, (x_offset, -20))  # Raise exponent
                x_offset += exponent_surface.get_width()
            else:
                char_surface = self.font.render(char, True, color)
                surface.blit(char_surface, (x_offset, 0))
                x_offset += char_surface.get_width()
        return surface

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_hovered():
                            self.handle_input(button.label)

            self.draw_ui()
            pygame.display.flip()
