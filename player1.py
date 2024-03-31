import pymunk
from statics import width, height, mass_max, force_max, elasticity_min, velocity_max

def action_ball_1(ball, space, stage_center, stage_radius):
    ball.mass = mass_max
    ball.shape.elasticity = elasticity_min
    ball.force = (pymunk.Vec2d(width // 2, height // 2) - ball.position) * force_max
    ball.velocity = (pymunk.Vec2d(width // 2, height // 2) - ball.position) * velocity_max