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
        self.direction = [1, -1]
        self.speed = 10
        self.img = Image.open( "C:\\Coding\\github\\kyunghee\\게임프로그래밍입문\\Practice\\ball.png")
        self.img = self.img.resize((20, 20), Image.ANTIALIAS)  
        self.ball_img = ImageTk.PhotoImage(self.img)
        item = canvas.create_image(x, y, image = self.ball_img)
        super(Ball, self).__init__(canvas, item)
    
    def get_position(self):
        self.coords_xy = self.canvas.coords(self.item)
        self.coords = [self.coords_xy[0] - self.radius, self.coords_xy[1] - self.radius,\
                        self.coords_xy[0] + self.radius, self.coords_xy[1] + self.radius]
        return self.coords

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

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
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
        else:
            for x in range(5, self.width - 5, 75):
                rand_num = random.randint(0, 9)
                if (rand_num % 3 == 0):
                    pass
                else:
                    self.add_brick(x + 37.5, 50, 2)

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
            self.text = "You clear level {0}".format(self.level)
            self.draw_text(300, 200, self.text)
            self.ball.update()
            self.reset = 1
            self.canvas.delete(self.text)
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
