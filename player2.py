import pymunk

def action_ball_2(ball, space, stage_center, stage_radius):
    # ボールの質量を増やす
    ball.mass = 50
    ball.moment = pymunk.moment_for_circle(50, 0, 20)

    # 跳ね返り係数を減らす
    ball.shape.elasticity = 0.5

    # ステージの中心に向かう力を加える
    direction_to_center = stage_center - ball.position
    force_magnitude_to_center = 10000
    ball.apply_force_at_local_point(direction_to_center.normalized() * force_magnitude_to_center)

    # 周回させるための力を加える
    direction = stage_center - ball.position
    perpendicular_direction = pymunk.Vec2d(-direction.y, direction.x)
    # 力の大きさを調整
    force_magnitude = 1500
    # ステージの中心に対して垂直な方向に力を加える
    ball.apply_force_at_local_point(perpendicular_direction.normalized() * force_magnitude)

    # ステージの外に出そうになった場合に中心に向かう力を強くする
    distance_from_center = (ball.position - stage_center).length
    if distance_from_center > stage_radius - 50:  # ステージの端に近づいたら
        extra_force = (stage_radius - distance_from_center) * -50  # 距離に応じて力を増加
        ball.apply_force_at_local_point(direction_to_center.normalized() * extra_force)

    # ボールの速度が一定以上にならないように制限
    max_velocity = 200  # 最大速度
    if ball.velocity.length > max_velocity:
        ball.velocity = ball.velocity.normalized() * max_velocity

    # コリジョンハンドラーの設定
    def ball_collision_handler(arbiter, space, data):
        contact_point = arbiter.contact_point_set.points[0].point_a
        direction = pymunk.Vec2d(contact_point) - ball.position
        small_ball_mass = 25  # 小さなボールの質量
        small_ball_radius = 10  # 小さなボールの半径
        small_ball_moment = pymunk.moment_for_circle(small_ball_mass, 0, small_ball_radius)
        small_ball_body = pymunk.Body(small_ball_mass, small_ball_moment)
        small_ball_body.position = ball.position + direction.normalized() * (ball.shape.radius + small_ball_radius)
        small_ball_shape = pymunk.Circle(small_ball_body, small_ball_radius)
        small_ball_shape.elasticity = 0.5
        space.add(small_ball_body, small_ball_shape)
        small_ball_body.apply_impulse_at_local_point(direction.normalized() * 500)

        return True

    # コリジョンハンドラーを追加
    handler = space.add_collision_handler(2, 1)  # 2はplayer2、1はplayer1のコリジョンタイプ
    handler.begin = ball_collision_handler