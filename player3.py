import pymunk

def action_ball_3(ball, space, stage_center, stage_radius):
    # ステージの中心に向かう力を加える（常に適用）
    direction_to_center = stage_center - ball.position
    force_magnitude_to_center = 1000
    ball.apply_force_at_local_point(direction_to_center.normalized() * force_magnitude_to_center)

    # コリジョンハンドラーの設定
    def ball_collision_handler(arbiter, space, data):
        other_ball = arbiter.shapes[1].body
        # 相手のボールをステージの外に押し出す力を加える
        direction_outside = other_ball.position - stage_center
        force_magnitude_outside = 5000
        other_ball.apply_force_at_local_point(direction_outside.normalized() * force_magnitude_outside)
        return True

    # コリジョンハンドラーを追加
    handler = space.add_collision_handler(3, 1)  # 例: 3はplayer3、1はplayer1のコリジョンタイプ
    handler.begin = ball_collision_handler
    handler = space.add_collision_handler(3, 2)  # 例: 2はplayer2のコリジョンタイプ
    handler.begin = ball_collision_handler

    # ステージの外に出ないようにする
    distance_from_center = (ball.position - stage_center).length
    if distance_from_center > stage_radius:
        # ステージの中心に向かう力を強くする
        force_magnitude_to_center *= 2
        ball.apply_force_at_local_point(direction_to_center.normalized() * force_magnitude_to_center)