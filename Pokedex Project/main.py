#section for imports
import random
from random import randint

import pandas as pd
from matplotlib import pyplot as plt
import tkinter as tk
import customtkinter as ctk
import numpy as np

#Read the csv and put into a variable
pokedex="pokemon_data.csv"
data=pd.read_csv(pokedex)

#Sets the current scene to main. it's opened on main by default.
currentScene="Main"
#Sets the default criteria to Type instead of Name for searching.
pokeChoice="Type"
#Sets colours that get used by the UI
lapisLazuli="#003D5B"
periwinkle="#B3C2F2"
richBlack="#0C1821"
lavender="#CCC9DC"
lavenderDark = "#928DAE"
airForceBlue = "#61819D"

#This function filters the data file, finding pokemon under your query and
#criteria selected (pokeChoice) and then creates buttons for each pokemon
#which when clicked, send you into a menu detailing their statistics.
def filter_pokemon_():
    global currentScene
    #pack_forget removes the item from the UI, to bring it back, you
    #need to use pack() again and previous commands will not be remembered
    typeDistButton.pack_forget()
    randomPokemonButton.pack_forget()
    if currentScene=="PokeDetails":
        pokeNameLabel.pack_forget()
        framePokeDetails.pack_forget()
        spiderButton.pack_forget()
    currentScene="PokeList"
    #removes empty spaces and lowercases the query
    query=entry.get().strip().lower()
    #if the criteria is type, go by type
    if pokeChoice=="Type":
        if pokeChoice.isalpha():
            filteredData=data[
                data['Type 1'].str.lower().str.contains(query) |
                data['Type 2'].str.lower().str.contains(query)
            ]

    #if it isn't that, go by the name
    elif pokeChoice=="Name":
        if pokeChoice.isalpha():
            filteredData=data[
                data['Name'].str.lower().str.contains(query)
            ]

    elif pokeChoice=="Generation":
        queryInt=int(query)
        filteredData=data[
            data['Generation'] == queryInt
        ]
    filteredData=filteredData.drop_duplicates(subset=[
        'Name','Type 1','Type 2'])

    #Destroys all buttons from previous query
    remove_pokemon_()
    #this ungodly thing creates the buttons
    for index,row in filteredData.iterrows():
        name=row["Name"]
        type1=row["Type 1"]
        #row.get is used because some pokemon do not have a second type
        #and python doesn't like it if you use row[] and nothing appears
        type2=row.get("Type 2", None)
        hp=row["HP"]
        atk=row["Attack"]
        defense=row["Defense"]
        spAtk=row["Sp. Atk"]
        spDef=row["Sp. Def"]
        spd=row["Speed"]
        gen=row["Generation"]
        leg=row["Legendary"]
        #the lambda part of this command is kinda important.

        #it makes it so that the button has its own variation of each stat
        #and when clicked, it uses the variables that correspond to it
        #in its function
        button=ctk.CTkButton(frameButtons,fg_color=lapisLazuli,
        corner_radius=8,text=name,width=40, text_color="white",
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
    #to be honest this stuff doesnt make the most sense in why it works
    #it just does, and i'd like to keep it that way.
    #i know what each command does in isolation but removing any of them
    #breaks it ALL and i dont know why
    canvas.update_idletasks()
    frameButtons.grid_propagate(True)
    canvas.pack( fill="both",expand=True)
    canvas.configure(scrollregion=canvas.bbox("all"))

#when a button created by filter_pokemon is clicked, this is called
def on_button_click(
    name,type1,type2,hp,atk,defense,spAtk,spDef,spd,gen,leg):
    global currentScene
    global nameX,type1X,type2X,hpX,atkX,defenseX,spAtkX,spDefX,spdX,genX,legX
    #this stuff looks messy but its just passing variables and another type
    #i probably could have used a dictionary but i needed to prioritise
    #other stuff in the code, so I didn't get around to it
    remove_pokemon_()
    currentScene="PokeDetails"
    #adds UI elements
    framePokeDetails.pack(side="right",anchor="n",padx=10,pady=10)
    spiderButton.pack(side="left",anchor="n",padx=10,pady=10)
    randomPokemonButton.pack(side="left",pady=10,anchor="n")
    count=0
    nameX=name
    type1X=type1
    type2X=type2
    hpX=hp
    atkX=atk
    defenseX=defense
    spAtkX=spAtk
    spDefX=spDef
    spdX=spd
    genX=gen
    legX=leg
    #i dont know why i couldn't have just used i instead of count
    #but python didn't like it, and i actually dont really know why
    for i in statButtons:
        var = statButtons[count]
        count+=1
        var.pack(padx=15,pady=5)
    #this part just changes the text of each label for the statistics
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
    typeDistButton.pack_forget()


#this is for scrolling
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)),"units")


#this is where the scene stuff matters
#when home is clicked, stuff gets removed.
#its a lot faster than just removing everything that could be there
def back_button_():
    global currentScene
    if currentScene=="Main":
        print()
    if currentScene=="PokeDetails":
        typeDistButton.pack(pady=10,padx=10,side="top",anchor="w")
        randomPokemonButton.pack(pady=10,padx=10,side="top",anchor="w")
        print("detail")
        framePokeDetails.pack_forget()
        spiderButton.pack_forget()
        remove_pokemon_()
        canvas.update_idletasks()
        currentScene="Main"
    if currentScene=="PokeList":
        typeDistButton.pack(pady=10,padx=10,side="top",anchor="w")
        remove_pokemon_()
        currentScene="Main"


#removes all buttons created by filter_pokemon
def remove_pokemon_():
    for widget in frameButtons.winfo_children():
        widget.destroy()

#this one needs a genius to figure it out
def graph_():
    #this combines type 1 and type 2
    typesCombined=pd.concat([data["Type 1"],data["Type 2"]])
    #this counts how many of each type exists
    valueCount=typesCombined.value_counts()
    print(valueCount)
    #index for types + bar colours
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
    #sets the size of the window
    #matplotlib WHY ON THIS PLANET would you do it in inches and not px???????
    plt.figure(figsize=(12,8))
    valueCount.plot(kind='bar',color=colour2)
    #set the title and labels
    plt.title('Count of Each Type (Type 1 + Type 2)',fontsize=16)
    plt.xlabel('Type',fontsize=12)
    plt.ylabel('Count',fontsize=12)
    #display the graph
    plt.show()

#this one opens a spider graph
#(i know, cool right?)
def spider_graph_button():
    labels=['Attack','Defense','Sp. Attack','Sp. Defense','Speed','HP']
    values=[atkX,defenseX,spAtkX,spDefX,spdX,hpX]
    numLabels=len(labels)

    #i dont think im gonna remember how to do this in time for the ESP
    angle=np.linspace(0,2*np.pi,numLabels,endpoint=False).tolist()

    values+=values[:1]
    angle+=angle[:1]

    #i hated figuring this out. worst part of python ive
    #ever had the displeasure of doing
    fig,spider=plt.subplots(figsize=(6,6),subplot_kw=dict(polar=True))
    spider.fill(angle,values,color='blue',alpha=0.25)
    spider.plot(angle,values,color='blue',linewidth=2)
    spider.set_xticks(angle[:-1])
    spider.set_xticklabels(labels)
    plt.show()

#just stuff for the criteria selector
def poke_type_change(choice):
    global pokeChoice
    pokeChoice = choice


def random_pokemon_():
    randomNum=random.randint(1,802)
    row = data.iloc[randomNum]
    name = row["Name"]
    type1 = row["Type 1"]
    type2 = row.get("Type 2", None)
    hp = row["HP"]
    atk = row["Attack"]
    defense = row["Defense"]
    spAtk = row["Sp. Atk"]
    spDef = row["Sp. Def"]
    spd = row["Speed"]
    gen = row["Generation"]
    leg = row["Legendary"]
    on_button_click(name,type1,type2,hp,atk,defense,spAtk,spDef,spd,gen,leg)
    currentScene="PokeDetails"


#--------------------------------UI------------------------------------------#
#lis it a bird, is it a plane?
#no, its the text 'ui' in all caps with dashes!

#creates the window and sets stuff
root=ctk.CTk()
root.resizable(False,True)
root.title("Pokedex")
root.geometry("600x600")
root.configure(bg=periwinkle,fg_color=periwinkle)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#in tkinter and other variations (such as customtkinter which I use),
#placing ui elements by themselves works, but Frames make it easier to keep
#elements in one place and next to each other. It's not for everything though.

#Frame for the top bar
searchFrame=ctk.CTkFrame(root,fg_color="#000000",bg_color="#000000",
border_width=0)
searchFrame.pack(fill="x")
#pokedex text
label=ctk.CTkLabel(searchFrame,text="Pokedex")
label.pack(pady=(5,0))

#the searchbar (the coup de grass or whatever)
entry=ctk.CTkEntry(searchFrame,width=370)
entry.pack(side="left",padx=5,pady=5,expand=True,fill="both")

#creates the search button and gives it a function.
searchButton=ctk.CTkButton(searchFrame,text="Search",
command=filter_pokemon_,width=100,fg_color=lavender,
text_color="#000000",hover_color=lavender)
searchButton.pack(side="left",padx=5,pady=5,fill="both")

#the crteria selector appears!
pokeTypeSelector=ctk.CTkOptionMenu(searchFrame,values=["Name",
                "Type","Generation"],command=poke_type_change,width=100,
                fg_color=lavender, text_color="#000000",
                button_color=lavenderDark,
                                   button_hover_color=lavenderDark)
pokeTypeSelector.pack(side="left",padx=5,pady=5,fill="both")
#sets the default criteria to type
pokeTypeSelector.set("Type")

#THIS HAS CAUSED ME IMMENSE SUFFERING.
#anyway its a canvas and you can scroll with it.

#customtkinter has a scrollableframe class but i modified tkinter code
#that i used to have so I didn't want to change things around considering
#that a lot of code would've needed to be modified which wasn't worth
#the work especially since it wouldn't really benefit me
canvas=tk.Canvas(root,bg=periwinkle,borderwidth=0,highlightthickness=0)
canvas.pack(fill="both",expand=True,anchor="n")

#creates a frame for the back button
backFrame=ctk.CTkFrame(root, corner_radius=0, fg_color="#000000")
backFrame.pack(fill = "x")
#creates the back button
backButton=ctk.CTkButton(backFrame,text="Home",command=back_button_,
                        width = 200,fg_color=lavender,hover_color=lavender,
                         text_color="black")
backButton.pack(side="bottom",pady=10)

#creates the frame for the buttons
frameButtons=ctk.CTkFrame(canvas,
height=600,fg_color=periwinkle,border_width=0)

#creates the scrollbar and gives it a command (as well as the canvas)
scrollbar=ctk.CTkScrollbar(canvas,command=canvas.yview)
scrollbar.pack(side="right",fill="y")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.create_window((0,0),window=frameButtons,anchor="n")

#guess what happens when a scrollbar and a framebuttons meet.
frameButtons.bind("<Configure>",
lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
root.bind_all("<MouseWheel>",on_mouse_wheel)

#creates the frame for the pokemon statistics
#and then removes it
framePokeDetails=ctk.CTkFrame(canvas)
framePokeDetails.pack(side="right",anchor="n",padx=10,pady=10)
framePokeDetails.pack_forget()

#same thing here but for the spider graph button
spiderButton=ctk.CTkButton(canvas,
text='Statistics Graph',command=spider_graph_button,
width=130,fg_color=lapisLazuli,hover_color=lapisLazuli,
text_color='#FFFFFF',corner_radius=5)
spiderButton.pack(side="left",anchor="n",padx=10,pady=10)
spiderButton.pack_forget()

#dont even ask
#this is creating each stat label
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

#makes framebuttons fit the window
frameButtons.configure(height=600,width=600)

#creates the bar chart button
typeDistButton=ctk.CTkButton(canvas,
text="Type Distribution Graph",command=graph_,
fg_color=lapisLazuli,hover_color=lapisLazuli,)
typeDistButton.pack(pady=10,padx=10,side="top",anchor="w")

#creates the random pokemon button
randomPokemonButton=ctk.CTkButton(canvas,text="Random Pokemon",
command=random_pokemon_,fg_color=lapisLazuli,hover_color=lapisLazuli)
randomPokemonButton.pack(pady=10,padx=10,side="top",anchor="w")

#this is needed for the window to run
root.mainloop()