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

#----------------------------BEGIN FUNCTION INTEGRATION--------------------------------------------------------------------------------------
def executeSparqlQuery(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def insertColumnDf(listProposition, column,columnValues):
    index = column.rfind('/')
    tmpColumn = column[index + 1:]
    listColumnName = list()

    for columnValue in columnValues:
        columnValue = str(columnValue)
        index = columnValue.rfind('/')
        tmpcolumnValue = columnValue[index + 1:]
        listColumnName.append(tmpcolumnValue)

    listColumnNameProposition = list()
    for proposition in listProposition:
        index = proposition.rfind('/')
        tmpproposition = proposition[index + 1:]
        listColumnNameProposition.append(tmpproposition)
    if tmpColumn not in listColumnNameProposition and tmpColumn not in listColumnName:
        return column

def insertDataDf(df, results, i, item):
    for result in results["results"]["bindings"]:
        predicate = result["object"]["value"]
        #print(predicate)
        if len(str(df.at[i, item])) == 4:
            df.at[i, item] = str(df.at[i, item]).replace("<NA>", "")
        elif len(str(df.at[i, item])) == 3:
            df.at[i, item] = str(df.at[i, item]).replace("nan", "")
            # print(df.at[i, item])
            # print(len(str(df.at[i, item])))
        df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "
    return df

def printDf(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))
    df.to_csv(r'Final Dataset.csv',index=False)
    df.to_excel(r'Final Dataset.xlsx', index=False)
#-------------------------------------------------------END FUNCTION INTEGRATION-------------------------------------------------------------

#bool URI loaded
uriLoad = False
listDf = list()
listDictDf = list()
cta = list()
increment = 1
listPropositionQ3 = list()
listTvi = list()


#variables
isDebug = 0
file_path_absolute = os.path.dirname(__file__)
file_path_debug = os.path.join(file_path_absolute, ".idea\\files\\case_test")
listFrame1 = list()
listFrame2 = list()
file_path = ""

# initalise the tkinter GUI
root = tk.Tk()
root.geometry("500x600")  # set the root dimensions

##### container = root contains two pages
container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)

##### Frame data (first page)
frame_pageOne = Frame(root)
#frame_pageOne.pack(fill="both", expand="yes")
label_frame_data = tk.LabelFrame(frame_pageOne, text="Excel Data")
label_frame_data.pack(fill="both",expand="yes")

# Frame data : options
Label_options = tk.LabelFrame(frame_pageOne, text="Options")
Label_options.pack(fill="both", pady=20, padx = 10, side='left')
label_file = tk.Label(Label_options, text="No File Selected")
label_file.pack(pady = 20)

# Frame data : Buttons
button1 = tk.Button(Label_options, text="Browse A Folder", command=lambda: File_dialog())
button1.pack(side='left', padx = 5)

button2 = tk.Button(Label_options, text="Load Files", command=lambda: Load_excel_data())
button2.pack(side='left', padx = 5)

#if path is empty disable button LoadFiles
if(file_path == ""):
    button2["state"] = "disable"

button3 = tk.Button(Label_options, text="Load URI", state="disable", command=lambda: load_uri(frame_pageTwo))
button3.pack(side='left', padx = 5)

button5 = tk.Button(Label_options, text='Next Page', command=lambda:raise_frame(frame_pageTwo))
button5.pack(side='left', padx = 5)


######Frame pagetwo  : two container one for result (frame_data2 and one for questions and choices frame_selection)
frame_pageTwo = Frame(root)
#frame_pageTwo.pack(fill="both", expand="yes")

## two frames
label_frame_data2 = tk.LabelFrame(frame_pageTwo, text="Excel Data")
label_frame_data2.pack(side="left", padx=2, pady=2,fill="both", expand="yes")
label_frame_selection = tk.LabelFrame(frame_pageTwo, text="Selection", width = "400")
label_frame_selection.pack(side="left", padx=2, pady=2, fill="y")

frame_questions = tk.LabelFrame(label_frame_selection, text="Questions")
frame_questions.pack(expand="no", fill="x",padx = 5)


#Boutton pour revenir a la page précédente.
button4 = tk.Button(frame_pageTwo, text='Previous page', command=lambda:raise_frame(frame_pageOne))
button4.pack(side='bottom', padx = 5)



##### Frame question 3 (third page)
frame_pageThree = Frame(root)
frame_pageThree.pack(fill="both", expand="yes")



frame_pageOne.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
frame_pageTwo.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
frame_pageThree.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    """filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select A File",
                                              filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))"""
    krepertoire = filedialog.askdirectory(title="Sélectionnez un répertoire de destination ...", mustexist=True)
    label_file["text"] = krepertoire

    #active buttons loadUri and loadFiles
    button2["state"] = "normal"
    button3["state"] = "normal"

    return None

def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    directory = os.fsencode(label_file["text"])
    #Changer l'init ici il faut transformer listFrame en variable globale.
    global listFrame1
    for frame in listFrame1:
        frame.destroy()
    listFrame1 = list()

    i = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        listFrame1.append(tk.LabelFrame(label_frame_data, text=filename))
        listFrame1[i].pack(fill="both",expand="yes", pady = 10, padx = 10)

        global file_path
        file_path = label_file["text"]+"/"+filename

        if file_path.endswith(".csv"):
            try:
                excel_filename = r"{}".format(file_path)
                if excel_filename[-4:] == ".csv":
                    df = pd.read_csv(excel_filename)
                else:
                    df = pd.read_excel(excel_filename)

            except ValueError:
                tk.messagebox.showerror("Information", "The file you have chosen is invalid")
                return None
            except FileNotFoundError:
                tk.messagebox.showerror("Information", f"No such file as {file_path}")
                return None

        tvI = ttk.Treeview(listFrame1[i])
        tvI.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(listFrame1[i], orient="vertical",
                                   command=tvI.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(listFrame1[i], orient="horizontal",
                                   command=tvI.xview)  # command means update the xaxis view of the widget
        tvI.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
        tvI["column"] = list(df.columns)
        tvI["show"] = "headings"

        #columns
        for column in tvI["columns"]:
            tvI.heading(column, text=column)  # let the column heading = column name

        #rows
        df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
        for row in df_rows:
            tvI.insert("", "end", values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        i = i +1



    return None

def load_uri(frame):
    #Permet de pas se retrouver avec des propositions qui existe déjà pour la Q3
    global listPropositionQ3
    listPropositionQ3 = list()
    # Create the dataFrames
    #print(label_file["text"])
    api = MtabAnnotationApi(label_file["text"])
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

    numberOfDf = len(cpa)
    global listDf
    listDf = list()
    global listDictDf
    listDictDf = list()

    global listFrame2
    for frame in listFrame2:
        frame.destroy()
    listFrame2 = list()

    #file_path = label_file["text"]
    i = 0
    for i in range(0, numberOfDf, 1):
        df = pd.DataFrame(data=cea[i],
                          columns=cpa[i],
                          dtype=str)
        #Supprime la premiere ligne du fichier en ajustant les indexes
        df = df.reindex(df.index.drop(0)).reset_index(drop=True)
        cta[i].pop(0)
        listCol = df.columns.values.tolist()
        #Supprime les colonnes qui n'ont pas été trouvées par Mtab
        if "" in listCol:
            df.drop(labels=[""], axis=1, inplace=True)
        #Supprime les colonnes dupliquées
        df = df.loc[:, ~df.columns.duplicated()]
        #Affiche le tableau
        #print(tabulate(df, headers='keys', tablefmt='psql'))
        listDf.append(df)
        j = 0
        dictDf = dict()
        for j in range(0, len(cpa[i]), 1):
            dictDf[tuple(cta[i][j])] = cpa[i][j]
        listDictDf.append(dictDf)

        ##--------------------------------------------Afficher dataFrames-------------------------------------------------------------------------
        listFrame2.append(tk.LabelFrame(label_frame_data2, text='df'))
        listFrame2[i].pack(fill="both",expand="yes", pady = 10, padx = 10)

        global listTvi
        listTvi.append(ttk.Treeview(listFrame2[i]))
        listTvi[i].place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(listFrame2[i], orient="vertical",
                                   command=listTvi[i].yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(listFrame2[i], orient="horizontal",
                                   command=listTvi[i].xview)  # command means update the xaxis view of the widget
        listTvi[i].configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
        listTvi[i]["column"] = list(df.columns)
        listTvi[i]["show"] = "headings"

        for column in listTvi[i]["columns"]:
            listTvi[i].heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                listTvi[i].insert("", "end",
                           values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    global uriLoad
    uriLoad = True
    frame.tkraise()
    ask_question()

def ask_question():
    global uriLoad
    if uriLoad  == True:
        global increment
        common_element = set(cta[0][0]).intersection(cta[increment][0])
        frame_text = "CTA from the first Dataset :" + str(cta[0][0]) + "\n" + "CTA from the second Dataset :" + str(cta[increment][0]) + "\n" + "Voici les éléments en communs :" + str(common_element)
        label_cta = ttk.Label(frame_questions, text= frame_text, wraplengt=750)
        label_cta.pack(padx = 5,fill="none",expand="false")

        #print(frame_text)
        #print(cta[0][0])
        #print(cta[increment][0])
        #print("Voici les éléments en communs :" + str(common_element))

        if len(common_element) == len(cta[0][0]):
            text_label_Q1="Tous les types de la liste sujet se retrouvent dans la liste cible. Nous suggérons donc de choisir le premier choix d'intégration de dataset."
        elif len(common_element) > 0:
            text_label_Q1="Tous les types de la liste sujet ne se retrouvent pas dans la liste cible. Nous suggérons donc de choisir le deuxième choix d'intégration de dataset."
        else:
            text_label_Q1="Aucun type n'est retrouvé dans la liste cible. Le deuxième choix d'intégration sera utilisé."

        label_Q1 = ttk.Label(frame_questions, text= text_label_Q1, wraplengt=750)
        label_Q1.pack(padx = 5,fill="none",expand="false")

        label_rep_Q1 = ttk.Label(frame_questions, text="Pour choisir le premier choix taper 1 sinon taper 2:", wraplengt=750)
        label_rep_Q1.pack(padx = 5,fill="none",expand="false")
        textBox_rep_Q1 = ttk.Entry(frame_questions)
        textBox_rep_Q1.pack(padx = 5,fill="none",expand="false")
        button_Q1_OK = tk.Button(frame_questions, text='OK', command=lambda:question_2(textBox_rep_Q1))
        button_Q1_OK.pack(padx = 5,fill="none",expand="false")

def askQuestion1(listProposition,tvResult,df):
    frameDf = tk.LabelFrame(label_frame_selection, text='Liste proposition')
    frameDf.pack(padx = 5,expand="false", fill="x")

    tvI = ttk.Treeview(frameDf)
    tvI.pack(padx = 5,fill="x",expand="false")

    treescrolly = tk.Scrollbar(frameDf, orient="vertical",
                               command=tvI.yview)  # command means update the yaxis view of the widget
    treescrollx = tk.Scrollbar(frameDf, orient="horizontal",
                               command=tvI.xview)  # command means update the xaxis view of the widget
    tvI.configure(xscrollcommand=treescrollx.set,
                  yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
    treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

    tvI["column"] = ["Propositions"]
    tvI["show"] = "headings"

    for record in tvI.get_children():
        tvI.delete(record)

    for column in tvI["columns"]:
        tvI.heading(column, text=column)  # let the column heading = column name
        df_rows = listProposition  # turns the dataframe into a list of lists
        for row in df_rows:
            tvI.insert("", "end",values=row)

    button_Q_SelectProposition = tk.Button(label_frame_selection, text='Ajouter', command=lambda:algo_question_proposition(tvI, df, tvResult))
    button_Q_SelectProposition.pack()
    listComponentDestroy = list()
    listComponentDestroy.append(button_Q_SelectProposition)
    listComponentDestroy.append(frameDf)
    return listComponentDestroy

def question_2(textBox_rep_Q1):
    choice = textBox_rep_Q1.get()
    df1 = listDf[0]
    df2 = listDf[increment]
    df = listDf[0]
    if choice == "1":
        df1.to_excel(r'Premier Dataset Tour'+str(increment)+'.xlsx', index=False)
        df2.to_excel(r'Deuxième Dataset Tour'+str(increment)+'.xlsx', index=False)

        df = pd.merge(df1,df2)
        #Evite les doublons dans le tableau final pour l'étape append
        df1 = df1[~df1.isin(df)].dropna()
        df2 = df2[~df2.isin(df)].dropna()

        df = df.append(df1, ignore_index=True, sort=False)
        df = df.append(df2, ignore_index=True, sort=False)

            #df = df.drop_duplicates(subset=['Core Attribute'], keep='first')
        df.to_excel(r'Première Question Tour'+str(increment)+'.xlsx', index=False)

        #print(tabulate(df, headers='keys', tablefmt='psql'))

        frameDf = tk.LabelFrame(label_frame_data2, text='df resultat')
        frameDf.pack(fill="both",expand="yes", pady = 10, padx = 10)

        tvResult = ttk.Treeview(frameDf)
        tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)   # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(tvResult, orient="vertical",
                                   command=tvResult.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(tvResult, orient="horizontal",
                                   command=tvResult.xview)  # command means update the xaxis view of the widget
        tvResult.configure(xscrollcommand=treescrollx.set,
                           yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
        tvResult["column"] = list(df.columns)
        tvResult["show"] = "headings"

        for column in tvResult["columns"]:
            tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                tvResult.insert("", "end",
                                values=row)

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
                    results1 = executeSparqlQuery(queryString)
                except HTTPError:
                    print("Problème Http dbpedia veuillez ressayer plus tard.")
                if results1["results"]["bindings"]:
                    listSubjectOntology.append(item)
                    resultInserCol = insertColumnDf(listProposition, item,df1.columns.values)
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
                            results1 = executeSparqlQuery(queryString)
                        except HTTPError:
                            print("Problème Http avec dbpedia veuillez ressayer plus tard.")
                        for result in results1["results"]["bindings"]:
                            predicate = result["predicate"]["value"]
                            if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                                # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
                                print("InsertCol2")
                                resultInserCol = insertColumnDf(listProposition, predicate,df1.columns.values)
                                print("Fin InsertCol2")
                                if resultInserCol:
                                    listProposition.append(resultInserCol)
                    j = j + 1
                i = i + 1
        df = df1
        #df = df.drop_duplicates(subset=['Core Attribute'], keep='first')
        df.to_excel(r'Première Question Tour'+str(increment)+'.xlsx', index=False)

        #print(tabulate(df, headers='keys', tablefmt='psql'))

        frameDf = tk.LabelFrame(label_frame_data2, text='df resultat')
        frameDf.pack(fill="both",expand="yes", pady = 10, padx = 10)

        tvResult = ttk.Treeview(frameDf)
        tvResult.pack(fill="both",expand="yes", pady = 10, padx = 10)   # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(tvResult, orient="vertical",
                                   command=tvResult.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(tvResult, orient="horizontal",
                                   command=tvResult.xview)  # command means update the xaxis view of the widget
        tvResult.configure(xscrollcommand=treescrollx.set,
                           yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget
        tvResult["column"] = list(df.columns)
        tvResult["show"] = "headings"

        for column in tvResult["columns"]:
            tvResult.heading(column, text=column)  # let the column heading = column name
            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                tvResult.insert("", "end",
                                values=row)
        frameProposition = askQuestion1(listProposition,tvResult,df)
        df.to_excel(r'Première Question Tour'+str(i)+'.xlsx', index=False)

    button_Q_SelectProposition = tk.Button(label_frame_selection, text='Questions', command=lambda:algo_question2_begin(button_Q_SelectProposition,df,tvResult,frameProposition))
    button_Q_SelectProposition.pack()



def algo_question2_begin(button_Q_SelectProposition,df,tvResult,frameProposition):
    #print("Question 2")
    button_Q_SelectProposition.destroy()
    frameProposition[0].destroy()
    frameProposition[1].destroy()

    label_Add_Column = ttk.Label(frame_questions, text="Si vous avez une autre colonne à ajouter ecrivez le. Exemple : birthPlace. Si vous n'en avez plus, écrivez -1:", wraplengt=750)
    label_Add_Column.pack(padx = 5,fill="none",expand="false", side = "top")
    textBox_rep_Q2 = ttk.Entry(frame_questions)
    textBox_rep_Q2.pack(padx = 5,fill="none",expand="false")

    #Show la liste de proposition
    frameDf = tk.LabelFrame(label_frame_selection, text='Liste proposition')
    frameDf.pack(padx = 5,expand="false", fill="x")

    tvI = ttk.Treeview(frameDf)
    tvI.pack(padx = 5,fill="x",expand="false")

    treescrolly = tk.Scrollbar(frameDf, orient="vertical",
                               command=tvI.yview)  # command means update the yaxis view of the widget
    treescrollx = tk.Scrollbar(frameDf, orient="horizontal",
                               command=tvI.xview)  # command means update the xaxis view of the widget
    tvI.configure(xscrollcommand=treescrollx.set,
                  yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
    treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

    button_Q2_Proposition = tk.Button(frame_questions, text='Choisir', command=lambda:algo_question2(textBox_rep_Q2,df,tvI))
    button_Q2_Proposition.pack(padx = 5,fill="none",expand="false")

    #Show button selection
    button_Q2_SelectProposition = tk.Button(label_frame_selection, text='Ajouter', command=lambda:algo_question_proposition(tvI, df, tvResult))
    button_Q2_SelectProposition.pack()
    button_Q2_EndProposition = tk.Button(label_frame_selection, text='Terminer', command=lambda:askQuestion3(df,frameDf,tvI,button_Q2_Proposition,button_Q2_SelectProposition,button_Q2_EndProposition,label_Add_Column,textBox_rep_Q2,tvResult))
    button_Q2_EndProposition.pack()

def algo_question2(textBox_rep_Q2,df,tvI):
    print("algo_question2")
    listProposition = list()
    newColumn = str(textBox_rep_Q2.get())
    print("newColumn: "+newColumn)
    if(newColumn == "-1"):
        return
    queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n SELECT ?predicate \nWHERE {\n?predicate a rdf:Property\nFILTER ( REGEX ( STR (?predicate), \"http://dbpedia.org/ontology/\", \"i\" ) )\nFILTER ( REGEX ( STR (?predicate), \"" + newColumn + "\", \"i\" ) )\n}\nORDER BY ?predicate"
    # print(queryString)
    try:
        results1 = executeSparqlQuery(queryString)
    except HTTPError:
        print("Problème Http dbpedia veuillez ressayer plus tard.")
    for result in results1["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        print("predicate: "+predicate)
        if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
            # Pour l'instant ca va insérer automatiquement la colonne dans le df -> A changer.
            print(df.columns.values)
            resultInserCol = insertColumnDf(listProposition, predicate,df.columns.values)
            if resultInserCol and resultInserCol not in listProposition and resultInserCol not in df.columns.values:
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


def algo_question_proposition(tvI, df, tvResult):
    #get items from proposition's list
    for item in tvI.selection():
        columnAdd = tvI.item(item,"values")
        columnAdd = str(columnAdd)
        if(columnAdd.startswith("(")):
            columnAdd = columnAdd[2:]
            columnAdd = columnAdd[:-3]
        print(columnAdd)
        df[columnAdd] = 'nan'

    df.to_excel(r'Deuxième Question Tour'+str(increment)+'.xlsx', index=False)

    #### refresh df resultat
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



def askQuestion3(df,tvI_Q2,frameDfQ2,button_Q2_Proposition,button_Q2_SelectProposition,button_Q2_EndProposition,label_Add_Column,textBox_rep_Q2,tvResult):
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
    label_Add_Column_Q3 = ttk.Label(frame_questions, text="Ce que vous cherchez n'a toujours pas été trouvé? Veuillez insérer l'URI de la colonne souhaitée. Exemple : http://dbpedia.org/ontology/deathDate", wraplengt=750)
    label_Add_Column_Q3.pack(padx = 5,fill="none",expand="false", side = "top")
    textBox_rep_Q3 = ttk.Entry(frame_questions)
    textBox_rep_Q3.pack(padx = 5,fill="none",expand="false")
    button_Q3_SelectProposition = tk.Button(frame_questions, text='Ajouter', command=lambda:algo_question3_proposition(df, str(textBox_rep_Q3.get()),tvResult))
    button_Q3_SelectProposition.pack()
    button_Q3_SelectProposition = tk.Button(frame_questions, text='Terminer', command=lambda:show_df_result(df,tvResult))
    button_Q3_SelectProposition.pack()

def algo_question3_proposition(df,textQ3,tvResult):
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
        if newColumn and newColumn not in listPropositionQ3 and newColumn not in df.columns.values:
            df[newColumn] = 'nan'
            listPropositionQ3.append(newColumn)
            #df[newColumn] = np.nan
            #df[newColumn] = df[newColumn].astype('string')
            #printDf(df)
        else:
            print("La colonne existe déjà dans le DF")

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

def show_df_result(df,tvResult):
    rowCount = len(df.index)
    headers = list(df.columns.values)
    i = 0
    # STI du deuxième cas. Très similaire sauf qu'on ne boucle pas sur la meme chose. Ici on boucle sur les colonnes du df. Dans le premier cas c'est via le dictionnaire. -> A améliorer. Créer une méthode pour éviter d'avoir 2 fois le meme code.
    while i < rowCount:
        for item in headers:
            # Si l'item est null il faut le remplir. -> Faudrait changer le if. Ici le nan est en string via la fonction insertColumnDf il faudrait éviter de la mettre en string.
            if pd.isnull(df.at[i, item]) or df.at[i, item] == 'nan':
                # Ici je récupère la cellule de la colonne sujet.
                dbrSubject = df.at[i, headers[0]]
                queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + str(dbrSubject) + "> <" + str(item) + "> ?object } \n}"
                print(queryString)
                try:
                    results1 = executeSparqlQuery(queryString)
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

def raise_frame(frame):
    frame.tkraise()


raise_frame(frame_pageOne)

if(isDebug == 1) :
    print("DEBUG MODE")
    file_path = file_path_debug
    label_file["text"] = file_path_debug

    #Charge excel from file path debug
    Load_excel_data()
    #Load uri
    load_uri(label_frame_data2)
    #Next Page
    raise_frame(frame_pageTwo)

root.mainloop()





