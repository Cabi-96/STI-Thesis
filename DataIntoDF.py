from csv import reader
import pandas as pd


#-------------------------------------------------------------------------------------------------
#CLASS
#-------------------------------------------------------------------------------------------------

class DataInfoDF:
    __ontologiesTable1 = ""
    __ontologiesTable2 = ""

    def __init__(self,pathCEA,pathCTA):
        self.pathCEA = pathCEA
        self.pathCTA = pathCTA

    def __readCsvFile(self,path):
        with open(path, 'r', encoding= 'utf-8') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)

            #list which contains the ontologies of the columns
            dataList = list()

            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                #print(row)
                dataList.append(str(row))
            return dataList

    def getOntologiesTable1(self):
        return self.__ontologiesTable1

    def getOntologiesTable2(self):
        return self.__ontologiesTable2

    def __printDf(self,df):
        print(df)
        df.to_csv(r'C:\Users\ANTHONY\Desktop\ECOLE\MA1\Mémoire\Outil\File Name.csv',index=Fals)

    def __cleanOntologies(self,tableName, ctaInfos):
        ontologyList = list()
        for item in ctaInfos:
            i = str(item).rfind(',')
            if tableName in item:
                #print(item)
                #On récupère le lien web de l'ontologie du String
                subjectOntologyTable = item[i+1:len(item)-2]
                #Remove all double quotes
                subjectOntologyTable = subjectOntologyTable.strip('"')
                #print(subjectOntologyTable)
                ontologyList.append(subjectOntologyTable)
        return ontologyList


    def __getArray(self,tableName, arrayTab, dataList):
        for item in dataList:
            if tableName in item:
                lastDataLineTab = item
                i = lastDataLineTab.find(',')
                j = lastDataLineTab.replace(',', 'XXX', 1).find(',')
                indexJTableau= int(lastDataLineTab[i + 3:j - 3])
                tmp = lastDataLineTab.replace(',', 'XXX', 1)
                z = tmp.replace(',', 'XXX', 1).find(',')
                indexITableau = int(lastDataLineTab[j + 1:z - 5])
                #print('Index ok?')
                #print(indexITableau-1,indexJTableau)
                #print(len(arrayTab), len(arrayTab[0]))
                arrayTab[indexITableau-1][indexJTableau] = self.__cleanData(item)
        return arrayTab

    def __getDf(self,arrayTab, ontologies):
        arrayHeaders = ontologies
        #print(ontologies)
        df = pd.DataFrame(data = arrayTab,
                          columns = arrayHeaders,
                          dtype= str)
        return df


    def __findIndexI(self,lastDataLineTab):
        #ICi l'input change et qu'il y a une erreur, vérifier ici! Ici, on récupère le nombre max de colonne pour le tableau 1.
        i = lastDataLineTab.find(',')
        j = lastDataLineTab.replace(',', 'XXX', 1).find(',')
        return lastDataLineTab[i + 3:j - 3]

    def __findIndexJ(self,lastDataLineTab):
        #ICi l'input change et qu'il y a une erreur, vérifier ici! Ici, on récupère le nombre max de ligne pour le tableau 1. .
        j = lastDataLineTab.replace(',', 'XXX', 1).find(',')
        tmp = lastDataLineTab.replace(',', 'XXX', 1)
        z = tmp.replace(',', 'XXX', 1).find(',')
        return lastDataLineTab[j + 1:z - 5]



    def __find_nth_overlapping(self,haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+1)
            n -= 1
        return start

    def __cleanData(self,item):
        #print("Function cleanOntology")
        #On veut les ontologies (liens dbpedia pour pouvoir les comparer)
        i = self.__find_nth_overlapping(item, ',', 3)
        #On récupère le lien web de l'ontologie du String
        subjectOntologyTable = item[i + 2:len(item) - 2]

        #Remove bad writting
        subjectOntologyTable = subjectOntologyTable.replace('"',"")
        subjectOntologyTable = subjectOntologyTable.replace("', '",",")
        subjectOntologyTable = subjectOntologyTable.replace(", '",",")
        subjectOntologyTable = subjectOntologyTable.replace(' ','_')
        if subjectOntologyTable.startswith('\''):
            subjectOntologyTable = subjectOntologyTable[1:]
        #print(subjectOntologyTable)
        return subjectOntologyTable

    def runTab1(self):
            dataList = self.__readCsvFile(self.pathCEA)

            #print(dataList[1])
            dataList.reverse()
            lastDataLineTab1 = ""
            for item in dataList:
                if 'Table1' in item:
                    #store the item in a variable
                    lastDataLineTab1 = item
                    #break out of loop
                    break

            indexITableau = self.__findIndexI(lastDataLineTab1)
            indexJTableau = self.__findIndexJ(lastDataLineTab1)

            #print('Index Tableau1 I:', indexJTableau)
            #print('Index Tableau1 J:', indexITableau)
            arrayTab1 = [[0 for x in range(int(indexITableau) + 1 )] for y in range(int(indexJTableau))]

            #------------------------------------------------------------------------------------------------------------------------
            #Après avoir reçu les dimensions des deux tables, il suffit de les remplir.
            #------------------------------------------------------------------------------------------------------------------------
            #list which contains the ontologies of the columns
            ctaInfos = self.__readCsvFile(self.pathCTA)

            DataInfoDF.__ontologiesTable1 = self.__cleanOntologies("table1", ctaInfos)

            #Fill les tableaux. Vu que le tableau est inversé, il faut faire les index dans l'autre sens. Table1 Hard codé trouver autre chose aussi?
            #Je le fais direct passé en DataFrame
            array1 = self.__getArray('Table1', arrayTab1, dataList)

            df1 = self.__getDf(array1, DataInfoDF.__ontologiesTable1)
            #printDf(df1)

            return df1


    def runTab2(self):
            dataList = self.__readCsvFile(self.pathCEA)

            dataList.reverse()
            #print("Tab2")
            lastDataLineTab2 = dataList[0]
            #print(lastDataLineTab2)


            #ICi l'input change et qu'il y a une erreur, vérifier ici! Ici, on récupère le nombre max de ligne pour le tableau 1. .
            indexITableau= self.__findIndexI(lastDataLineTab2)
            indexJTableau = self.__findIndexJ(lastDataLineTab2)
            #print(indexITableau,indexJTableau)
            arrayTab2 = [[0 for x in range(int(indexITableau) + 1)] for y in range(int(indexJTableau))]
            #------------------------------------------------------------------------------------------------------------------------
            #Après avoir reçu les dimensions des deux tables, il suffit de les remplir.
            #------------------------------------------------------------------------------------------------------------------------
            ctaInfos = self.__readCsvFile(self.pathCTA)

            #print('cleanOntologies')
            DataInfoDF.__ontologiesTable2 = self.__cleanOntologies("table2", ctaInfos)



            #Fill les tableaux. Vu que le tableau est inversé, il faut faire les index dans l'autre sens. Table1 Hard codé trouver autre chose aussi?
            #Je le fais direct passé en DataFrame
            array2 = self.__getArray('Table2', arrayTab2, dataList)

            df2 = self.__getDf(array2, DataInfoDF.__ontologiesTable2)
            #printDf(df2)

            return df2

    #print(pd.isnull(result.at[1,"http://dbpedia.org/ontology/Person1"]))
    #if pd.isnull(result.at[1,"http://dbpedia.org/ontology/Person1"]):
