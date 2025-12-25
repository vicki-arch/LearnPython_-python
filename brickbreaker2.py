"""
File: brickbreaker.py
----------------
YOUR DESCRIPTION HERE
"""
import re

import tkinter
import time
import random

# How big is the playing area?
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 800     # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 8              # How many rows of bricks are there?
N_COLS = 10             # How many columns of bricks are there?
SPACING = 5             # How much space is there between each brick?
BRICK_START_Y = 50      # The y coordinate of the top-most brick
BRICK_HEIGHT = 20       # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS+1) * SPACING ) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 20
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 80
LIFE = 3



START = False

Paddle = None
Bricks = []
NUM = 0
canvas = None

def main():
    global Paddle, Bricks, NUM, canvas
   
    for i in range(N_ROWS+2):
        for j in range(N_COLS):
            color = ['salmon', 'moccasin', 'cornsilk', 'pale green', 'powder blue']
            x1,y1 = j*BRICK_WIDTH+(j+1)*SPACING, BRICK_START_Y+i*BRICK_HEIGHT
            x2,y2 = x1+BRICK_WIDTH, BRICK_START_Y+(i+1)*BRICK_HEIGHT
            
            # create space between bricks
            canvas.create_rectangle(j*SPACING, y2-BRICK_HEIGHT,x1,y1, fill = 'white', outline = 'white')
            Bricks.append(canvas.create_rectangle(x1, y1, x2, y2, fill=color[(i//2)], outline="white"))
            NUM += 1

    create_life_info()
    px1 = CANVAS_WIDTH/2-PADDLE_WIDTH/2
    Paddle = canvas.create_rectangle(px1, PADDLE_Y, px1+PADDLE_WIDTH,CANVAS_HEIGHT-20,fill='black',outline='black',tags ="paddle")
        
    change_x = -4
    change_y = -4

    ball = canvas.create_oval(CANVAS_WIDTH/2-BALL_SIZE, PADDLE_Y-2*BALL_SIZE,
                        CANVAS_WIDTH/2+BALL_SIZE, PADDLE_Y,
                        fill = 'grey', outline = 'grey', tags="ball")    
       
        
    move_circle(ball, change_x, change_y)
    move_paddle(Paddle, PADDLE_Y)

def create_life_info():
    canvas.create_text(10, 25, text='Life: '+str(LIFE), anchor='w', 
                           fill="#320404", font=('Arial', 12, 'bold'), tags="life_text")    

def move_paddle(paddle, PADDLE_Y):
    if START:
        mouse_x = canvas.winfo_pointerx()
        canvas.moveto(paddle, mouse_x-160, PADDLE_Y)
    canvas.after(10, move_paddle, paddle, PADDLE_Y)

def move_circle(ball,change_x, change_y):
    global START, LIFE, NUM
    if not START:
        canvas.delete("end_text")
        canvas.create_text(300, 400, text='Press Space to Start', anchor='center', 
                           fill="#320404", font=('Arial', 15, 'bold'), tags="start_text")
    else:
        canvas.delete("start_text")
        canvas.move(ball, change_x, change_y)
        x_1,y_1,x_2,y_2 = canvas.coords(ball)
        if x_1 <=0 or x_2 >= CANVAS_WIDTH:
            change_x = -change_x
        if y_1 <= 0:
            change_y = -change_y
        if y_2 >= CANVAS_HEIGHT:
            canvas.create_text(300, 400, text='GAME OVER', anchor='center', 
                               fill='#8B0000', font=('Arial', 30, 'bold'), tags="end_text")
            START = False
            if LIFE > 1:
                LIFE -= 1
                canvas.after(1000, restart_round, ball)
            else:
                canvas.after(3000, restart_game)
            return 
        
        colliding_list = canvas.find_overlapping(x_1, y_1, x_2, y_2)
        
        for obj in colliding_list:
            if not canvas.gettags(obj):
                canvas.delete(obj)
                NUM -= 1
                change_y = -change_y
            elif obj == Paddle:
                # ball center and paddle center
                ball_x = (x_1+x_2)/2
                padd_1,_,padd_2,_ = canvas.coords(Paddle)
                padd_center = (padd_1+padd_2)/2

                # calculate offset from -1 to 1
                offset = (ball_x - padd_center) / ((padd_2-padd_1)/2)

                change_x = change_x*offset + random.uniform(-0.5,0.5)
                change_y = -change_y + random.uniform(-0.5,0.5)
        
        if NUM == 0:
            canvas.create_text(300, 400, text='YOU WIN', anchor='center', 
                               fill='#8B0000', font=('Arial', 30, 'bold'), tags="win_text")
            START = False
            canvas.after(3000, restart_game)

    canvas.after(5, move_circle,ball, change_x, change_y)

def restart_round(ball):
    canvas.delete("end_text")
    canvas.delete("life_text")
    create_life_info()
    canvas.coords(
        Paddle,
        CANVAS_WIDTH/2-PADDLE_WIDTH/2, PADDLE_Y, 
        CANVAS_WIDTH/2-PADDLE_WIDTH/2+PADDLE_WIDTH,
        CANVAS_HEIGHT-20
    )
    canvas.coords(
        ball,
        CANVAS_WIDTH/2-BALL_SIZE,
        PADDLE_Y-2*BALL_SIZE,
        CANVAS_WIDTH/2+BALL_SIZE,
        PADDLE_Y
    )
    canvas.after(5, move_circle,ball, -4, -4)


def on_space_press(event):
    global START
    START = True

def restart_game():
    global LIFE, NUM
    canvas.delete("all")
    LIFE = 3
    NUM = 0
    main()

def make_canvas(width, height, title):
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas

if __name__ == '__main__':
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    canvas.bind_all("<space>", on_space_press)
    main()
    canvas.mainloop()
