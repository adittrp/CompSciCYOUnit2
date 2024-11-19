import pygame

pygame.init()

window = pygame.display.set_mode((1920, 1080))
background_color = (20, 25, 92)
pygame.display.set_caption("Math Tutor")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    window.fill(background_color)

    pygame.draw.rect(window, (210, 180, 140), (300, 100, 1340, 800))  # Light brown box
    font = pygame.font.SysFont(None, 100)
    text = font.render("Shop", True, (0, 0, 0))
    window.blit(text, (900, 150))

    pygame.display.flip()

pygame.quit()