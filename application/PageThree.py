#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os

import utils
import pandas as pd




class PageThree(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.tvResult = ttk.Treeview(self)
        self.tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)   # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(self.tvResult, orient="vertical",
                                   command=self.tvResult.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(self.tvResult, orient="horizontal",
                                   command=self.tvResult.xview)  # command means update the xaxis view of the widget
        self.tvResult.configure(xscrollcommand=treescrollx.set,
                           yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget


    def show(self):
        self.lift()



    def show_df_result(self,df):
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
                    df = utils.insertDataDf(df, results1, i, item)
            i = i + 1

        utils.printDf(df)
        #label_frame_selection.destroy()
        global listTvi
        listTvi = list()
        for i in range(0, len(listTvi), 1):
            listTvi[i].destroy()
            listFrame2[i].destroy()

        self.tvResult["column"] = list(df.columns)
        # delete all records
        for record in self.tvResult.get_children():
            self.tvResult.delete(record)

        # add records with new column(s)
        for column in self.tvResult["columns"]:
            self.tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists

        for row in df_rows:
            self.tvResult.insert("", "end",
                            values=row)

        self.show()