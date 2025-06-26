import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulation (Scaffold)")

# Car properties
def draw_car(surface, x, y):
    CAR_WIDTH, CAR_HEIGHT = 60, 30
    CAR_COLOR = (200, 50, 50)
    pygame.draw.rect(surface, CAR_COLOR, (x, y, CAR_WIDTH, CAR_HEIGHT), border_radius=8)
    # Wheels
    WHEEL_COLOR = (20, 20, 20)
    pygame.draw.circle(surface, WHEEL_COLOR, (x+15, y+CAR_HEIGHT), 7)
    pygame.draw.circle(surface, WHEEL_COLOR, (x+CAR_WIDTH-15, y+CAR_HEIGHT), 7)

car_x = WIDTH // 2 - 30
car_y = HEIGHT // 2 - 15

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # Fill the screen with a dark color
    draw_car(screen, car_x, car_y)
    pygame.display.flip()

pygame.quit()
sys.exit()
