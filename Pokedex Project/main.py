import pandas as pd
from tkinter import font
import matplotlib as mp
from customtkinter import CTkCanvas
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from window_functions import search_pokemon_
from PIL import ImageFont
from tkinter import ttk
import tkinter as tk
import customtkinter as ctk

#Read the csv and put into a variable
pokedex="pokemon_data.csv"
data=pd.read_csv(pokedex)
currentScene="Main"
pokeChoice="Type"


def hide_me(event):
    event.widget.pack_forget()


def filter_pokemon_():
    global currentScene
    global frameButtons
    frameButtons.configure(height=600,width=600)
    typeDistButton.pack_forget()
    if currentScene=="PokeDetails":
        pokeNameLabel.pack_forget()
        framePokeDetails.pack_forget()
    currentScene="PokeList"
    query=entry.get().strip().lower()
    if pokeChoice=="Type":
        filteredData=data[
            data['Type 1'].str.lower().str.contains(query) |
            data['Type 2'].str.lower().str.contains(query)
        ]
    elif pokeChoice=="Name":
        filteredData=data[
            data['Name'].str.lower().str.contains(query)
        ]
    filteredData=filteredData.drop_duplicates(subset=[
        'Name','Type 1','Type 2'])
    #Destroys all buttons from previous query
    remove_pokemon_()
    for index,row in filteredData.iterrows():
        name=row["Name"]
        type1=row["Type 1"]
        type2=row.get("Type 2", None)
        hp=row["HP"]
        atk=row["Attack"]
        defense=row["Defense"]
        spAtk=row["Sp. Atk"]
        spDef=row["Sp. Def"]
        spd=row["Speed"]
        gen=row["Generation"]
        leg=row["Legendary"]
        button=ctk.CTkButton(frameButtons,fg_color="#147285",
        corner_radius=3,text=name,width=40,
            command=lambda
                name=name,
                type1=type1,
                type2=type2,
                hp=hp,
                atk=atk,
                defense=defense,
                spAtk=spAtk,
                spDef=spDef,
                spd=spd,
                gen=gen,
                leg=leg:
                on_button_click(
                name,type1,type2,
                hp,atk,defense,
                spAtk,spDef,spd,gen,leg))
        button.pack(pady=5)
    canvas.update_idletasks()
    frameButtons.grid_propagate(True)
    canvas.pack( fill="both",expand=True)
    canvas.configure(scrollregion=canvas.bbox("all"))


def on_button_click(
    name,type1,type2,hp,atk,defense,spAtk,spDef,spd,gen,leg):
    global currentScene
    remove_pokemon_()
    currentScene="PokeDetails"
    framePokeDetails.pack(side="top",anchor="ne",padx=10,pady=10)
    count=0
    for i in statButtons:
        var = statButtons[count]
        count+=1
        var.pack(padx=5,pady=5)
    pokeNameLabel.configure(text="Name: "+name)
    pokeTypeLabel.configure(text="Type: "+type1)
    if type2:
        pokeType2Label.configure(text="Type 2: None")
    else:
        pokeType2Label.configure(text="Type 2: "+type2)
    pokeHpLabel.configure(text="HP: "+str(hp))
    pokeAtkLabel.configure(text="Attack: "+str(atk))
    pokeDefLabel.configure(text="Defense: "+str(defense))
    pokeSpAtkLabel.configure(text="SP. Attack: "+str(spAtk))
    pokeSpDefLabel.configure(text="SP. Defense: "+str(spDef))
    pokeSpeedLabel.configure(text="Speed: "+str(spd))
    pokeGenLabel.configure(text="Generation: "+str(gen))
    pokeLegendLabel.configure(text="Legendary?  "+str(leg))
    canvas.configure(scrollregion=canvas.bbox("all"))
    #HERE ALSO MAKE THE GRAPH BUTTON THAT MAKES A POLYGON GRAPH WITH STATS OPEN UP!!!
    #WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK
    # WAKE UP LOOK

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)),"units")


def combobox_callback(choice):
    print("combobox dropdown clicked:",choice)


def back_button_():
    global currentScene
    if currentScene=="Main":
        frameButtons.configure(height=600,width=600)
        print()
    if currentScene=="PokeDetails":
        typeDistButton.pack(pady=10,padx=10,side="top",anchor="w")
        print("detail")
        framePokeDetails.pack_forget()
        remove_pokemon_()
        canvas.update_idletasks()
        currentScene="Main"
    if currentScene=="PokeList":
        typeDistButton.pack(pady=10,padx=10,side="top",anchor="w")
        frameButtons.configure(height=600,width=600)
        remove_pokemon_()
        currentScene="Main"
    if currentScene=="Graph":
        pass


def remove_pokemon_():
    for widget in frameButtons.winfo_children():
        widget.destroy()


def graph_():
    typesCombined=pd.concat([data["Type 1"],data["Type 2"]])
    valueCount=typesCombined.value_counts()
    print(valueCount)
    colours = {
        'Fire': 'red',
        'Water': 'blue',
        'Electric': 'yellow',
        'Grass': 'green',
        'Poison': 'purple',
        'Dragon': 'orange',
        'Fairy': 'pink',
        'Normal': 'brown',
        'Flying': 'lightblue',
        'Psychic': 'pink',
        'Bug': 'yellow',
        'Ground': 'brown',
        'Rock': 'grey',
        'Fighting': 'orange',
        'Dark': 'black',
        'Steel': 'grey',
        'Ghost': 'purple',
        'Ice': 'lightblue'
    }
    colour2=[colours.get(type_, 'grey')for type_ in valueCount.index]
    plt.figure(figsize=(12,8))
    valueCount.plot(kind='bar',color=colour2)
    # Set chart title and labels
    plt.title('Count of Each Type (Type 1 + Type 2)',fontsize=16)
    plt.xlabel('Type',fontsize=12)
    plt.ylabel('Count',fontsize=12)
    # Display the plot
    plt.show()


def poke_type_change(choice):
    global pokeChoice
    pokeChoice = choice

root=ctk.CTk()
root.title("Pokedex")
root.geometry("600x600")
root.configure(bg="#b34448",fg_color="#b34448")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

richBlack = "#0C1821"
lavender = "#CCC9DC"
lavenderDark = "#928DAE"
airForceBlue = "#61819D"
#set theme here!!!!
fontPath="JUST Sans Regular.otf"
customFont=ImageFont.truetype(fontPath,10)
fontName=customFont.getname()[0]
font1=font.Font(family = fontName, size = 10)
#Create the title label

searchFrame=ctk.CTkFrame(root,fg_color="#000000",bg_color="#000000",border_width=0)
searchFrame.pack(fill="x")
label=ctk.CTkLabel(searchFrame,text="Pokedex")
label.pack(pady=10)
#Create the entry field

entry=ctk.CTkEntry(searchFrame,width=370)
entry.pack(side="left",padx=5,pady=5)

searchButton=ctk.CTkButton(searchFrame,text="Search",
                             command=filter_pokemon_,
                          width=100,fg_color=lavender,
                           text_color="#000000")
searchButton.pack(side="left",padx=5,pady=5)

pokeTypeSelector=ctk.CTkOptionMenu(searchFrame,values=["Name",
                "Type"],command=poke_type_change,width=100,
                fg_color=lavender, text_color="#000000",
                button_color=lavenderDark,
                                   button_hover_color=lavenderDark)
pokeTypeSelector.pack(side="left",padx=5,pady=5)
pokeTypeSelector.set("Type")
#comboboxVar = ttk.StringVar(value="Type")
#combobox = tk.ComboBox(searchFrame, values=["Type", "Name"],
                       #    command=combobox_callback,
                        #   width = 200)
#combobox.pack(side = "left", padx = (10,0))

#comboboxVar.set("Type")

#######################THIS IS TKINTER DO A CASCADE INSTEAD OF THIS!!!!!!!!!!!!!

canvas=tk.Canvas(root,bg="#b34448",borderwidth=0,highlightthickness=0)
canvas.pack(fill="both",expand=True)

backFrame=ctk.CTkFrame(root, corner_radius=0, bg_color="#000000")
backFrame.pack(fill = "x")
backButton=ctk.CTkButton(backFrame,text="Home",command=back_button_,
                        width = 200,)
backButton.pack(side="bottom",pady=10)

frameButtons=ctk.CTkFrame(canvas,width=600,height=600,fg_color="#b34448",border_width=0)

scrollbar=ctk.CTkScrollbar(canvas,command=canvas.yview)
scrollbar.pack(side="right",fill="y")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.create_window((0,0),window=frameButtons,anchor="nw",width=600)

frameButtons.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
root.bind_all("<MouseWheel>",on_mouse_wheel)

framePokeDetails=ctk.CTkFrame(canvas,width=600,height=600)
framePokeDetails.pack(side="top",anchor="nw",padx=10,pady=10)
framePokeDetails.pack_forget()

pokeNameLabel=ctk.CTkLabel(framePokeDetails,text="No Name Set")
pokeTypeLabel=ctk.CTkLabel(framePokeDetails,text="No Type Set")
pokeType2Label=ctk.CTkLabel(framePokeDetails,text="No Type 2 Set")
pokeHpLabel=ctk.CTkLabel(framePokeDetails,text="No HP Value Set")
pokeAtkLabel=ctk.CTkLabel(framePokeDetails,text="No Attack Set")
pokeDefLabel=ctk.CTkLabel(framePokeDetails,text="No Defense Set")
pokeSpAtkLabel=ctk.CTkLabel(framePokeDetails,text="No Special Attack Set")
pokeSpDefLabel=ctk.CTkLabel(framePokeDetails,text="No Special Defense Set")
pokeSpeedLabel=ctk.CTkLabel(framePokeDetails,text="No Speed Set")
pokeGenLabel=ctk.CTkLabel(framePokeDetails,text="No Generation Set")
pokeLegendLabel=ctk.CTkLabel(framePokeDetails,text="No Legendary Bool Set")
statButtons = [pokeNameLabel,pokeTypeLabel,pokeType2Label,
               pokeHpLabel,pokeAtkLabel,pokeDefLabel,
               pokeSpAtkLabel,pokeSpDefLabel,pokeSpeedLabel,
               pokeGenLabel,pokeLegendLabel]


frameButtons.configure(height=600,width=600)



typeDistButton=ctk.CTkButton(canvas,text="Type Distribution Graph",command=graph_)
typeDistButton.pack(pady=10,padx=10,side="top",anchor="w")

root.mainloop()