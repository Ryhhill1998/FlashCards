from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
cards_list = {}

# -----------------------CREATE WORDS LISTS----------------------- #
try:
    data = pd.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("french_words.csv")
    cards_list = original_data.to_dict(orient="records")
else:
    cards_list = data.to_dict(orient="records")


# ----------------------CREATE WORD FUNCTIONS---------------------- #
def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(cards_list)
    french_word = current_card["French"]
    canvas.itemconfig(card_display, image=card_front_img)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french_word, fill="black")
    flip_timer = window.after(3000, flip_card)


def new_card_known():
    global current_card, flip_timer, cards_list
    window.after_cancel(flip_timer)

    cards_list.remove(current_card)

    words_to_learn = pd.DataFrame(cards_list)
    words_to_learn.to_csv("words_to_learn.csv", index=False)

    new_card()


def flip_card():
    english_word = current_card["English"]
    canvas.itemconfig(card_display, image=card_back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_word, fill="white")


# ----------------------------SETUP UI---------------------------- #
# Create window
window = Tk()
window.title("Flash Card App")
window.config(bg=BACKGROUND_COLOR, padx=20, pady=20)

flip_timer = window.after(3000, flip_card)

# Create canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_display = canvas.create_image(400, 263, image=card_front_img)
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), fill="black")
canvas.grid(column=0, row=0, columnspan=2)

# Create buttons
right_img = PhotoImage(file="right.png")
right_button = Button(image=right_img, command=new_card_known, highlightthickness=0, border=0)
right_button.grid(column=1, row=1)

wrong_img = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_img, command=new_card, highlightthickness=0, border=0)
wrong_button.grid(column=0, row=1)

new_card()

window.mainloop()
