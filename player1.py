import pymunk
from statics import width, height

def action_ball_1(ball, space, stage_center, stage_radius):
    ball.mass = 9999999
    ball.shape.elasticity = 0
    ball.force = (pymunk.Vec2d(width // 2, height // 2) - ball.position) * 999999999
    ball.velocity = (pymunk.Vec2d(width // 2, height // 2) - ball.position) * 99