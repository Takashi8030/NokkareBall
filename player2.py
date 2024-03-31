import pymunk
from statics import force_max

def action_ball_2(ball, space, stage_center, stage_radius):
    # ステージの中心に向かう力を加える
    direction_to_center = stage_center - ball.position
    force_to_center = direction_to_center.normalized() * force_max
    ball.apply_force_at_local_point(force_to_center)

    # コリジョンハンドラーの設定
    def ball_collision_handler(arbiter, space, data):
        shape1, shape2 = arbiter.shapess
        ball1, ball2 = shape1.body, shape2.body

        if ball1 == ball:
            other_ball = ball2
        else:
            other_ball = ball1

        # ステージの外に押し出すための力を加える
        direction_out = (other_ball.position - stage_center).normalized()
        force_out = direction_out * force_max * 10  # 通常よりも強い力を加える
        other_ball.apply_force_at_world_point(force_out, other_ball.position)

        return True

    # コリジョンハンドラーを追加
    handler = space.add_collision_handler(2, 1)
    handler.begin = ball_collision_handler
