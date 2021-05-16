from DataIntoDF import DataInfoDF
from collections import Counter
from tabulate import tabulate
import pandas as pd
# Code SPARQL vient de : https://stackoverflow.com/questions/58519010/constructing-graph-using-rdflib-for-the-outputs-from-sparql-select-query-with
from SPARQLWrapper import SPARQLWrapper, JSON


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


# Va permettre d'insérer dans la colonne du dataframe, le resultat de la query SPARQL
def insertDataDf(df, results, i, item):
    itemOntology = cleanLastDigit(item)
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
        queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> rdf:type ?object } \n FILTER (" + stringFilter + ")\n}"
        resultsFilter = executeSparqlQuery(queryString)

        # print("FILTER")
        # print(queryString)
        if resultsFilter:

            # Faire disparaitre la valeur NaN avec fillna() mais pas réussi. df.fillna('') -> A AMELIORER!
            if len(str(df.at[i, item])) == 3:
                df.at[i, item] = str(df.at[i, item]).replace("nan", "")

            df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "

# -----------------------------------------------------------------
#                           MAIN
# -----------------------------------------------------------------


# Create the dataFrames
dataInfoDF = DataInfoDF('annotations_CEA_12_05_2021(1).csv', 'cpa.csv')

df1 = dataInfoDF.runTab1()
df2 = dataInfoDF.runTab2()

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

    # print the list of all the column headers
    # print("The column headers :")
    headers = list(df.columns.values)
    # print(headers)
    i = 0
    rowCount = len(df.index)
    headers = list(df.columns.values)
    # STI du premier cas.
    while i < rowCount:
        #print("HEADERS")
        #print(headers)
        for item in headers:
            # print(item)
            # Si l'item est null il faut le remplir.
            if pd.isnull(df.at[i, item]):
                # Ici je récupère la cellule de la colonne sujet.
                dbrSubject = df.at[i, headers[0]]
                queryString = "PREFIX dbr:  <http://dbpedia.org/resource/> \n select ?object where { \n { <" + dbrSubject + "> <" + item + "> ?object } \n}"
                # print(queryString)
                results1 = executeSparqlQuery(queryString)
                # J'écris les résultats trouvé grâce à la query au dessus.
                insertDataDf(df, results1, i, item)
        i = i + 1
    print("DataFrame Final")

    # Clean les headers qui ont un chiffre à la fin.
    for item in headers:
        if (item[-1].isdigit()):
            df.rename(columns={item: item[:-1]}, inplace=True)
    printDf(df)
else:
    print("test")
