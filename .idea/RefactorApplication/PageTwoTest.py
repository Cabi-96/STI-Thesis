#Interface
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os

#Algo Integration
from requests.exceptions import MissingSchema, HTTPError
from tabulate import tabulate
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from MtabExtractTable import MtabAnnotationApi

import utils



class PageTwoTest(Frame):

    def __init__(self, *args, **kwargs):
        ######Frame pagetwo  : two container one for result (frame_data2 and one for questions and choices frame_selection)
        Frame.__init__(self, *args, **kwargs)

        # variables
        self.listFrame2 = list()
        self.increment = 1
        self.uriLoad = False

        #### two frames: data2 and selection (questions)
        ## data
        self.label_frame_data = tk.LabelFrame(self, text="Excel Data")
        self.label_frame_data.pack(side="left", padx=2, pady=2,fill="both", expand="yes")
        self.label_frame_selection = tk.LabelFrame(self, text="Selection", width = "400")
        self.label_frame_selection.pack(side="left", padx=2, pady=2, fill="y")

        #frame result
        self.frameDf = tk.LabelFrame(self.label_frame_data, text='df resultat')
        self.tvResult = ttk.Treeview(self.frameDf)
        treescrolly = tk.Scrollbar(self.tvResult, orient="vertical",
                                   command=self.tvResult.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(self.tvResult, orient="horizontal",
                                   command=self.tvResult.xview)  # command means update the xaxis view of the widget
        self.tvResult.configure(xscrollcommand=treescrollx.set,
                                yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget


        ##questions
        self.frame_questions = tk.LabelFrame(self.label_frame_selection, text="Questions")
        self.frame_questions.pack(expand="no", fill="x",padx = 5)

        self.listDf = list()
        self.numberOfDf = 0
        self.df = None



    def show(self):
        self.lift()


    def load_uri(self, p1):
        # Create the dataFrames
        #print(label_file["text"])
        api = MtabAnnotationApi(p1.label_file["text"])
        api.extractTableHTML()

        cea = api.getList_CEA_Global()
        #print("CEA")
        #print(cea)

        cpa = api.getList_CPA_Global()
        #print("CPA")
        #print(cpa)

        global cta
        cta = api.getList_CTA_Global()
        #print("CTA")
        # Pour chaque CTA, le premier index est nul. Je l'ai enlevé dans le for juste en dessous.
        #print(cta)

        self.numberOfDf = len(cpa)
        listDictDf = list()

        for frame in self.listFrame2:
            frame.destroy()
        self.listFrame2 = list()

        #file_path = label_file["text"]
        i = 0
        for i in range(0, self.numberOfDf, 1):
            self.df = pd.DataFrame(data=cea[i],
                              columns=cpa[i],
                              dtype=str)
            #Supprime la premiere ligne du fichier en ajustant les indexes
            self.df = self.df.reindex(self.df.index.drop(0)).reset_index(drop=True)
            cta[i].pop(0)
            listCol = self.df.columns.values.tolist()
            #Supprime les colonnes qui n'ont pas été trouvées par Mtab
            if "" in listCol:
                self.df.drop(labels=[""], axis=1, inplace=True)
            #Supprime les colonnes dupliquées
            self.df = self.df.loc[:, ~self.df.columns.duplicated()]
            #Affiche le tableau
            #print(tabulate(self.df, headers='keys', tablefmt='psql'))
            self.listDf.append(self.df)
            j = 0
            dictDf = dict()
            for j in range(0, len(cpa[i]), 1):
                dictDf[tuple(cta[i][j])] = cpa[i][j]
            listDictDf.append(dictDf)

            ##--------------------------------------------Afficher dataFrames-------------------------------------------------------------------------
            self.listFrame2.append(tk.LabelFrame(self.label_frame_data, text='df'))
            self.listFrame2[i].pack(fill="both",expand="yes", pady = 10, padx = 10)


            tvI = ttk.Treeview(self.listFrame2[i])
            tvI.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

            treescrolly = tk.Scrollbar(self.listFrame2[i], orient="vertical",
                                       command=tvI.yview)  # command means update the yaxis view of the widget
            treescrollx = tk.Scrollbar(self.listFrame2[i], orient="horizontal",
                                       command=tvI.xview)  # command means update the xaxis view of the widget
            tvI.configure(xscrollcommand=treescrollx.set,
                          yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
            treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
            treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
            tvI["column"] = list(self.df.columns)
            tvI["show"] = "headings"

            for column in tvI["columns"]:
                tvI.heading(column, text=column)  # let the column heading = column name
                df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists

            for row in df_rows:
                tvI.insert("", "end",
                            values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

        self.uriLoad = True
        self.ask_question()
        self.show()

    def ask_question(self):
        if self.uriLoad  == True:
            common_element = set(cta[0][0]).intersection(cta[self.increment][0])
            frame_text = "CTA from the first Dataset :" + str(cta[0][0]) + "\n" + "CTA from the second Dataset :" + str(cta[self.increment][0]) + "\n" + "Voici les éléments en communs :" + str(common_element)

            self.frame_questions = tk.LabelFrame(self.label_frame_selection, text="Questions")
            self.frame_questions.pack(expand="no", fill="x",padx = 5)

            self.label_cta = ttk.Label(self.frame_questions, text= frame_text, wraplengt=750)
            self.label_cta.pack(padx = 5,fill="none",expand="false")

            #print(frame_text)
            #print(cta[0][0])
            #print(cta[self.increment][0])
            #print("Voici les éléments en communs :" + str(common_element))

            if len(common_element) == len(cta[0][0]):
                text_label_Q1="Tous les types de la liste sujet se retrouvent dans la liste cible. Nous suggérons donc de choisir le premier choix d'intégration de dataset."
            elif len(common_element) > 0:
                text_label_Q1="Tous les types de la liste sujet ne se retrouvent pas dans la liste cible. Nous suggérons donc de choisir le deuxième choix d'intégration de dataset."
            else:
                text_label_Q1="Aucun type n'est retrouvé dans la liste cible. Le deuxième choix d'intégration sera utilisé."

            self.label_Q1 = ttk.Label(self.frame_questions, text= text_label_Q1, wraplengt=750)
            self.label_Q1.pack(padx = 5,fill="none",expand="false")

            self.label_rep_Q1 = ttk.Label(self.frame_questions, text="Pour choisir le premier choix taper 1 sinon taper 2:", wraplengt=750)
            self.label_rep_Q1.pack(padx = 5,fill="none",expand="false")
            self.textBox_rep_Q1 = ttk.Entry(self.frame_questions)
            self.textBox_rep_Q1.pack(padx = 5,fill="none",expand="false")
            self.button_Q1_OK = tk.Button(self.frame_questions, text='OK', command=lambda:self.question_2())
            self.button_Q1_OK.pack(padx = 5,fill="none",expand="false")

    def refreshTvResult(self):
        self.tvResult["column"] = list(self.df.columns)
        self.tvResult["show"] = "headings"

        incrementRVE = 0
        for column in self.tvResult["columns"]:
            incrementRVE += 1
            self.tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = self.df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                self.tvResult.insert("", "end",
                                     values=row)
        # RVE
        for i in range(incrementRVE):
            self.tvResult.column('#' + str(i), minwidth=300, stretch=0)
            #tvResult.heading(i, text="Column {}".format(i))
            self.tvResult.column('#0', stretch=0)


    def question_2(self):
        choice = self.textBox_rep_Q1.get()
        df1 = self.listDf[0]
        df2 = self.listDf[self.increment]
        self.df = self.listDf[0]
        frameProposition = None
        if choice == "1":
            df1.to_excel(r'Premier Dataset Tour'+str(self.increment)+'.xlsx', index=False)
            df2.to_excel(r'Deuxième Dataset Tour'+str(self.increment)+'.xlsx', index=False)

            self.df = pd.merge(df1,df2)
            #Evite les doublons dans le tableau final pour l'étape append
            df1 = df1[~df1.isin(self.df)].dropna()
            df2 = df2[~df2.isin(self.df)].dropna()

            self.df = self.df.append(df1, ignore_index=True, sort=False)
            self.df = self.df.append(df2, ignore_index=True, sort=False)

            #df = df.drop_duplicates(subset=['Core Attribute'], keep='first')
            self.df.to_excel(r'Première Question Tour'+str(self.increment)+'.xlsx', index=False)

            #print(tabulate(df, headers='keys', tablefmt='psql'))

            self.frameDf.pack(fill="both",expand="yes", pady = 10, padx = 10)
            self.tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)

            self.refreshTvResult()

        elif choice == "2":
            rowCountDf1 = len(df1.index)
            rowCountDf2 = len(df2.index)
            headerSubjectTable1 = df1.columns.values[0]
            #Skip the first column "Core attribute"
            headers = list(df2.columns.values)[1:]
            # Si on retrouve des dbo qui sont en lien avec notre dbr alors on en ressort des +
            listSubjectOntology = list()
            # Liste contenant les propositions de colonnes. JE SUIS ICI. FAIRE UNE CONDITION POUR N AJOUTER QUE DES VALEURS UNIQUES.
            listProposition = list()
            #REPASSER A 0
            i = 0
            while i < rowCountDf1:
                for item in headers:
                    #print("headerSubjectTable1")
                    #print(headerSubjectTable1)
                    dbrSubject = df1.at[i, headerSubjectTable1]
                    #print(dbrSubject+" "+item)
                    queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
                    #print(queryString)
                    try:
                        results1 = utils.executeSparqlQuery(queryString)
                    except HTTPError:
                        print("Problème Http dbpedia veuillez ressayer plus tard.")
                    if results1["results"]["bindings"]:
                        listSubjectOntology.append(item)
                        resultInserCol = utils.insertColumnDf(listProposition, item,df1.columns.values)
                        #print("Liste proposition :")
                        #print(listProposition)
                        if resultInserCol:
                            listProposition.append(resultInserCol)
                i = i + 1

            # Avec ça, on enlève les colonnes qui ont été insérées dans le df via le insert columnDf en haut.
            headers = set(headers) - set(listSubjectOntology)
            i = 0
            # S'il y a encore des colonnes dans le headers, ca veut dire que toutes les colonnes vont faire une sorte de produit cartésien. On va prendre chaque cellule de la colonne sujet du df1 et voir si elle a un lien avec les cellules du df2. La perf est de n^4 pas terrible! Peut être moyen de descendre à n^3 mais je ne pense pas.
            if headers:
                while i < rowCountDf1:
                    j = 0
                    while j < rowCountDf2:
                        for item in headers:
                            dbrSubject = df1.at[i, headerSubjectTable1]
                            dbrSubject1 = df2.at[j, item]
                            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select distinct ?predicate where { \n { <" + dbrSubject + "> ?predicate <" + dbrSubject1 + ">} \n}"
                            #print(queryString)
                            try:
                                results1 = utils.executeSparqlQuery(queryString)
                            except HTTPError:
                                print("Problème Http avec dbpedia veuillez ressayer plus tard.")
                            for result in results1["results"]["bindings"]:
                                predicate = result["predicate"]["value"]
                                if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                                    # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                                    print("InsertCol2")
                                    resultInserCol = utils.insertColumnDf(listProposition, predicate,df1.columns.values)
                                    print("Fin InsertCol2")
                                    if resultInserCol:
                                        listProposition.append(resultInserCol)
                        j = j + 1
                    i = i + 1
            self.df = df1
            #df = df.drop_duplicates(subset=['Core Attribute'], keep='first')
            self.df.to_excel(r'Première Question Tour'+str(self.increment)+'.xlsx', index=False)

            #print(tabulate(df, headers='keys', tablefmt='psql'))
           #if self.frameDf != None:
           #    self.frameDf.destroy()

            self.refreshTvResult()

            frameProposition = askQuestion1(listProposition)
            self.df.to_excel(r'Première Question Tour'+str(i)+'.xlsx', index=False)

        button_Q_SelectProposition = tk.Button(self.label_frame_selection, text='Questions', command=lambda:self.algo_question2_begin(button_Q_SelectProposition,frameProposition))
        button_Q_SelectProposition.pack()


    def algo_question2_begin(self,button_Q_SelectProposition,frameProposition):
        #print("Question 2")
        button_Q_SelectProposition.destroy()
        if frameProposition != None:
            frameProposition[0].destroy()
            frameProposition[1].destroy()

        label_Add_Column = ttk.Label(self.frame_questions, text="Si vous avez une autre colonne à ajouter ecrivez le. Exemple : birthPlace. Si vous n'en avez plus, écrivez -1:", wraplengt=750)
        label_Add_Column.pack(padx = 5,fill="none",expand="false", side = "top")
        textBox_rep_Q2 = ttk.Entry(self.frame_questions)
        textBox_rep_Q2.pack(padx = 5,fill="none",expand="false")

        #Show la liste de proposition
        frameListProposition = tk.LabelFrame(self.label_frame_selection, text='Liste proposition')
        frameListProposition.pack(padx = 5,expand="false", fill="x")

        tvI = ttk.Treeview(frameListProposition)
        tvI.pack(padx = 5,fill="x",expand="false")

        treescrolly = tk.Scrollbar(frameListProposition, orient="vertical",
                                   command=tvI.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(frameListProposition, orient="horizontal",
                                   command=tvI.xview)  # command means update the xaxis view of the widget
        tvI.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        button_Q2_Proposition = tk.Button(self.frame_questions, text='Choisir', command=lambda:self.algo_question2(textBox_rep_Q2,tvI))
        button_Q2_Proposition.pack(padx = 5,fill="none",expand="false")

        #Show button selection
        button_Q2_SelectProposition = tk.Button(self.label_frame_selection, text='Ajouter', command=lambda:self.algo_question_proposition(tvI))
        button_Q2_SelectProposition.pack()




    def algo_question2(self,textBox_rep_Q2,tvI):
        listProposition = list()
        newColumn = str(textBox_rep_Q2.get())
        if(newColumn == "-1"):
            return
        queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n SELECT ?predicate \nWHERE {\n?predicate a rdf:Property\nFILTER ( REGEX ( STR (?predicate), \"http://dbpedia.org/ontology/\", \"i\" ) )\nFILTER ( REGEX ( STR (?predicate), \"" + newColumn + "\", \"i\" ) )\n}\nORDER BY ?predicate"
        # print(queryString)
        try:
            results1 = utils.executeSparqlQuery(queryString)
        except HTTPError:
            print("Problème Http dbpedia veuillez ressayer plus tard.")
        for result in results1["results"]["bindings"]:
            predicate = result["predicate"]["value"]
            print("predicate: "+predicate)
            if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                resultInserCol = utils.insertColumnDf(listProposition, predicate,self.df.columns.values)
                if resultInserCol and resultInserCol not in listProposition and resultInserCol not in self.df.columns.values:
                    listProposition.append(resultInserCol)

        #print(listProposition)

        tvI["column"] = ["Propositions"]
        tvI["show"] = "headings"

        for record in tvI.get_children():
            tvI.delete(record)

        for column in tvI["columns"]:
            tvI.heading(column, text=column)  # let the column heading = column name
            df_rows = listProposition  # turns the dataframe into a list of lists

        for row in df_rows:
            tvI.insert("", "end",values=row)


    def algo_question_proposition(self,tvI):
        #get items from proposition's list
        for item in tvI.selection():
            columnAdd = tvI.item(item,"values")
            columnAdd = str(columnAdd)
            if(columnAdd.startswith("(")):
                columnAdd = columnAdd[2:]
                columnAdd = columnAdd[:-3]
            print(columnAdd)
            self.df[columnAdd] = 'nan'

        self.df.to_excel(r'Deuxième Question Tour'+str(self.increment)+'.xlsx', index=False)

        #### refresh df resultat
        self.refreshTvResult()


    def askQuestion3(self,tvI_Q2,frameDfQ2,button_Q2_Proposition,button_Q2_SelectProposition,button_Q2_EndProposition,label_Add_Column,textBox_rep_Q2):
        #DESTUCTION DES OBJETS. Il faudrait peut etre pas detruire label_Add_Column mais plutot changer son text.
        #label_frame_selection.destroy()
        tvI_Q2.destroy()
        frameDfQ2.destroy()
        button_Q2_Proposition.destroy()
        button_Q2_SelectProposition.destroy()
        button_Q2_EndProposition.destroy()
        label_Add_Column.destroy()
        textBox_rep_Q2.destroy()
        #
        label_Add_Column_Q3 = ttk.Label(self.frame_questions, text="Ce que vous cherchez n'a toujours pas été trouvé? Veuillez insérer l'URI de la colonne souhaitée. Exemple : http://dbpedia.org/ontology/deathDate", wraplengt=750)
        label_Add_Column_Q3.pack(padx = 5,fill="none",expand="false", side = "top")
        textBox_rep_Q3 = ttk.Entry(self.frame_questions)
        textBox_rep_Q3.pack(padx = 5,fill="none",expand="false")
        button_Q3_SelectProposition = tk.Button(self.frame_questions, text='Ajouter', command=lambda:self.algo_question3_proposition(str(textBox_rep_Q3.get())))
        button_Q3_SelectProposition.pack()
        button_Q3_SelectProposition = tk.Button(self.frame_questions, text='Terminer', command=lambda:show_df_result())
        button_Q3_SelectProposition.pack()



    def algo_question3_proposition(self,textQ3):
        newColumn = textQ3.strip()
        global listPropositionQ3
        try:
            request = "" #requests.get(newColumn)
        except ConnectionError:
            print('Le lien n existe pas')
        except MissingSchema:
            print('Le lien n existe pas')
        else:
            #print('Le lien existe')
            if newColumn and newColumn not in listPropositionQ3 and newColumn not in self.df.columns.values:
                self.df[newColumn] = 'nan'
                listPropositionQ3.append(newColumn)
                #df[newColumn] = np.nan
                #df[newColumn] = df[newColumn].astype('string')
                #printDf(df)
            else:
                print("La colonne existe déjà dans le DF")

        self.refreshTvResult()