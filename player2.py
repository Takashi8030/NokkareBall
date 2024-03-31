import pymunk
from statics import width, height

def action_ball_2(ball):
    # ボールの質量を増やす
    ball.mass = 50  # 例として質量を50に設定
    ball.moment = 10000  # 適切なモーメント値に設定する必要があるかもしれません

    # 跳ね返り係数を減らす
    ball.shape.elasticity = 0.5  # 跳ね返り係数を減らす