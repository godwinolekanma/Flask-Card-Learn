from tkinter import *
import pandas
import random
import csv

BACKGROUND_COLOR = "#B1DDC6"
DATA = pandas.read_csv("./data/french_words.csv")
used_word_list = []
word_to_learn = pandas.read_csv("./data/french_words.csv").to_dict(orient="records")
french_item = ""
english_item = ""


def french_getter():
    global used_word_list, french_item
    # Get random choice from French words data column
    word = random.choice(DATA.French)
    if word in used_word_list:
        french_getter()
    else:
        used_word_list.append(word)
        french_item = word
        return french_item


def english_getter():
    global french_item, english_item
    item_row = DATA[DATA.French == french_item]
    english_word = item_row.English.to_list()
    english_item = english_word[0]
    return english_item


def change_canvas():
    global english_item
    english_item = english_getter()
    canvas.itemconfig(card, image=back_image)
    canvas.itemconfig(language, text="English")
    canvas.itemconfig(french_word, text=english_item)


def right_click():
    left_click()
    current_card = DATA[DATA.French == french_item].to_dict(orient="records")
    word_to_learn.remove(current_card[0])
    data = pandas.DataFrame(word_to_learn)
    data.to_csv("./data/more_to_learn.csv", index=False)


def left_click():
    global french_item, flip_timer
    window.after_cancel(flip_timer)
    french_item = french_getter()
    canvas.itemconfig(card, image=front_image)
    canvas.itemconfig(language, text="French")
    canvas.itemconfig(french_word, text=french_item)
    flip_timer = window.after(3000, change_canvas)


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg="#B1DDC6")

flip_timer = window.after(3000, change_canvas)

canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
card = canvas.create_image(400, 263, image=front_image)
language = canvas.create_text(400, 150, text="French", fill="black", font=("Arial", 40, "italic"))
french_word = canvas.create_text(400, 263, text=french_getter(), fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(highlightbackground="#B1DDC6", image=wrong_image, command=left_click)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png", )
right_button = Button(highlightbackground="#B1DDC6", image=right_image, command=right_click)
right_button.grid(column=1, row=1)

window.mainloop()
