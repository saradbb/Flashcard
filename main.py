from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random



#####################################    READ DATA FROM FILES      #####################

data = None
try:
    # Try to resume learning from past sessions.
    data = pandas.read_csv("D:\Python\Flash\data/words_to_learn.csv")
except FileNotFoundError:
    # If not, start with all words
    data =  pandas.read_csv("D:\Python\Flash\data/french_words.csv")

print(data)
data_list = data["French"].to_list()       #Extract the French words
#print(data["French"])
#print(data_list)
data_dict = {k:v for k,v in zip(data["French"],data["English"])}  # New Dictionary with k = French and v = English translation of k
#print(data_dict)
word = ""
#correct_words = []
AFTER = NONE        #For window.after()


def on_closing():
    """
    This function is executed when close button is clicked. Once the user confirms close, all the words user still doesnt
    know are saved to a file.
    :return:
    """
    global correct_words
    if messagebox.askokcancel("Quit", "Do you want to quit?"):   #If quit confirmed
        out_dict = {esp:data_dict[esp] for esp in data_list}        #New dictionary of remaining words
        new_df = pandas.DataFrame(out_dict.items(),columns = ["French","English"])    #Convert to dataframe
        new_df.to_csv("D:\Python\Flash\data\words_to_learn.csv", index = False)        #Save in a .csv file
        window.destroy()

def flip_front():
    """
    Function to revert the background and language to English
    :return:
    """
    canvas.itemconfig(canvas_img, image=front_img)
    canvas.itemconfig(language, text="French")


def generate_word():
    """
    Flips the card and generates new french word to learn
    :return:
    """
    global AFTER
    flip_front()
    word = random.choice(data_list)
    canvas.itemconfig(canvas_word, text=word)
    AFTER = window.after(3000, flipback)

def correct_click():
    """
    Represents user clicking the green button. Removes word from learners list and calls function to generate new word
    :return:
    """
    global AFTER,correct_words
    window.after_cancel(AFTER)
    word = canvas.itemcget(canvas_word, "text")
    try:
        data_list.remove(word)
    except ValueError:
        pass
    generate_word()


def incorrect_click():
    """
    Represents user clicking X.
    :return:
    """
    global AFTER
    window.after_cancel(AFTER)
    generate_word()
    #window.after(3000, flipback)



def flipback():
    """
    Shows the english translation with different background
    :return:
    """
    global word
    word = canvas.itemcget(canvas_word,"text")
    #img = PhotoImage(file="D:\Python\Flash\images/card_back.png")
    canvas.itemconfig(canvas_img,image = back_img)
    canvas.itemconfig(language, text = "English")
    txt = data_dict[word]
    canvas.itemconfig(canvas_word, text = txt)






########################################    UI SETUP #################################


#########  MAIN WINDOW ######
window = Tk()
window.title("Language Flashcard")
window.config(bg=BACKGROUND_COLOR)
window.minsize(height=800, width=800)

########   CARD AND TEXT   ####

canvas = Canvas(height=500, width=500)
front_img= PhotoImage(file = "D:\Python\Flash\images/card_front.png")
back_img = PhotoImage(file = "D:\Python\Flash\images/card_back.png")
canvas_img = canvas.create_image(200,265, image = front_img)
language = canvas.create_text(250,140,text = "Frenh",font = ("Black",40,"italic"))
canvas_word = canvas.create_text(250, 260, text = "trouve", font = ("Black", 60, "bold"))
canvas.grid(row=0, column=0, padx = 150, pady = 50, rowspan = 1, columnspan = 2)


############ BUTTONS   ############
buttonPic = PhotoImage(file="D:\Python\Flash\images/right.png")
correct_button = Button(image=buttonPic, highlightthickness=0,command = correct_click)
correct_button.grid(row=1,column = 1, rowspan = 1, columnspan = 1)
b = PhotoImage(file="D:\Python\Flash\images/wrong.png")
incorrect_button = Button(image = b, highlightthickness=0, command = incorrect_click)
incorrect_button.grid(row=1, column=  0, rowspan = 1, columnspan = 1)









window.protocol("WM_DELETE_WINDOW", on_closing)



window.mainloop()
