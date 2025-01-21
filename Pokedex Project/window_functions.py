import pandas as pd
from tkinter import messagebox

def search_pokemon_(data,query):
    #data is a pd.dataframe, which is the pokedex
    #query (string) is the pokemon name that is searched.
    query=query.strip() #removes redundant spaces
    if not query:
        messagebox.showerror("ERROR","Nothing is entered into the searchbar")
    output=data[data["Name"].str.lower()==query.lower()]
    if output.empty:
        messagebox.showinfo("ERROR", "No valid pokemon found.")
        return None
    row=output.iloc[0]
    pokeName=row["Name"]
    pokeType=row["Type 1"]
    pokeType2=row.get("Type 2",None)
    pokeHP=row["HP"]
    pokeAttack=row["Attack"]
    pokeDefense=row["Defense"]
    pokeSpAttack=row["Sp. Atk"]
    pokeSpDefense=row["Sp. Def"]
    pokeSpeed=row["Speed"]
    pokeGeneration=row["Generation"]
    pokeLegendary=row["Legendary"]
    return {
        "Name":pokeName,
        "Type 1":pokeType,
        "Type 2":pokeType2,
        "HP":pokeHP,
        "Attack":pokeAttack,
        "Defense":pokeDefense,
        "Sp. Atk":pokeSpAttack,
        "Sp. Def":pokeSpDefense,
        "Speed":pokeSpeed,
        "Generation":pokeGeneration,
        "Legendary":pokeLegendary,
    }