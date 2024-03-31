import pymunk
from statics import width, height

def action_ball_1(ball):
    ball.mass = 1000
    ball.shape.elasticity = 0
    ball.force = (pymunk.Vec2d(width // 2, height // 2) - ball.position) * 1000