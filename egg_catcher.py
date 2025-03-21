from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

canvas_width = 800
canvas_height = 400
root = Tk()
c = Canvas(root, width=canvas_width, height=canvas_height, background='deep sky blue')
c.create_rectangle(-5, canvas_height-100, canvas_width + 5, canvas_height + 5, fill='sea green', width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

color_cycle = cycle(['light blue', 'light green', 'light pink', 'light yellow', 'light cyan'])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 100
egg_interval = 4000
difficulty_factor = 0.95

catcher_colors = ['pink', 'yellow']  # Colors for player catchers
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20
catchers = []
for i, color in enumerate(catcher_colors):
    catcher = c.create_arc(catcher_start_x, catcher_start_y, catcher_start_x + catcher_width, catcher_start_y + catcher_height,
                           start=200, extent=140, style='arc', outline=color, width=3)
    catchers.append(catcher)

game_font = font.nametofont('TkFixedFont')
game_font.config(size=18)

score = [0, 0]  # Score for each player
score_texts = []
for i in range(len(catcher_colors)):
    score_text = c.create_text(10, 10 + i * 30, anchor='nw', font=game_font, fill='darkblue',
                               text='Player ' + str(i + 1) + ' Score: ' + str(score[i]))
    score_texts.append(score_text)

lives_remaining = [3, 3]  # Lives remaining for each player
lives_texts = []
for i in range(len(catcher_colors)):
    lives_text = c.create_text(canvas_width - 10, 10 + i * 30, anchor='ne', font=game_font, fill='darkblue',
                               text='Player ' + str(i + 1) + ' Lives: ' + str(lives_remaining[i]))
    lives_texts.append(lives_text)

eggs = []

def create_egg():
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        c.move(egg, 0, 10)
        if egg_y2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if all(lives == 0 for lives in lives_remaining):
        messagebox.showinfo('Game Over!', 'Both players have lost the game!')

def lose_a_life():
    for i in range(len(catcher_colors)):
        if lives_remaining[i] > 0:
            lives_remaining[i] -= 1
            c.itemconfigure(lives_texts[i], text='Player ' + str(i + 1) + ' Lives: ' + str(lives_remaining[i]))

def check_catch():
    for i, catcher in enumerate(catchers):
        (catcher_x, catcher_y, catcher_x2, catcher_y2) = c.coords(catcher)
        for egg in eggs:
            (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
            if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 40:
                eggs.remove(egg)
                c.delete(egg)
                increase_score(i, egg_score)
    root.after(100, check_catch)

def increase_score(player_index, points):
    score[player_index] += points
    c.itemconfigure(score_texts[player_index], text='Player ' + str(player_index + 1) + ' Score: ' + str(score[player_index]))

def move_left(event):
    if c.coords(catchers[0])[0] > 0:
        c.move(catchers[0], -20, 0)

def move_right(event):
    if c.coords(catchers[0])[2] < canvas_width:
        c.move(catchers[0], 20, 0)

def move_s(event):
    if c.coords(catchers[1])[0] > 0:
        c.move(catchers[1], -20, 0)

def move_d(event):
    if c.coords(catchers[1])[2] < canvas_width:
        c.move(catchers[1], 20, 0)

c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.bind('<s>', move_s)
c.bind('<d>', move_d)
c.focus_set()

root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)
root.mainloop()