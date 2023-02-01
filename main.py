from tkinter import *
import pandas
import random

# In case already used the program once, just will show the unknown cards
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/english_words.csv")
to_learn = data.to_dict(orient="records")
current_card = {}


# Show the next word to learn
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


# Delets the known card from card list
def is_know():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# Flip the card from english to portuguese
def flip_card():
    canvas.itemconfig(card_title, text="Portugues", fill="white")
    canvas.itemconfig(card_word, text=current_card["Portugues"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# Configuring the window
window = Tk()
window.title("Flash Cards")
BACKGROUND_COLOR = "#B1DDC6"
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Formating Style
canvas = Canvas(width=800, height=520)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 260, image=card_front_img)
card_title = canvas.create_text(400, 180, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 290, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Red button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# Green Button
check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, padx=10, highlightthickness=0, command=is_know)
check_button.grid(row=1, column=1)

# Starts with a word from the csv file
next_card()
window.mainloop()
