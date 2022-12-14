from asyncio.windows_events import NULL
from cmath import pi
import math
import random
import tkinter as tk
from PIL import ImageTk, Image

class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)   

class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [0.707, 0.707]
        self.speed = 10
        self.img = Image.open("C:\\KyungHee\\kyunghee\\게임프로그래밍입문\\Practice\\ball.png")
        self.img = self.img.resize((20, 20), Image.ANTIALIAS)  
        self.ball_img = ImageTk.PhotoImage(self.img)
        item = canvas.create_image(x, y, image = self.ball_img)
        super(Ball, self).__init__(canvas, item)
    
    def get_position(self):
        self.coords_xy = self.canvas.coords(self.item)
        self.coords = [self.coords_xy[0] - self.radius, self.coords_xy[1] - self.radius,\
                        self.coords_xy[0] + self.radius, self.coords_xy[1] + self.radius]
        return self.coords

    def get_position_center(self):
        self.coords_xy = self.canvas.coords(self.item)
        return self.coords_xy

    def update(self):
        self.speed = 10
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    # 근의 공식 값 출력
    def solution(self, b, c, range_one, range_two):
        D = (b**2) - (4*c)
        if D>0:
            r1= (-b + (b**2-4*c)**0.5)/(2)
            r2 = (-b - (b**2-4*c)**0.5)/(2)
            # 값이 출동 되는 위치에 있는 지 여부를 확인하고 return 값을 전달해줌
            if (r1 >= range_one and r1 <= range_two):
                return r1
            else:
                return r2
        elif D==0:
            x = -b / 2
            return x
        else:
            pass

    # 충돌을 어디에서 발생했는지 리턴하는 함수
    def collide_where(self, rectangle, circle):
        rectangle_xy = rectangle
        
        # 충돌 처리 영역을 확장하면 충돌 처리 직선을 바깥으로 그리고 그것이 기준이 된 것 같이 됨
        rectangle_xy[0] -= 0.5
        rectangle_xy[1] -= 0.5
        rectangle_xy[2] += 0.5
        rectangle_xy[3] += 0.5
        
        # 원의 x좌표와 y좌표를 구한다.
        circle_x = circle[0]
        circle_y = circle[1]
        
        # 구분이 되는 x와 y값을 구한다.
        check_x = (rectangle_xy[0] + rectangle_xy[2])/2
        check_y = (rectangle_xy[1] + rectangle_xy[3])/2
        find_x = None
        find_y = None
        
        # 기준에 따라 충돌된 x좌표와 y좌표를 구할 수 있다.
        if (circle_y > check_y):
            find_x = self.solution(-2*circle_x, circle_x**2-100+(rectangle_xy[3]-circle_y)**2, rectangle_xy[0], rectangle_xy[2])
            and_y = rectangle_xy[3]
        else:
            find_x = self.solution(-2*circle_x, circle_x**2-100+(rectangle_xy[1]-circle_y)**2, rectangle_xy[0], rectangle_xy[2])
            and_y = rectangle_xy[1]
        if (circle_x < check_x):
            find_y = self.solution(-2*circle_y, circle_y**2-100+(rectangle_xy[0]-circle_x)**2, rectangle_xy[1], rectangle_xy[3])
            and_x = rectangle_xy[0]
        else:
            find_y = self.solution(-2*circle_y, circle_y**2-100+(rectangle_xy[2]-circle_x)**2, rectangle_xy[1], rectangle_xy[3])
            and_x = rectangle_xy[2]
        
        # 만약 모서리 충돌이 발생했다면 if문 아래로 들어간다.
        if (find_x != None and find_y != None):
            coords = [find_x, and_y, and_x, find_y]
            return coords
        else:
            return NULL

    def check_90degree(self, x, y):
        degree = math.acos(x*self.direction[1]+y*self.direction[0]) * (180/3.14)
        print(degree)
        if (degree > 90):
            return True
        else:
            return False


    def cal_reflection(self, meet):
        # x축과 교점의 좌표
        x1 = meet[0]
        y1 = meet[1]
        # y축과 교점의 좌표
        x2 = meet[2]
        y2 = meet[3]

        # 백터의 방향 설정
        abs1 = 1
        abs2 = 1
        # 충돌하는 위치에 따라 생성되는 법선 백터의 값은 동일함
        if (x1 > x2 and y1 > y2):
            abs1 *= -1
        elif (x1 > x2 and y1 < y2):
            abs1 *= -1
            abs2 *= -1
        elif (x1 < x2 and y1 < y2):
            abs2 *= -1
        
        # 법선 백터
        N_vector_x = abs1*abs(y1 - y2)
        N_vector_y = abs2*abs(x1 - x2)

        # 법선 백터를 단위 백터로 치환
        new_length = ((N_vector_x)**2 + (N_vector_y)**2)**(0.5)
        N_vector_x = N_vector_x/new_length
        N_vector_y = N_vector_y/new_length
        
        if (self.check_90degree(N_vector_x, N_vector_y)):
            # 반사 백터 구하기
            vec_X_reflection = self.direction[0] + N_vector_x
            vec_Y_reflection = self.direction[1] + N_vector_y
            
            R_length = ((vec_X_reflection)**2 + (vec_Y_reflection)**2)**(0.5)
            vec_X_reflection = vec_X_reflection/R_length
            vec_Y_reflection = vec_Y_reflection/R_length
            
            self.direction[0] = vec_X_reflection
            self.direction[1] = vec_Y_reflection
        
    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            
            # 사각형의 꼭짓점 위치
            coords = game_object.get_position()
            # 원의 중심 좌표 구하기
            ball_center = self.get_position_center()
            meet = self.collide_where(coords, ball_center)
            # 모서리 충돌이 발생함.
            if (meet):
                self.cal_reflection(meet)
            # 모서리 충돌이 발생하지 않음.
            else:
                if x > coords[2]:
                    self.direction[0] *= 1
                elif x < coords[0]:
                    self.direction[0] *= -1
                else:
                    self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()


class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2,
                                        x + self.width / 2, y + self.height / 2,
                                        fill='blue')
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)


class Brick(GameObject):
    COLORS = {1: '#999999', 2: '#555555', 3: '#222222'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width / 2, y - self.height / 2,
                                        x + self.width / 2, y + self.height / 2,
                                        fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.level = 0
        self.reset = 1
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#aaaaff', width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle

        self.hud = None
        self.setup_game(self.level, self.reset)
        self.canvas.focus_set()
        self.canvas.bind('<Left>',lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',lambda _: self.paddle.move(10))

    def make_brick(self, level):
        if (level == 0):
            for x in range(5, self.width - 5, 75):
                rand_num = random.randint(0, 9)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 50, 1)
        elif (level == 1):
            for x in range(5, self.width - 5, 75):
                rand_num = random.randint(0, 9)
                if (rand_num % 4 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 50, 1)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 70, 1)
        elif (level == 2):
            for x in range(5, self.width - 5, 75):
                rand_num = random.randint(0, 9)
                if (rand_num % 4 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 50, 2)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 70, 2)
        elif (level == 3):
            for x in range(5, self.width - 5, 75):
                rand_num = random.randint(0, 9)
                if (rand_num % 4 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 50, 3)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 70, 2)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 90, 1)
        elif (level == 4):
            for x in range(5, self.width - 5, 75):
                rand_num = random.randint(0, 9)
                if (rand_num % 4 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 50, 3)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 70, 2)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 90, 2)
        elif (level == 5):
            for x in range(5, self.width - 5, 75):
                rand_num = random.randint(0, 9)
                if (rand_num % 4 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 50, 3)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 70, 3)
                if (rand_num % 2 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 90, 3)

    def setup_game(self, level, reset):
        self.add_ball()
        if (reset == 1):
            self.make_brick(level)
        self.update_lives_text()
        self.text = self.draw_text(300, 200, 'Press Space to start')
        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)

    def update_lives_text(self):
        text = "Lives: %s Level : %s" % (self.lives, self.level)
        if self.hud is None:
            self.hud = self.draw_text(80, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0: 
            self.level += 1
            self.ball.speed = None
            # 코드 수정부
            self.ball.update()
            self.reset = 1
            self.after(1000, self.setup_game(self.level, self.reset))
        
        elif self.ball.get_position()[3] >= self.height: 
            self.ball.speed = None
            self.reset = 0
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'Game Over')
            else:
                self.after(1000, self.setup_game(self.level, self.reset))
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello, Pong!')
    game = Game(root)
    game.mainloop()
