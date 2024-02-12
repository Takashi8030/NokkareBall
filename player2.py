import pymunk
from statics import width, height

def action_ball_2(ball):
    direction = pymunk.Vec2d(width // 2 + 100, height // 2 + 100) - ball.position
    force = 1000 * direction.normalized()
    ball.apply_force_at_local_point(force, (0, 0))