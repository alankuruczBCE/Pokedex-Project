import pandas as pd
from tkinter import font
import matplotlib as mp

from window_functions import search_pokemon_
from PIL import ImageFont
from tkinter import ttk
import tkinter as tk

import sv_ttk
#Read the csv and put into a variable
pokedex = "pokemon_data.csv"
data = pd.read_csv(pokedex)
currentScene = "Main"

def hide_me(event):
    event.widget.pack_forget()

#pack() WILL BRING BACK THE HIDDEN ELEMENT

#btn=Button(root, text="Click")
#btn.bind('<Button-1>', hide_me)
#btn.pack()    THIS IS AN EXAMPLE OF ITS USAGE

#Search function
def search_():
    query = entry.get()

    result = search_pokemon_(data, query)

    if result:
        pokeNameString = f"Name: {result["Name"]}"
        pokeTypeString = f"Type: {result["Type 1"]}"

    resultLabel.config(text=pokeNameString)
    typeLabel.config(text=pokeTypeString)


def filter_pokemon_():
    global currentScene
    query = entry.get().strip().lower()
    currentScene = "PokeList"
    filteredData = data[
        data['Type 1'].str.lower().str.contains(query) |
        data['Type 2'].str.lower().str.contains(query)
    ]

    filteredData = filteredData.drop_duplicates(subset=['Name', 'Type 1', 'Type 2'])

    #Destroys all buttons from previous query
    remove_pokemon_()

    for index, row in filteredData.iterrows():
        name = row["Name"]
        button = ttk.Button(frameButtons, text = name, width = 40, command = lambda name = name: on_button_click(name))
        button.pack(pady=5)




    frameButtons.grid_propagate(True)

    canvas.config(scrollregion=frameButtons.bbox("all"))


def on_button_click(name):
    global currentScene
    print(f"Clicked on {name}")
    for widget in frameButtons.winfo_children():
        widget.destroy()
    currentScene = "PokeDetails"
    framePokeDetails.pack(side = "top", anchor = "nw", padx = 10, pady = 10)
    pokeNameLabel.pack(padx = 5, pady = 5)
    pokeNameLabel.config(text = f"Name: {name}")


def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)


def back_button_():
    global currentScene
    if currentScene == "Main":
        print()
    if currentScene == "PokeDetails":
        print("detail")
        pokeNameLabel.pack_forget()
        framePokeDetails.pack_forget()
    if currentScene == "PokeList":
        for widget in frameButtons.winfo_children():
            widget.destroy()
        currentScene = "Main"


def graph_button_():
    remove_pokemon_()
    currentScene = "Graphs"


#Create the window
def remove_pokemon_():
    for widget in frameButtons.winfo_children():
        widget.destroy()


def hide_me_(event):
    event.widget.pack_forget()




root = tk.Tk()
root.title("Pokedex")
root.geometry("700x700")
#set theme here!!!!
fontPath = "JUST Sans Regular.otf"
customFont = ImageFont.truetype(fontPath, 10)
fontName = customFont.getname()[0]
font1 = font.Font(family = fontName, size = 10)

#Create the title label
label = ttk.Label(root, text = "Pokedex")
label.pack(pady = 10)


searchFrame = ttk.Frame(root)
searchFrame.pack(pady = 10, padx = 10, fill = "x")
#Create the entry field
entry = ttk.Entry(searchFrame, width = 40,)
entry.pack(side = "left", padx = (0,10))

searchButton = ttk.Button(searchFrame, text = "Search",
                             command = filter_pokemon_,
                          width=150,)
searchButton.pack(side = "left")

#comboboxVar = ttk.StringVar(value="Type")
#combobox = tk.ComboBox(searchFrame, values=["Type", "Name"],
                       #    command=combobox_callback,
                        #   width = 200)
#combobox.pack(side = "left", padx = (10,0))

#comboboxVar.set("Type")

#######################THIS IS TKINTER DO A CASCADE INSTEAD OF THIS!!!!!!!!!!!!!

backFrame = ttk.Frame(root)
backFrame.pack(fill = "x")
backButton = ttk.Button(backFrame, text = "Home", command = back_button_,
                            width = 200,)
backButton.pack(side = "bottom", pady=10)
canvas = tk.Canvas(root, bg = "black")
canvas.pack( fill = "both", expand = True)



frameButtons = ttk.Frame(canvas, width = 700, height = 700,)

scrollbar = ttk.Scrollbar(canvas, orient = "vertical", command = canvas.yview)
scrollbar.pack(side = "right", fill = "y")
canvas.configure(yscrollcommand = scrollbar.set)

canvas.create_window((0, 0), window=frameButtons, anchor="nw", width = 700)

frameButtons.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
root.bind_all("<MouseWheel>", on_mouse_wheel)
#

framePokeDetails = ttk.Frame(canvas, width = 700, height = 700)
framePokeDetails.pack(side = "top", anchor = "nw", padx = 10, pady = 10)
framePokeDetails.pack_forget()
#Create the search button
pokeNameLabel = ttk.Label(framePokeDetails, text = "No Name Set")
pokeNameLabel.pack(padx = 5, pady = 5)
pokeNameLabel.pack_forget()



resultLabel = ttk.Label(root, text = "", justify ="left", font = (font1, 10))
resultLabel.place(x=20, y=100)
typeLabel = ttk.Label(root, text = "", justify ="left", font = (font1, 10))
typeLabel.place(x=20, y=130)

sv_ttk.set_theme("dark")
root.mainloop()