import pygame

pygame.init()

window = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Calculus Tutor")


running = True
while running:
    pygame.display.flip()