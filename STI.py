from DataIntoDF import DataInfoDF
from tabulate import tabulate
import pandas as pd
import numpy as np
# Code SPARQL vient de : https://stackoverflow.com/questions/58519010/constructing-graph-using-rdflib-for-the-outputs-from-sparql-select-query-with
from SPARQLWrapper import SPARQLWrapper, JSON
import pathlib


def printDf(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))
    # df.to_csv(r'File Name.csv',index=False)
    df.to_excel(r'File Name.xlsx', index=False)

def cleanLastDigit(item):
    # Ici je récupère la cellule de la colonne pour l'ontologie qui m'intéresse je remove un chiffre s'il y a en a un à la fin.
    itemOntology = item
    if (item[-1].isdigit()):
        itemOntology = item[:-1]
    # print(itemOntology)
    return itemOntology


def executeSparqlQuery(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

# Va permettre d'insérer dans la colonne du dataframe, le resultat de la query SPARQL ici en fonction du cas passé en argument, on vérifie son rdf type ou pas.
def insertDataDf(df, results, i, key, item):
    if key is not None:
        itemOntology = cleanLastDigit(key)
        objectFilter = itemOntology.split(" ")
        stringFilter = ""

        # Ici on récupère toutes les ontologies de la colonne une par une.
        for object in objectFilter:
            stringFilter += "?object = <" + object + "> ||\n"
        stringFilter = stringFilter[:-3]

        for result in results["results"]["bindings"]:
            predicate = result["object"]["value"]
            # print(item)
            # print(predicate)

            # Cette query va permettre de vérifier que l'entité qu'on va insérer dans le tableau possède dans son rdf type, les différentes ontologies de la colonne.
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + predicate + "> rdf:type ?object } \n FILTER (" + stringFilter + ")\n}"
            #print(queryString)
            resultsFilter = executeSparqlQuery(queryString)
            # print("FILTER")
            #print(queryString)
            if resultsFilter["results"]["bindings"]:
                # Faire disparaitre la valeur NaN avec fillna() mais pas réussi. df.fillna('') -> A AMELIORER! Créer une fonction c'est presque le meme code qu'en bas, sauf que le replace se fait sur le nan et le replace d'en dessous sur <NA>
                if len(str(df.at[i, item])) == 3:
                    df.at[i, item] = str(df.at[i, item]).replace("nan", "")
                df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "
    else:
        for result in results["results"]["bindings"]:
            predicate = result["object"]["value"]
            if len(str(df.at[i, item])) == 4:
                df.at[i, item] = str(df.at[i, item]).replace("<NA>", "")
            df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "


def insertColumnDf(df,column):
    if column not in df:
        df[column] = np.nan
    df[column] = df[column].astype('string')




# -----------------------------------------------------------------
#                           MAIN
# -----------------------------------------------------------------


# Create the dataFrames
path = str(pathlib.Path().absolute())
dataInfoDF = DataInfoDF(path+'/.idea/files/annotations_CEA_12_05_2021(3).csv', path+'/.idea/files/cpa(3).csv')

df1 = dataInfoDF.runTab1()
dictDf1 = dataInfoDF.getOntologiesDictTable().copy()
df2 = dataInfoDF.runTab2()
dictDf2 = dataInfoDF.getOntologiesDictTable().copy()

#print("Df1 dict")
#print(dictDf1)
#print("Df2 dict")
#print(dictDf2)

print("DataFrame 1")
print(tabulate(df1, headers='keys', tablefmt='psql'))
print("DataFrame 2")
print(tabulate(df2, headers='keys', tablefmt='psql'))

# Permet de retrouver tous les noms des colonnes/ontologies.
ontologies1 = dataInfoDF.getOntologiesTable1()
ontologies2 = dataInfoDF.getOntologiesTable2()


# Boolean qui permet de savoir si la colonne sujet trouve une correspondance avec une colonne du deuxième dataset.
isSameColumn = False

# Premier cas, lorsque la colonne sujet match une colonne du deuxième dataset! Comme pour la classe DataInfoDF j'estime que la colonne sujet est la numéro 0. Trouver un moyen de récupérer la classe sujet de l'outil.
for ontology in ontologies2:
    if ontologies1[0] == ontology:
        isSameColumn = True
        break

# if(isSameColumn) -> Performance n^3 -> Dans le mémoire faudra en parler commme une faiblesse ou comme force, n^3 ca reste correcte !
# else -> Performance ? Encore à tester!
if (isSameColumn):
    # Je mélange les deux datasets avec le append
    df = df1.append(df2, ignore_index=True, sort=False)
    dictDf = dictDf1 | dictDf2
    # print the list of all the column headers
    # print("The column headers :")
    headers = list(df.columns.values)
    # print(headers)
    i = 0
    rowCount = len(df.index)
    headers = list(df.columns.values)
    # STI du premier cas.
    while i < rowCount:
        for key, item in dictDf.items():
            # Si l'item est null il faut le remplir.
            if item and pd.isnull(df.at[i, item]):
                # Ici je récupère la cellule de la colonne sujet.
                dbrSubject = df.at[i, headers[0]]
                #print("ITEM: "+item)
                queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
                #print(queryString)
                results1 = executeSparqlQuery(queryString)
                # J'écris les résultats trouvé grâce à la query au dessus.
                insertDataDf(df, results1, i, key, item)
        i = i + 1
    print("DataFrame Final")

    # Clean les headers qui ont un chiffre à la fin.
    #for item in headers:
    #    if (item[-1].isdigit()):
    #        df.rename(columns={item: item[:-1]}, inplace=True)
    printDf(df)
else:
    rowCountDf1 = len(df1.index)
    rowCountDf2 = len(df2.index)
    headerSubjectTable1 = df1.columns.values[0]
    headers = list(df2.columns.values)
    #Si on retrouve des dbo qui sont en lien avec notre dbr alors on en ressort des +
    listSubjectOntology = list()
    i = 0
    while i < rowCountDf1:
        for item in headers:
            dbrSubject = df1.at[i, headerSubjectTable1]
            queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
            results1 = executeSparqlQuery(queryString)
            if results1["results"]["bindings"]:
                listSubjectOntology.append(item)
                insertColumnDf(df1,item)
        i = i+1

    #Avec ça, on enlève les colonnes qui ont été insérées dans le df via le insert columnDf en haut.
    headers = set(headers) - set(listSubjectOntology)
    i = 0
    j = 0
    #S'il y a encore des colonnes dans le headers, ca veut dire que toutes les colOn va faire une sorte de produit cartésien. On va prendre chaque cellule de la colonne sujet du df1 et voir si elle a un lien avec les cellules du df2. La perf est de n^4 pas terrible! Peut être moyen de descendre à n^3 mais je ne pense pas.
    if headers:
        while i < rowCountDf1:
            while j < rowCountDf2:
                for item in headers:
                    dbrSubject = df1.at[i, headerSubjectTable1]
                    dbrSubject1 = df2.at[j, item]
                    queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select distinct ?predicate where { \n { <" + dbrSubject + "> ?predicate <" + dbrSubject1 + ">} \n}"
                    #print(queryString)
                    results1 = executeSparqlQuery(queryString)
                    for result in results1["results"]["bindings"]:
                        predicate = result["predicate"]["value"]
                        if predicate != "http://dbpedia.org/ontology/wikiPageWikiLink":
                            insertColumnDf(df1,predicate)
                j = j+1
            i = i+1

    #Insert values.
    i = 0
    rowCount = len(df1.index)
    headers = list(df1.columns.values)
    # STI du deuxième cas. Très similaire sauf qu'on ne boucle pas sur la meme chose. Ici on boucle sur les colonnes du df. Dans le premier cas c'est via le dictionnaire. -> A améliorer. Créer une méthode pour éviter d'avoir 2 fois le meme code.
    while i < rowCount:
        for item in headers:
            # Si l'item est null il faut le remplir. -> Faudrait changer le if. Ici le nan est en string via la fonction insertColumnDf il faudrait éviter de la mettre en string.
            if  pd.isnull(df1.at[i, item]):
                # Ici je récupère la cellule de la colonne sujet.
                dbrSubject = df1.at[i, headers[0]]
                queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
                #print(queryString)
                results1 = executeSparqlQuery(queryString)
                # J'écris les résultats trouvés grâce à la query au dessus.
                insertDataDf(df1, results1, i,None, item)
        i = i + 1
    print("DataFrame Final")
    printDf(df1)
