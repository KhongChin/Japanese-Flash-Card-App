import random
import tkinter
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

try:
    data = pandas.read_csv("words_to_learn.csv")

except FileNotFoundError:
    data = pandas.read_csv("Japanese_words.csv")
    data_dict = data.to_dict(orient="records")

else:
    data_dict = data.to_dict(orient="records")


# ----------------------------------------- FUNCTIONS ----------------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(language_text, text="Japanese", fill="black")
    canvas.itemconfig(word_text, text=current_card["Japanese"], fill="black")
    canvas.itemconfig(japanese_pronunciation, text="", fill="black")
    canvas.itemconfig(canvas_image, image=card_front_logo)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_logo)
    canvas.itemconfig(language_text, text="Translation", fill="white")
    canvas.itemconfig(word_text, text=current_card["Translation"], fill="white")
    canvas.itemconfig(japanese_pronunciation, text=current_card["Japanese_Pronunciation"], fill="white")


def is_known():
    data_dict.remove(current_card)
    remaining_data = pandas.DataFrame(data_dict)
    remaining_data.to_csv("words_to_learn.csv", index=False)
    next_card()


# ----------------------------------------- UI SETUP ----------------------------------------- #
window = tkinter.Tk()
window.title("Japanese Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, flip_card)

canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_logo = tkinter.PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card_front_logo)
canvas.grid(row=0, column=0, columnspan=2)
language_text = canvas.create_text(400, 100, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 250, text="", font=("Arial", 40, "bold"))
japanese_pronunciation = canvas.create_text(400, 400, text="", font=("Arial", 40, "bold"))

card_back_logo = tkinter.PhotoImage(file="./images/card_back.png")

right_image = tkinter.PhotoImage(file="./images/right.png")
known_button = tkinter.Button(image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known, bd=0)
known_button.grid(row=1, column=1)

wrong_image = tkinter.PhotoImage(file="./images/wrong.png")
unknown_button = tkinter.Button(image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card,bd=0)
unknown_button.grid(row=1, column=0)

next_card()

window.mainloop()

