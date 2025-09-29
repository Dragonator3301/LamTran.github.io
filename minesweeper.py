import tkinter as tk
import random as rd
import time

root = tk.Tk()
root.title("bomb: 50")
root.geometry("465x390")
root.resizable(False, False)

buttons = {}
for r in range(15):
    for c in range(15):
        btn = tk.Button(width=3, height=1)
        btn.grid(row=r, column=c)
        buttons[(r, c)] = btn

first_square_clicked = False
bombs = set()


def gameover():
    for button in buttons:
        buttons[button].config(state="disabled", bg="black", fg="white")
    for bomb in bombs:
        if bomb in marked:
            buttons[bomb].config(bg="yellow", text="💣")
        else:
            buttons[bomb].config(
                state="disabled", relief="raised", bg="red", text="💣")


marked = set()


def mark_bomb(event):
    widget = event.widget
    if widget['state'] == 'disabled':
        return
    pos = getattr(widget, 'pos', None)
    if pos is None:
        for p, b in buttons.items():
            if b is widget:
                pos = p
                break
    if pos in marked:
        marked.remove(pos)
        widget.config(bg="SystemButtonFace", text="", relief="raised")
    else:
        marked.add(pos)
        widget.config(bg="yellow", text="🚩", relief="sunken")


for button in buttons:
    buttons[button].bind("<Button-3>", mark_bomb)


def disable_clicked_squares(pos):
    global first_square_clicked
    r, c = pos

    if not first_square_clicked:
        start_game(pos)

    reveal_square(r, c)


def reveal_square(r, c):
    if (r, c) not in buttons:
        return
    if buttons[(r, c)]["state"] == "disabled":
        return

    nearby = find_bomb(r, c)

    if nearby == 0:
        buttons[(r, c)].config(state="disabled",
                               relief="sunken", text="", bg="white")
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if (i, j) != (r, c):
                    reveal_square(i, j)
    else:
        buttons[(r, c)].config(state="disabled", bg="white",
                               relief="sunken", text=str(nearby))


def start_game(first_click):
    global bombs, first_square_clicked
    r, c = first_click
    safe_zone = {(i, j) for i in range(r-1, r+2) for j in range(c-1, c+2)}
    available_positions = [
        pos for pos in buttons.keys() if pos not in safe_zone]

    bomb_position = rd.sample(available_positions, 50)
    bombs = set(bomb_position)

    for bomb in bomb_position:
        buttons[bomb].config(command=gameover)

    first_square_clicked = True


for pos, button in buttons.items():
    button.config(command=lambda p=pos: disable_clicked_squares(p))


def find_bomb(r, c):
    nearby = 0
    for i in range(r-1, r+2):
        for j in range(c-1, c+2):
            if (i, j) == (r, c):
                continue
            if (i, j) in bombs:
                nearby += 1
    return nearby


root.mainloop()
