import pygame

class Button:
    def __init__(self, label, x, y, width, height):
        self.label = label
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 50)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen):
        # Button color changes when hovered
        color = (0, 128, 255) if not self.is_hovered() else (0, 100, 200)
        pygame.draw.rect(screen, color, self.rect)

        # Adjust label rendering
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        text_rect = label_surface.get_rect(center=self.rect.center)
        screen.blit(label_surface, text_rect)
