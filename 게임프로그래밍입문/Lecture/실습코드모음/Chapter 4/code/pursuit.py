import cocos
import cocos.euclid as eu
import cocos.particle_systems as ps


def truncate(vector, m):
    magnitude = abs(vector)
    if magnitude > m:
        vector *= m / magnitude
    return vector


class Actor(cocos.cocosnode.CocosNode):
    def __init__(self, x, y):
        super(Actor, self).__init__()
        self.position = (x, y)
        self.velocity = eu.Vector2(0, 0)
        self.speed = 2
        self.max_force = 5
        self.max_velocity = 200
        self.target = None
        self.add(ps.Sun())
        self.schedule(self.update)

    def update(self, dt):
        if self.target is None:
            return
        # 타겟의 위치를 pos에 넣는다.
        pos = self.target.position
        # 현재의 위치에 속도를 더한 값이 미래의 위치이다.
        future_pos = pos + self.target.velocity * 1
        # 거리 또한 미래의 위치에 현재의 
        distance = future_pos - eu.Vector2(self.x, self.y)
        # 거리와 속도를 곱하고 현재 속도와의 차이만큼 이동한다.
        print(self.velocity)
        steering = distance * self.speed - self.velocity
        # 힘의 최대값만큼만 움직임의 속도를 제한한다. 
        # -> 이것은 현재의 속도와 합이 같은 비율로 들어가기 위해서 같은 비율로 맞춰준다.
        steering = truncate(steering, self.max_force)
        # steering 속력과 현재의 속력을 합해서 절대값을 취한다. 이것이 우리가 구하고자 하는 속력이다.
        self.velocity = truncate(self.velocity + steering, self.max_velocity)
        self.position += self.velocity * dt


class MainLayer(cocos.layer.Layer):
    def __init__(self):
        super(MainLayer, self).__init__()
        self.target = ps.Sun()
        self.target.position = (40, 40)
        self.target.start_color = ps.Color(0.2, 0.7, 0.7, 1.0)
        self.target.velocity = eu.Vector2(50, 0)
        self.add(self.target)
        self.actor = Actor(320, 240)
        self.actor.target = self.target
        self.add(self.actor)
        self.schedule(self.update)

    def update(self, dt):
        self.target.position += self.target.velocity * dt


if __name__ == '__main__':
    cocos.director.director.init(caption='Steering Behaviors')
    scene = cocos.scene.Scene(MainLayer())
    cocos.director.director.run(scene)
