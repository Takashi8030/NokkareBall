import pygame
from pygame.locals import QUIT
import pymunk
import pymunk.pygame_util
import random
import time

from statics import width, height
from player1 import action_ball_1
from player2 import action_ball_2
from player3 import action_ball_3

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Balls Simulation")

# Create a Pymunk space
space = pymunk.Space()
space.gravity = (0, 0)  # Disable gravity

# Create balls
num_balls = 3
balls = []
ball_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Set colors for the balls

for _ in range(num_balls):
    ball_mass = 10
    ball_radius = 20
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    
    # Ensure each ball has a unique initial position
    ball_initial_position = pymunk.Vec2d(
        width // 2 + random.uniform(-30, 30),
        height // 2 + random.uniform(-30, 30)
    )
    
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = ball_initial_position
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.95
    space.add(ball_body, ball_shape)
    balls.append(ball_body)

# Create Pygame clock
clock = pygame.time.Clock()

# Collision handler for balls and stage
def ball_stage_collision(arbiter, space, data):
    # Do nothing to prevent collisions with the stage
    return True

# Set up collision handler
space.add_collision_handler(0, 1).begin = ball_stage_collision

# Main loop
selected_ball = None
game_start_effect = time.time()
running = True
while True:
    # Clear the screen
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if (ball.position - pymunk.Vec2d(*event.pos)).length < ball_radius:
                    selected_ball = ball
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_ball = None
        elif event.type == pygame.MOUSEMOTION:
            if selected_ball is not None:
                selected_ball.position = pymunk.Vec2d(*event.pos)
    
    if game_start_effect:
        countdown = max(0, 3 - (time.time() - game_start_effect))
        if countdown == 0:
            game_start_effect = None
        else:
            font = pygame.font.Font(None, 74)
            text = font.render(str(int(countdown) + 1), True, (255, 0, 0))
            text_rect = text.get_rect(center=(width / 2, height / 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            continue

    # Make balls move toward the center of the stage
    for i, ball in enumerate(balls):
        if i == 0:
            action_ball_1(ball)
        elif i == 1:
            action_ball_2(ball)
        elif i == 2:
            action_ball_3(ball)

    # Step the physics simulation
    space.step(1 / 60.0)

    # Draw the stage
    pygame.draw.circle(screen, (0, 0, 255), (width/2, height/2), 250, 2)

    # Draw the balls
    for i, ball in enumerate(balls):
        pygame.draw.circle(screen, ball_colors[i], (int(ball.position.x), int(ball.position.y)), ball_radius)

    # Update the screen
    pygame.display.flip()

    # Control the clock
    clock.tick(60)

    if not running:
        break

# Quit Pygame
pygame.quit()