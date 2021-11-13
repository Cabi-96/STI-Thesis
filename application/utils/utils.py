#Algo Integration
import pathlib

from tabulate import tabulate
from SPARQLWrapper import SPARQLWrapper, JSON


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

def writeHtmlFile(df):
    rowCountDf = len(df.index)
    columnCountDf = len(df.columns)
    headers = list(df.columns.values)

    j = 0
    grapheFileColumn = "{\n "+'  "nodes":[\n'
    grapheFileValues = ""
    grapheFileLinks = ""
    grapheFileLinksColumn = ""
    grapheFileLinksValues = ""
    countTot = columnCountDf + columnCountDf + 1
    countLast = countTot + columnCountDf
    for item in headers:
        i = 0
        print(item)
        grapheFileColumn +=  "{"+'"id": "'+str(df.columns.values[j])+'", "group": '+str(columnCountDf  + j + 1)+'},\n'
        grapheFileLinksColumn += '{"source": "'+str(df.columns.values[0])+'", "target": "'+str(df.columns.values[j])+'", "value": '+str(countTot+j)+'},\n'
        while i < rowCountDf:
            grapheFileValues += "{"+'"id": "'+str(df[item].values[i])+'", "group": '+str(j+1)+'},\n'
            grapheFileLinks += '{"source": "'+str(df.columns.values[j])+'", "target": "'+str(df[item].values[i])+'", "value": '+str(j + 1)+'},\n'
            i = i + 1
        j = j + 1

    i = 0
    subjectColumn = "Core attribute"
    while i < rowCountDf:
        j = 0
        for item in headers:
            if j != 0:
                grapheFileLinksValues += '{"source": "'+str(df[subjectColumn].values[i])+'", "target": "'+str(df[item].values[i])+'", "value": '+str(countLast+i)+'},\n'
            else:
                subjectColumn = item
            j = j + 1
        i = i + 1

    grapheFileValues = grapheFileValues[:-2]+'\n'
    grapheFileLinksValues = grapheFileLinksValues[:-2]+'\n'
    graphePhile = grapheFileColumn+''+grapheFileValues+"],\n"+'"links": [\n'+grapheFileLinks+''+grapheFileLinksColumn+''+grapheFileLinksValues+']\n}'


    #print(graphePhile)
    pathBase = str(pathlib.Path(__file__).parent.resolve()).rsplit('\\', 2)[0]

    print(pathBase)

    ROOT_DIR =pathBase+'\\graph-file.json'
    f = open(ROOT_DIR, "a")
    f.seek(0)                        # <- This is the missing piece
    f.truncate()
    f.write(graphePhile)
    f.close()