#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os

import utils




class PageThreeTest(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)





    def show(self):
        self.lift()



    def show_df_result(self,df,tvResult):
        rowCount = len(df.index)
        headers = list(df.columns.values)
        i = 0
        # STI du deuxième cas. Très similaire sauf qu'on ne boucle pas sur la meme chose. Ici on boucle sur les colonnes du df. Dans le premier cas c'est via le dictionnaire. -> A améliorer. Créer une méthode pour éviter d'avoir 2 fois le meme code.
        while i < rowCount:
            for item in headers:
                # Si l'item est null il faut le remplir. -> Faudrait changer le if. Ici le nan est en string via la fonction insertColumnDf il faudrait éviter de la mettre en string.
                print(df.at[i, item])
                if pd.isnull(df.at[i, item]) or df.at[i, item] == 'nan' or df.at[i, item] == '':
                    # Ici je récupère la cellule de la colonne sujet.
                    dbrSubject = df.at[i, headers[0]]
                    queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + str(dbrSubject) + "> <" + str(item) + "> ?object } \n}"
                    print(queryString)
                    try:
                        results1 = utils.executeSparqlQuery(queryString)
                    except HTTPError:
                        print("Problème Http dbpedia veuillez réessayer plus tard.")
                    # J'écris les résultats trouvés grâce à la query au dessus.
                    df = insertDataDf(df, results1, i, item)
            i = i + 1

        printDf(df)
        label_frame_selection.destroy()
        global listTvi
        for i in range(0, len(listTvi), 1):
            listTvi[i].destroy()
            listFrame2[i].destroy()

        tvResult["column"] = list(df.columns)
        # delete all records
        for record in tvResult.get_children():
            tvResult.delete(record)

        # add records with new column(s)
        for column in tvResult["columns"]:
            tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists

        for row in df_rows:
            tvResult.insert("", "end",
                            values=row)

        self.show()