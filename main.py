import pygame
from clock import Clock

DISPLAY_SIZE = (1440, 1440)
DISPLAY_MIDDLE = (DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2)

CLOCK_RADIUS = 650

# pygame setup
pygame.init()
pygame.display.set_caption("Fantastic Clock")
screen = pygame.display.set_mode(DISPLAY_SIZE)

clock = Clock(DISPLAY_MIDDLE, CLOCK_RADIUS)
ticks = clock.get_ticks()

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", DISPLAY_MIDDLE, CLOCK_RADIUS, 10)

    # draw ticks
    for tick in ticks:
        start, end = tick.get_coords()
        pygame.draw.line(screen, "white", start, end, tick.thickness)

    # construct hand objects
    hands = clock.get_clock_hands()
    for hand in hands:
        start, end = hand.get_coords()
        pygame.draw.line(screen, "white", start, end, hand.thickness)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
