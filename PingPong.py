import tkinter as tk

######## WINDOW
root = tk.Tk()
root.title("Neon-Pong-AI")
root.resizable(0, 0)
canvas = tk.Canvas(root, bg="#020411", width=800, height=480, highlightthickness=0)
controls_text = canvas.create_text(400, 455,text="  Controls: W / S to move - R to reset - I diffculty",fill="#8d6b9f",font=("Montserrat SemiBold", 10))
canvas.pack()
for y in range(0, 480, 20):
    canvas.create_line(400, y, 400, y + 10, fill="#43384e", width=3)
########## VALUES
vx, vy = 7, 7
PADDLE_H = 120
PADDLE_W = 12
PADDLE_SPEED = 10
lpaddle_y = 180 
rpaddle_y = 180  
score1, score2 = 0, 0
keys = set()
bot_speed = 4

def neon(canvas, x1, y1, x2, y2, color_core, color_inner, color_outer):
    outer = canvas.create_rectangle(x1 - 10, y1 - 10, x2 + 10, y2 + 10, fill=color_outer, outline="", stipple="gray50")
    inner = canvas.create_rectangle(x1 - 5, y1 - 5, x2 + 5, y2 + 5,fill=color_inner, outline="", stipple="gray75")
    core = canvas.create_rectangle(x1, y1, x2, y2, fill=color_core, outline="")
    return core, inner, outer


lpaddle, lp_inner, lp_outer = neon(canvas,30, 180, 42, 300,color_core="#ff6b8f",color_inner="#a3235f",color_outer="#3b083b")
rpaddle, rp_inner, rp_outer = neon(canvas,758, 180, 770, 300,color_core="#c400ff",color_inner="#6b1a8f",color_outer="#3b083b")
ball = canvas.create_oval(100, 100, 116, 116, fill="white", width=0)

######### SCORES
score_text = canvas.create_text(200, 50,text="0",fill="#f5ddf0",font=("Montserrat SemiBold Italic", 32))
score_text2 = canvas.create_text(600, 50,text="0",fill="#f5ddf0",font=("Montserrat SemiBold Italic", 32))




########## upanddown
def on_key_down(e):
    keys.add(e.keysym.lower())

def on_key_up(e):
    keys.discard(e.keysym.lower())

root.bind("<KeyPress>", on_key_down)
root.bind("<KeyRelease>", on_key_up)


def update_score():
    canvas.itemconfig(score_text, text=score1)
    canvas.itemconfig(score_text2, text=score2)
    reset()

def reset():
    global vx, vy
    canvas.coords(ball, 392, 232, 408, 248)
    vx = -vx  
    vy = 7



def running():
    global vx, vy, lpaddle_y, rpaddle_y, score1, score2 ,  bot_speed

    if "w" in keys:
        lpaddle_y = max(0, lpaddle_y - PADDLE_SPEED)
    if "s" in keys:
        lpaddle_y = min(480 - PADDLE_H, lpaddle_y + PADDLE_SPEED)
        
    if "i" in keys:
        bot_speed +=0.1
        vx *= 1.05
        vy *= 1.05
        keys.discard("i")
        
    ball_x1, ball_y1, ball_x2, ball_y2 = canvas.coords(ball)
    ball_center_y = (ball_y1 + ball_y2) / 2

    if ball_center_y < rpaddle_y + PADDLE_H / 2:
        rpaddle_y -= bot_speed
    elif ball_center_y > rpaddle_y + PADDLE_H / 2:
        rpaddle_y += bot_speed

    rpaddle_y = max(0, min(480 - PADDLE_H, rpaddle_y))
    if "r" in keys:
        score1 , score2 = 0, 0
        canvas.itemconfig(score_text, text=score1)
        canvas.itemconfig(score_text2, text=score2)
        reset()
    canvas.coords(lpaddle, 30, lpaddle_y, 30 + PADDLE_W, lpaddle_y + PADDLE_H)
    canvas.coords(lp_inner, 30 - 5, lpaddle_y - 5, 30 + PADDLE_W + 5, lpaddle_y + PADDLE_H + 5)
    canvas.coords(lp_outer, 30 - 10, lpaddle_y - 10, 30 + PADDLE_W + 10, lpaddle_y + PADDLE_H + 10)
    canvas.coords(rpaddle, 758, rpaddle_y, 770, rpaddle_y + PADDLE_H)
    canvas.coords(rp_inner, 758 - 5, rpaddle_y - 5, 770 + 5, rpaddle_y + PADDLE_H + 5)
    canvas.coords(rp_outer, 758 - 10, rpaddle_y - 10,770 + 10, rpaddle_y + PADDLE_H + 10)
    canvas.move(ball, vx, vy)
    
    x1, y1, x2, y2 = canvas.coords(ball)
    
    if y1 <= 0 or y2 >= 480:
        vy = -vy
        
    if x1 <= 0:
        score2 += 1
        update_score()
        vx = -vx

    if x2 >= 800:
        score1 += 1
        update_score()
        vx = -vx
        
        

    if x1 <= 42 and y1 < lpaddle_y + PADDLE_H and y2 > lpaddle_y:
        vx = abs(vx)

    if x2 >= 758 and y1 < rpaddle_y + PADDLE_H and y2 > rpaddle_y:
        vx = -abs(vx)

    root.after(16, running)

running()
root.mainloop()
