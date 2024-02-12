import pygame
from pygame.locals import QUIT
import pymunk
import pymunk.pygame_util
import random

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
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Make balls move toward the center of the stage
    for i, ball in enumerate(balls[:]):  # Copy the list to iterate safely
        if i == 0:
            action_ball_1(ball)
        elif i == 1:
            action_ball_2(ball)
        elif i == 2:
            action_ball_3(ball)

        # Calculate the distance from the center of the stage
        distance_from_center = (pymunk.Vec2d(ball.position.x - width / 2, ball.position.y - height / 2)).length

        # If the distance is greater than 250, move the ball to the top-left corner of the screen
        if distance_from_center > 250:
            ball.position = pymunk.Vec2d(20, 20)  # Move the ball to the top-left corner

        # If the distance is greater than 250, but the ball is still outside the stage, bring it back inside
        if distance_from_center > 250:
            if ball.position.x < 0 or ball.position.x > width or ball.position.y < 0 or ball.position.y > height:
                # Move the ball to a random position within the stage
                ball.position = pymunk.Vec2d(
                    width // 2 + random.uniform(-30, 30),
                    height // 2 + random.uniform(-30, 30)
                )

    # Step the physics simulation
    space.step(1 / 60.0)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the stage
    pygame.draw.circle(screen, (0, 0, 255), (width/2, height/2), 250, 2)

    # Draw the balls
    for i, ball in enumerate(balls):   # Now we iterate over the modified list
        pygame.draw.circle(screen, ball_colors[i], (int(ball.position.x), int(ball.position.y)), ball_radius)

    # Update the screen
    pygame.display.flip()

    # Control the clock
    clock.tick(60)

# Quit Pygame
pygame.quit()
