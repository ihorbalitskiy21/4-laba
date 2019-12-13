from tkinter import *
from tkinter import messagebox
import os
import socket
import json
import random

try:
    os.remove('close.txt')
except:
    print('Already cleared')

#OBJECTS-------------------------

class screen_obj():
    def __init__(self):
        self.width = 1250
        self.height = 500
        self.left_edge = 20
        self.right_edge = self.width - self.left_edge
        self.theme = 0
        self.game = 0
screen = screen_obj()

class screen_obj2():
    def __init__(self):
        self.width = 1000
        self.height = 500
        self.left_edge = 20
        self.right_edge = self.width - self.left_edge
screen2 = screen_obj2()


class network_obj():
    def __init__(self):
        self.player = 0
        self.name = 'Noname'
        self.host = 'NoHost'
        self.port = 0
        self.side = 'NoSide'
        self.ball = 0
        self.start = 0
        self.top = 0
        self.bot = 0
network = network_obj()

class ball_obj():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 45
        self.speed_init = 15
        self.speed_x = self.speed_init
        self.speed_y = self.speed_init
        self.speed_up = 1.05
        self.speed_max = 40
        self.change_x = 20
        self.change_y = 0
ball = ball_obj()

class player_obj():
    def __init__(self):
        self.name = 'Noname'
        self.score = 0
        self.width = 20
        self.height = 100
        self.speed_init = 15
        self.speed = 0
player1 = player_obj()
player2 = player_obj()

#OBJECTS-------------------------



#GAME 1PC-------------------------

def start_onepc():

    if screen.theme == 1:
        theme_background = '#1c1b29'
        theme_ball = '#797979'
        theme_racket = '#772'
        theme_text = 'white'
    elif screen.theme == 2:
        theme_background = '#bababa'
        theme_ball = '#d0d0d0'
        theme_racket = '#7b7b7b'
        theme_text = 'black'



    def update_score(player):
        if player == '1':
            player1.score += 1
            c.itemconfig(player1_score, text=player1.score)
        elif player == '2':
            player2.score += 1
            c.itemconfig(player2_score, text=player2.score)

    def spawn():
        c.coords(ball_f, screen2.width/2-ball.radius/2, screen2.height/2-ball.radius/2, screen2.width/2+ball.radius/2, screen2.height/2+ball.radius/2)
        ball.speed_x = -(ball.speed_x * -ball.speed_init) / abs(ball.speed_x)

    def spring(act):
        if act == "hit":
            ball.speed_y = random.randrange(-15, 15)
            if abs(ball.speed_x) < ball.speed_max:
                ball.speed_x *= -ball.speed_up
            else:
                ball.speed_x = -ball.speed_x
        else:
            ball.speed_y = -ball.speed_y

    onecgamescr = Tk()
    onecgamescr.title('Game')
    c = Canvas(onecgamescr, width=screen.width, height=screen.height, background=theme_background)
    c.pack()

    left_racket = c.create_line(screen.left_edge / 2,
                                screen.height / 2 + player1.height / 2,
                                screen.left_edge / 2,
                                screen.height / 2 - player1.height / 2,
                                width=player1.width,
                                fill=theme_racket)
    right_racket = c.create_line(screen.width - screen.left_edge / 2,
                                 screen.height / 2 + player2.height / 2,
                                 screen.width - screen.left_edge / 2,
                                 screen.height / 2 - player2.height / 2,
                                 width=player2.width,
                                 fill=theme_racket)

    ball_f = c.create_oval(screen.width / 2 - ball.radius / 2,
                           screen.height / 2 - ball.radius / 2,
                           screen.width / 2 + ball.radius / 2,
                           screen.height / 2 + ball.radius / 2,
                           fill=theme_ball)

    player1_score = c.create_text(screen.width / 6, 475, text=player1.score, font=('Verdana', 18), fill=theme_text)
    player2_score = c.create_text(screen.width - screen.width / 6, 475, text=player2.score, font=('Verdana', 18),
                                  fill=theme_text)
    player1_name = c.create_text(screen.width / 6, 25, text=player1.name, font=('Verdana', 15), fill=theme_text)
    player2_name = c.create_text(screen.width - screen.width / 6, 25, text=player2.name, font=('Verdana', 15),
                                 fill=theme_text)

    def move():
        ball_left, ball_top, ball_right, ball_bottom = c.coords(ball_f)
        ball_center = (ball_top + ball_bottom) / 2
        if ball_right + ball.speed_x < screen.right_edge and ball_left + ball.speed_x > screen.left_edge:
            c.move(ball_f, ball.speed_x, ball.speed_y)
        elif ball_right == screen.right_edge or ball_left == screen.left_edge:
            if ball_right > screen.width / 2:
                if c.coords(right_racket)[3] < ball_center < c.coords(right_racket)[1]:
                    spring("hit")
                else:
                    update_score('1')
                    spawn()
            else:
                if c.coords(left_racket)[3] < ball_center < c.coords(left_racket)[1]:
                    spring("hit")
                else:
                    update_score('2')
                    spawn()
        else:
            if ball_right > screen.width / 2:
                c.move(ball_f, screen.right_edge - ball_right, ball.speed_y)
            else:
                c.move(ball_f, -ball_left + screen.left_edge, ball.speed_y)
        if ball_top + ball.speed_y < 0 or ball_bottom + ball.speed_y > screen.height:
            spring("other")

    def rackets_move():
        rackets_obj = {left_racket: player1.speed, right_racket: player2.speed}
        for racket in rackets_obj:
            c.move(racket, 0, rackets_obj[racket])
            if c.coords(racket)[3] < 0:
                c.move(racket, 0, -c.coords(racket)[3])
            elif c.coords(racket)[1] > screen.height:
                c.move(racket, 0, screen.height - c.coords(racket)[1])


    def prestart():
        if screen.game == 0:
            main_function()
            screen.game = 1

    def main_function():
        move()
        rackets_move()
        onecgamescr.after(31, main_function)

    c.focus_set()

    def keys_down(event):
        if event.keycode == 87:
            player1.speed = -player1.speed_init
        elif event.keycode == 83:
            player1.speed = player1.speed_init
        elif event.keycode == 38:
            player2.speed = -player2.speed_init
        elif event.keycode == 40:
            player2.speed = player2.speed_init
        elif event.keycode == 32:
            prestart()
    c.bind("<KeyPress>", keys_down)

    def keys_up(event):
        if event.keycode == 87 or event.keycode == 83:
            player1.speed = 0
        elif event.keycode == 38 or event.keycode == 40:
            player2.speed = 0
    c.bind("<KeyRelease>", keys_up)

#GAME 1PC-------------------------
#----------------------------------------------------
#GAME 2PC-------------------------

def start_twopc_left():

    if screen.theme == 1:
        theme_background = '#1c1b29'
        theme_ball = '#797979'
        theme_racket = '#4b4d5c'
        theme_text = 'white'
    elif screen.theme == 2:
        theme_background = '#bababa'
        theme_ball = '#d0d0d0'
        theme_racket = '#7b7b7b'
        theme_text = 'black'

    def update_score():
        player2.score += 1
        c.itemconfig(player2_score, text=player2.score)
        sock = socket.socket()
        sock.connect((network.host, int(network.port)))
        data = {"title": "goal"}
        sock.send(json.dumps(data).encode('utf-8'))
        sock.close()
        network.ball = 0

    def spawn():
        c.coords(ball_f, screen2.width/2-ball.radius/2, screen2.height/2-ball.radius/2, screen2.width/2+ball.radius/2, screen2.height/2+ball.radius/2)
        ball.speed_x = 15

    def spring(act):
        if act == "hit":
            if ball.speed_y < 0:
                ball.speed_y = (-15)
            elif ball.speed_y > 0:
                ball.speed_y = 15
            ball.speed_x = -ball.speed_x
        else:
            ball.speed_y = -ball.speed_y

    game_window = Tk()
    game_window.title('Game')
    c = Canvas(game_window, width=screen2.width, height=screen.height, background=theme_background)
    c.pack()

    left_racket = c.create_line(screen2.left_edge / 2,
                                screen2.height / 2 + player1.height / 2,
                                screen2.left_edge / 2,
                                screen2.height / 2 - player1.height / 2,
                                width=player1.width,
                                fill=theme_racket)

    player1_score = c.create_text(screen2.width / 6, 475, text=player1.score, font=('Verdana', 18), fill=theme_text)
    player2_score = c.create_text(screen2.width - screen2.width / 6, 475, text=player2.score, font=('Verdana', 18),
                                  fill=theme_text)
    player1_name = c.create_text(screen2.width / 6, 25, text=network.name, font=('Verdana', 15), fill=theme_text)
    player2_name = c.create_text(screen2.width - screen2.width / 6, 25, text='Not connected', font=('Verdana', 15),
                                 fill=theme_text)

    ball_f = c.create_oval(screen2.width / 2 - ball.radius / 2,
                           screen2.height / 2 - ball.radius / 2,
                           screen2.width / 2 + ball.radius / 2,
                           screen2.height / 2 + ball.radius / 2,
                           fill=theme_ball)

    def move():
        ball_left, ball_top, ball_right, ball_bottom = c.coords(ball_f)
        ball_center = (ball_top + ball_bottom) / 2
        if ball_right + ball.speed_x < screen2.right_edge and ball_left + ball.speed_x > screen2.left_edge:
            c.move(ball_f, ball.speed_x, ball.speed_y)
        elif ball_left == screen2.left_edge:
            if c.coords(left_racket)[3] < ball_center < c.coords(left_racket)[1]:
                spring("hit")
            else:
                update_score()
        elif screen2.right_edge < ball_right:
            sock = socket.socket()
            sock.connect((network.host, int(network.port)))
            data = {"title": "coords",
                    "top": ball_top,
                    "bottom": ball_bottom,
                    "speed_y": ball.speed_y,
                    "speed_x": ball.speed_x
            }
            sock.send(json.dumps(data).encode('utf-8'))
            sock.close()
            network.ball = 0
            c.coords(ball_f, 1320, 0, 1350, 30)
        elif 1300 < ball_right:
            print('wait')
        else:
            if ball_right > screen.width / 2:
                c.move(ball_f, screen.right_edge - ball_right, ball.speed_y)
            else:
                c.move(ball_f, -ball_left + screen.left_edge, ball.speed_y)
        if ball_top + ball.speed_y < 0 or ball_bottom + ball.speed_y > screen2.height:
            spring("other")

    def rackets_move():
        rackets_obj = {left_racket: player1.speed}
        for racket in rackets_obj:
            c.move(racket, 0, rackets_obj[racket])
            if c.coords(racket)[3] < 0:
                c.move(racket, 0, -c.coords(racket)[3])
            elif c.coords(racket)[1] > screen.height:
                c.move(racket, 0, screen.height - c.coords(racket)[1])

    def ready():
        listdir = os.listdir()
        if 'this_comp_ready.txt' in listdir and 'other_comp_ready.txt' in listdir:
            with open('name.txt', 'r') as file:
                other_player = file.read()
            c.itemconfig(player2_name, text=other_player)
            network.ball = 1
            main_function()
        else:
            print("Don't ready")
            game_window.after(100, ready)

    def check():
        listdir = os.listdir()
        if 'spawn.txt' in listdir:
            with open('top.txt', 'r') as file:
                top = file.read()
                network.top = float(top)
            with open('bot.txt', 'r') as file:
                bot = file.read()
                network.bot = float(bot)
            with open('y.txt', 'r') as file:
                sp = file.read()
                ball.speed_y = int(sp)
            with open('x.txt', 'r') as file:
                spe = file.read()
                ball.speed_x = float(spe)
            c.coords(ball_f, 935, network.top, 970, network.bot)
            network.ball = 1
            os.remove('spawn.txt')
            os.remove('top.txt')
            os.remove('bot.txt')
            os.remove('y.txt')
            os.remove('x.txt')
        if 'goal.txt' in listdir:
            player1.score += 1
            c.itemconfig(player1_score, text=player1.score)
            spawn()
            network.ball = 1
            os.remove('goal.txt')

    def finish():
        messagebox.showinfo('Congratulations', 'Opponent left the game\nCongratulations, you won')
        game_window.destroy()
        os.remove('close.txt')

    def main_function():
        if network.ball == 0:
            check()
        elif network.ball == 1:
            move()
        rackets_move()
        listdir = os.listdir()
        if 'close.txt' in listdir:
            finish()
        game_window.after(30, main_function)

    c.focus_set()

    def keys_down(event):
        if event.keycode == 38:
            player1.speed = -player1.speed_init
        elif event.keycode == 40:
            player1.speed = player1.speed_init
        elif event.keycode == 32:
            if network.start == 0:
                with open('this_comp_ready.txt', 'w') as file:
                    file.write(' ')
                sock = socket.socket()
                sock.connect((network.host, int(network.port)))
                data = {"title": "ready"}
                sock.send(json.dumps(data).encode('utf-8'))
                sock.close()
                network.start = 1
            else:
                print('You are ready already')
    c.bind("<KeyPress>", keys_down)

    def keys_up(event):
        if event.keycode == 38 or event.keycode == 40:
            player1.speed = 0
            sock = socket.socket()
            sock.connect((network.host, int(network.port)))
            data = {"title": "speed",
                    'act': 'stop'
                    }
            sock.send(json.dumps(data).encode('utf-8'))
            sock.close()
    c.bind("<KeyRelease>", keys_up)
    ready()
#----------------------------------------------------

def start_twopc_right():

    if screen.theme == 1:
        theme_background = '#1c1b29'
        theme_ball = '#797979'
        theme_racket = '#4b4d5c'
        theme_text = 'white'
    elif screen.theme == 2:
        theme_background = '#bababa'
        theme_ball = '#d0d0d0'
        theme_racket = '#7b7b7b'
        theme_text = 'black'

    def update_score():
        player1.score += 1
        c.itemconfig(player1_score, text=player1.score)
        sock = socket.socket()
        sock.connect((network.host, int(network.port)))
        data = {"title": "goal"}
        sock.send(json.dumps(data).encode('utf-8'))
        sock.close()
        network.ball = 0

    def spawn():
        c.coords(ball_f, screen2.width/2-ball.radius/2, screen2.height/2-ball.radius/2, screen2.width/2+ball.radius/2, screen2.height/2+ball.radius/2)
        ball.speed_x = -15

    def spring(act):
        if act == "hit":
            if ball.speed_y < 0:
                ball.speed_y = (-15)
            elif ball.speed_y > 0:
                ball.speed_y = 15
            ball.speed_x = -ball.speed_x
        else:
            ball.speed_y = -ball.speed_y

    game_window = Tk()
    game_window.title('Game')
    c = Canvas(game_window, width=screen2.width, height=screen.height, background=theme_background)
    c.pack()

    right_racket = c.create_line(screen2.width - screen2.left_edge / 2,
                                 screen2.height / 2 + player2.height / 2,
                                 screen2.width - screen2.left_edge / 2,
                                 screen2.height / 2 - player2.height / 2,
                                 width=player2.width,
                                 fill=theme_racket)

    player1_score = c.create_text(screen2.width / 6, 475, text=player1.score, font=('Verdana', 18), fill=theme_text)
    player2_score = c.create_text(screen2.width - screen2.width / 6, 475, text=player2.score, font=('Verdana', 18),
                                  fill=theme_text)
    player1_name = c.create_text(screen2.width / 6, 25, text='Not connected', font=('Verdana', 15), fill=theme_text)
    player2_name = c.create_text(screen2.width - screen2.width / 6, 25, text=network.name, font=('Verdana', 15),
                                 fill=theme_text)

    ball_f = c.create_oval(1300, 0, 1335, 35, fill=theme_ball)

    def move():
        ball_left, ball_top, ball_right, ball_bottom = c.coords(ball_f)
        ball_center = (ball_top + ball_bottom) / 2
        if ball_right + ball.speed_x < screen2.right_edge and ball_left + ball.speed_x > screen2.left_edge:
            c.move(ball_f, ball.speed_x, ball.speed_y)
        elif ball_right == screen2.right_edge or ball_right + 10 == screen2.right_edge:
            if c.coords(right_racket)[3] < ball_center < c.coords(right_racket)[1]:
                spring("hit")
            else:
                update_score()
        elif ball_left < 30:
            sock = socket.socket()
            sock.connect((network.host, int(network.port)))
            data = {"title": "coords",
                    "top": ball_top,
                    "bottom": ball_bottom,
                    "speed_y": ball.speed_y,
                    "speed_x": ball.speed_x
            }
            sock.send(json.dumps(data).encode('utf-8'))
            sock.close()
            network.ball = 0
            c.coords(ball_f, 1330, 1, 1360, 30)
        elif 1300 < ball_right:
            print('wait')
        else:
            if ball_right > screen.width / 2:
                c.move(ball_f, screen.right_edge - ball_right, ball.speed_y)
            else:
                c.move(ball_f, -ball_left + screen.left_edge, ball.speed_y)
        if ball_top + ball.speed_y < 0 or ball_bottom + ball.speed_y > screen2.height:
            spring("other")

    def rackets_move():
        rackets_obj = {right_racket: player1.speed}
        for racket in rackets_obj:
            c.move(racket, 0, rackets_obj[racket])
            if c.coords(racket)[3] < 0:
                c.move(racket, 0, -c.coords(racket)[3])
            elif c.coords(racket)[1] > screen.height:
                c.move(racket, 0, screen.height - c.coords(racket)[1])

    def ready():
        listdir = os.listdir()
        if 'this_comp_ready.txt' in listdir and 'other_comp_ready.txt' in listdir:
            with open('name.txt', 'r') as file:
                other_player = file.read()
            c.itemconfig(player1_name, text=other_player)
            network.ball = 0
            main_function()
        else:
            print("Don't ready")
            game_window.after(100, ready)

    def check():
        listdir = os.listdir()
        if 'spawn.txt' in listdir:
            with open('top.txt', 'r') as file:
                top = file.read()
                network.top = float(top)
            with open('bot.txt', 'r') as file:
                bot = file.read()
                network.bot = float(bot)
            with open('y.txt', 'r') as file:
                sp = file.read()
                ball.speed_y = int(sp)
            with open('x.txt', 'r') as file:
                spe = file.read()
                ball.speed_x = float(spe)
            c.coords(ball_f, 20, network.top, 55, network.bot)
            network.ball = 1
            os.remove('spawn.txt')
            os.remove('top.txt')
            os.remove('bot.txt')
            os.remove('y.txt')
            os.remove('x.txt')
        if 'goal.txt' in listdir:
            player2.score += 1
            c.itemconfig(player2_score, text=player2.score)
            spawn()
            network.ball = 1
            os.remove('goal.txt')

    def finish():
        messagebox.showinfo('Congratulations', 'Opponent left the game\nCongratulations, you won')
        game_window.destroy()
        os.remove('close.txt')

    def main_function():
        if network.ball == 0:
            check()
        elif network.ball == 1:
            move()
        rackets_move()
        listdir = os.listdir()
        if 'close.txt' in listdir:
            finish()
        game_window.after(30, main_function)

    c.focus_set()

    def keys_down(event):
        if event.keycode == 38:
            player1.speed = -player1.speed_init
        elif event.keycode == 40:
            player1.speed = player1.speed_init
        elif event.keycode == 32:
            if network.start == 0:
                with open('this_comp_ready.txt', 'w') as file:
                    file.write(' ')
                sock = socket.socket()
                sock.connect((network.host, int(network.port)))
                data = {"title": "ready"}
                sock.send(json.dumps(data).encode('utf-8'))
                sock.close()
                network.start = 1
            else:
                print('You are ready already')
    c.bind("<KeyPress>", keys_down)

    def keys_up(event):
        if event.keycode == 38 or event.keycode == 40:
            player1.speed = 0
            sock = socket.socket()
            sock.connect((network.host, int(network.port)))
            data = {"title": "speed",
                    'act': 'stop'
                    }
            sock.send(json.dumps(data).encode('utf-8'))
            sock.close()
    c.bind("<KeyRelease>", keys_up)
    ready()

#GAME 2PC-------------------------
#----------------------------------------------------
#TKINTER-------------------------

def onecscr():
    startscr.destroy()
    def setting():
        name1 = p1_field.get()
        name2 = p2_field.get()
        player1.name = name1
        player2.name = name2
        theme = v.get()
        if theme == 1:
            screen.theme = 1
        elif theme == 2:
            screen.theme = 2
        start_onepc()
        window.destroy()
    window = Tk()
    window.title('Settings')
    title = Label(window, text='LOCAL GAME', font=('Verdana', 14))
    p1_title = Label(window, text="1 player's name")
    p2_title = Label(window, text="2 player's name")
    p1_field = Entry(window, width=18)
    startbut = Button(window, text='Start', width=14, height=1, font=('Verdana', 9), command=setting)
    p2_field = Entry(window, width=18)
    v = IntVar()
    theme1 = Radiobutton(window, text='Theme "DARK"', variable=v, value=1)
    theme1.select()
    theme2 = Radiobutton(window, text='Theme "LIGHT"', variable=v, value=2)
    title.grid(columnspan=3)
    p1_title.grid(row=1, column=0)
    p2_title.grid(row=1, column=2)
    p1_field.grid(row=2, column=0)
    startbut.grid(row=3, column=1)
    p2_field.grid(row=2, column=2)
    theme1.grid(row=3 , column=0)
    theme2.grid(row=3, column=2)


def twocscr():
    startscr.destroy()
    window = Tk()
    def start_1():
        name = name_e.get()
        if len(name) > 0:
            network.name = name
        else:
            messagebox.showerror('ERROR', "You didn't write your name")
        theme = v.get()
        if theme == 1:
            screen.theme = 1
        elif theme == 2:
            screen.theme = 2
        network.host = host_e.get()
        network.port = port_e.get()
        listdir = os.listdir()
        if 'left_side.txt' in listdir:
            messagebox.showerror('Oops', 'Right side was chosen already\nYour side: right')
            if len(network.host) > 0 and len(network.port) > 0:
                try:
                    sock = socket.socket()
                    sock.connect((network.host, int(network.port)))
                    data = {"title": "side",
                            "side": "right",
                            "name": network.name}
                    sock.send(json.dumps(data).encode('utf-8'))
                    sock.close()
                    window.destroy()
                    start_twopc_right()
                except:
                    messagebox.showerror('ERROR', 'You have trouble with connection\nTry to connect one more time')
                    host_e.delete(0, 'end')
                    port_e.delete(0, 'end')
            else:
                messagebox.showerror('ERROR', "You didn't write IP or PORT")
        else:
            if len(network.host) > 0 and len(network.port) > 0:
                try:
                    so = socket.socket()
                    so.connect((network.host, int(network.port)))
                    data = {"title": "side",
                            "side": "left",
                            "name": network.name}
                    so.send(json.dumps(data).encode('utf-8'))
                    so.close()
                    window.destroy()
                    start_twopc_left()
                except:
                    messagebox.showerror('ERROR', 'You have trouble with connection\nTry to connect one more time')
                    host_e.delete(0, 'end')
                    port_e.delete(0, 'end')
            else:
                messagebox.showerror('ERROR', "You didn't write IP or PORT")

    def start_2():
        name = name_e.get()
        if len(name) > 0:
            network.name = name
        else:
            messagebox.showerror('ERROR', "You didn't write your name")
        theme = v.get()
        if theme == 1:
            screen.theme = 1
        elif theme == 2:
            screen.theme = 2
        network.host = host_e.get()
        network.port = port_e.get()
        listdir = os.listdir()
        if 'right_side.txt' in listdir:
            messagebox.showerror('Oops', 'Right side was chosen already\nYour side: left')
            if len(network.host) > 0 and len(network.port) > 0:
                try:
                    sock = socket.socket()
                    sock.connect((network.host, int(network.port)))
                    data = {"title": "side",
                            "side": "left",
                            "name": network.name}
                    sock.send(json.dumps(data).encode('utf-8'))
                    sock.close()
                    window.destroy()
                    start_twopc_left()
                except:
                    messagebox.showerror('ERROR', 'You have trouble with connection\nTry to connect one more time')
                    host_e.delete(0, 'end')
                    port_e.delete(0, 'end')
            else:
                messagebox.showerror('ERROR', "You didn't write IP or PORT")
        else:
            if len(network.host) > 0 and len(network.port) > 0:
                try:
                    so = socket.socket()
                    so.connect((network.host, int(network.port)))
                    data = {"title": "side",
                            "side": "right",
                            "name": network.name}
                    so.send(json.dumps(data).encode('utf-8'))
                    so.close()
                    window.destroy()
                    start_twopc_right()
                except:
                    messagebox.showerror('ERROR', 'You have trouble with connection\nTry to connect one more time')
                    host_e.delete(0, 'end')
                    port_e.delete(0, 'end')
            else:
                messagebox.showerror('ERROR', "You didn't write IP or PORT")

startscr = Tk()
startscr.title('TYPE OF GAME')
stc_title = Label(startscr, text='Choice a type of game', font=('Verdana', 14))
stc_one = Button(startscr, text='Local game', width=15, command=onecscr)
stc_two = Button(startscr, text='Network game', width=15, command=twocscr)
stc_title.grid(columnspan=2)
stc_one.grid(row=1, column=0)
stc_two.grid(row=1, column=1)

mainloop()
#TKINTER-------------------------
sock = socket.socket()
sock.connect((network.host, int(network.port)))
data = {'title': 'finish'}
sock.send(json.dumps(data).encode('utf-8'))
sock.close()
os.remove('name.txt')
try:
    os.remove('right_side.txt')
except:
    os.remove('left_side.txt')
os.remove('this_comp_ready.txt')
os.remove('other_comp_ready.txt')