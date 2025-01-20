import pandas as pd
from tkinter import font
import matplotlib as mp

from window_functions import search_pokemon_
from PIL import ImageFont
from tkinter import ttk
import tkinter as tk
import customtkinter as ctk

#Read the csv and put into a variable
pokedex = "pokemon_data.csv"
data = pd.read_csv(pokedex)
currentScene = "Main"
fail = 1


def hide_me(event):
    event.widget.pack_forget()

#pack() WILL BRING BACK THE HIDDEN ELEMENT

#btn=Button(root, text="Click")
#btn.bind('<Button-1>', hide_me)
#btn.pack()    THIS IS AN EXAMPLE OF ITS USAGE

#Search function
def search_():
    scrollbar.pack(side="right", fill="y")
    query = entry.get()

    result = search_pokemon_(data, query)

    if result:
        textFail.configure(text = "")
        pokeNameString = f"Name: {result["Name"]}"
        pokeTypeString = f"Type: {result["Type 1"]}"

    resultLabel.config(text=pokeNameString)
    typeLabel.config(text=pokeTypeString)


def filter_pokemon_():
    global currentScene
    global frameButtons
    frameButtons.configure(height=900, width=1200)
    textFail.pack_forget()
    if currentScene == "PokeDetails":
        pokeNameLabel.pack_forget()
        framePokeDetails.pack_forget()
    currentScene = "PokeList"
    query = entry.get().strip().lower()
    filteredData = data[
        data['Type 1'].str.lower().str.contains(query) |
        data['Type 2'].str.lower().str.contains(query)
    ]

    filteredData = filteredData.drop_duplicates(subset=['Name', 'Type 1', 'Type 2'])

    #Destroys all buttons from previous query
    remove_pokemon_()

    for index, row in filteredData.iterrows():
        name = row["Name"]
        type1 = row["Type 1"]
        type2 = row.get("Type 2", None)
        hp = row["HP"]
        button = ctk.CTkButton(frameButtons, fg_color = "#147285",
                               corner_radius=3,text = name, width = 40,
                               command = lambda name = name,
                                                type1 = type1,
                               type2 = type2,
                               hp = hp:
                               on_button_click(name, type1, type2, hp))
        button.pack(pady=5)

    canvas.update_idletasks()
    frameButtons.grid_propagate(True)
    canvas.pack( fill = "both", expand = True)
    canvas.configure(scrollregion=canvas.bbox("all"))


def on_button_click(name, type1, type2, hp):
    global currentScene
    for widget in frameButtons.winfo_children():
        widget.destroy()
    currentScene = "PokeDetails"
    framePokeDetails.pack(side = "top", anchor = "nw", padx = 10, pady = 10)
    pokeNameLabel.pack(padx = 5, pady = 5)
    pokeTypeLabel.pack(padx=5, pady=5)
    pokeType2Label.pack(padx=5, pady=5)
    pokeHpLabel.pack(padx=5, pady=5)
    pokeNameLabel.configure(text = "Name: " + name)
    pokeTypeLabel.configure(text = "Type: " + type1)
    if type2:
        pokeType2Label.configure(text = "Type 2: None")
    else:
        pokeType2Label.configure(text = "Type 2: " + type2)
    pokeHpLabel.configure(text = "HP: " + str(hp))

    canvas.configure(scrollregion=canvas.bbox("all"))


def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)


def back_button_():
    global currentScene
    if currentScene == "Main":
        frameButtons.configure(height=900, width=1200)
        print()
    if currentScene == "PokeDetails":
        textFail.pack(pady=300)
        print("detail")
        framePokeDetails.pack_forget()
        for widget in frameButtons.winfo_children():
            widget.destroy()
        canvas.update_idletasks()
        currentScene = "Main"
    if currentScene == "PokeList":
        textFail.pack(pady=300)
        frameButtons.configure(height=900, width=1200)
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




root = ctk.CTk()
root.title("Pokedex")
root.geometry("1200x900")
root.configure(bg="#b34448", fg_color="#b34448")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
#set theme here!!!!
fontPath = "JUST Sans Regular.otf"
customFont = ImageFont.truetype(fontPath, 10)
fontName = customFont.getname()[0]
font1 = font.Font(family = fontName, size = 10)

#Create the title label


searchFrame = ctk.CTkFrame(root, fg_color= "#380b0d", bg_color= "#380b0d", border_width = 0)
searchFrame.pack(fill = "x")
label = ctk.CTkLabel(searchFrame, text = "Pokedex")
label.pack(pady = 10)
#Create the entry field

entry = ctk.CTkEntry(searchFrame, width = 900,)
entry.pack(side = "left", padx = 10, pady = 5)

searchButton = ctk.CTkButton(searchFrame, text = "Search",
                             command = filter_pokemon_,
                          width=300, fg_color="#963035")
searchButton.pack(side = "left", padx = 10, pady = 5)

#comboboxVar = ttk.StringVar(value="Type")
#combobox = tk.ComboBox(searchFrame, values=["Type", "Name"],
                       #    command=combobox_callback,
                        #   width = 200)
#combobox.pack(side = "left", padx = (10,0))

#comboboxVar.set("Type")

#######################THIS IS TKINTER DO A CASCADE INSTEAD OF THIS!!!!!!!!!!!!!

canvas = tk.Canvas(root, bg="#b34448", borderwidth=0, highlightthickness=0)
canvas.pack( fill = "both", expand = True)

backFrame = ctk.CTkFrame(root)
backFrame.pack(fill = "x")
backButton = ctk.CTkButton(backFrame, text = "Home", command = back_button_,
                            width = 200,)
backButton.pack(side = "bottom", pady=10)



frameButtons = ctk.CTkFrame(canvas, width = 1205, height = 900, fg_color= "#b34448", border_width=0,)


scrollbar = ctk.CTkScrollbar(canvas, command = canvas.yview)
scrollbar.pack(side = "right", fill = "y")
canvas.configure(yscrollcommand = scrollbar.set)

canvas.create_window((0, 0), window=frameButtons, anchor="nw", width = 1200)

frameButtons.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
root.bind_all("<MouseWheel>", on_mouse_wheel)
#

textFail = ctk.CTkLabel(canvas, text = "Search for a Pokemon")
textFail.pack(pady = 300)

framePokeDetails = ctk.CTkFrame(canvas, width = 1200, height = 900)
framePokeDetails.pack(side = "top", anchor = "nw", padx = 10, pady = 10)
framePokeDetails.pack_forget()
#Create the search button
pokeNameLabel = ctk.CTkLabel(framePokeDetails, text = "No Name Set")
pokeNameLabel.pack_forget()
pokeTypeLabel = ctk.CTkLabel(framePokeDetails, text = "No Type Set")
pokeNameLabel.pack_forget()
pokeType2Label = ctk.CTkLabel(framePokeDetails, text = "No Type 2 Set")
pokeHpLabel = ctk.CTkLabel(framePokeDetails, text = "No HP Value Set")

frameButtons.configure(height=900, width=1200)

resultLabel = ctk.CTkLabel(root,text="",justify="left",font=(font1, 10))
resultLabel.place(x=20,y=100)
resultLabel.pack_forget()
typeLabel = ttk.Label(root,text="",justify="left",font=(font1, 10))
typeLabel.place(x=20,y=130)
typeLabel.pack_forget()



root.mainloop()