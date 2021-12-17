import copy

import pandas as pd

totCelAnnoted = 0
totCelCorrectlyAnnoted = 0
totTargetAnnoted = 0
totCelAddedAnnoted = 0
totCelAddedCorrectlyAnnoted = 0
totTargetAddedAnnoted = 0

def finalDf(dfFinal,isAddCol,i,fcru,cellAnnoted,celCorreclyAnnoted,targetCell,valueTargetAnnoted):
    dfFinal.at[i,"File name - column - row - URI"] = fcru
    dfFinal.at[i,"Cel Annoted"] = cellAnnoted
    dfFinal.at[i,"Cel Correcly annoted"] = celCorreclyAnnoted
    dfFinal.at[i,"Target Cell"] = targetCell
    dfFinal.at[i,"Value Target Annoted"] = valueTargetAnnoted
    if not isAddCol:
        global totCelAnnoted
        global totCelCorrectlyAnnoted
        global totTargetAnnoted

        totCelAnnoted = totCelAnnoted +cellAnnoted
        totCelCorrectlyAnnoted = totCelCorrectlyAnnoted +celCorreclyAnnoted
        totTargetAnnoted = totTargetAnnoted +valueTargetAnnoted
    else :
        global totCelAddedAnnoted
        global totCelAddedCorrectlyAnnoted
        global totTargetAddedAnnoted

        totCelAddedAnnoted = totCelAddedAnnoted + cellAnnoted
        totCelAddedCorrectlyAnnoted = totCelAddedCorrectlyAnnoted + celCorreclyAnnoted
        totTargetAddedAnnoted = totTargetAddedAnnoted + valueTargetAnnoted


#Premier Fichier
from application.utils.utils import printDf

df = pd.read_csv(r"C:\Users\ANTHONY\Desktop\EvaluationCode\EvaluationTestCode.csv")

rowCountDf1 = len(df.index)
headers = list(df.columns.values)[1:]

df2 = pd.DataFrame(columns=["A","B"])


x = [[0 for i in range(2)] for j in range(int(df['Row'].iloc[-1]))]


i = 0
while i < rowCountDf1:
    x[df.at[i,"Row"]-1][df.at[i,"Column"]-1] = df.at[i,"Data"]
    i = i+1

i = 0

for i in range(len(x)):
    df2.at[i,"A"] = x[i][1]
    df2.at[i,"B"] = x[i][0]

printDf(df2)
#Deuxieme fichier
df = pd.read_csv(r"C:\Users\ANTHONY\Desktop\EvaluationCode\EvaluationTestCode2.csv")

rowCountDf1 = len(df.index)
headers = list(df.columns.values)[1:]

df3 = pd.DataFrame(columns=["A","B"])


x = [[0 for i in range(2)] for j in range(int(df['Row'].iloc[-1]))]


i = 0
while i < rowCountDf1:
    x[df.at[i,"Row"]-1][df.at[i,"Column"]-1] = df.at[i,"Data"]
    i = i+1

i = 0
for i in range(len(x)):
    df3.at[i,"A"] = x[i][1]
    df3.at[i,"B"] = x[i][0]

printDf(df3)


#Merge like page two
"""
columnDf2 =  df2.columns.values.tolist()
columnDf3 =  df3.columns.values.tolist()

listIndexDf3 = list()
for i in range(len(columnDf3)):
    listIndexDf3.append(i)

commonElement = list(set(columnDf2).intersection(columnDf3))
listIndex = list()
if len(commonElement) > 0:
    for element in commonElement:
        listIndex.append(columnDf3.index(element))

    i = 0
    for index in listIndex:
        del listIndexDf3[index - i]
        i = i + 1
    df3tmp = copy.deepcopy(df3.iloc[:, listIndexDf3])
else:
    df3tmp = df3

printDf(df3tmp)

df = pd.merge(df2,df3tmp,on="A",how='left')



cond = df2.iloc[:,0].isin(df.iloc[:,0])
df2.drop(df2[cond].index, inplace = True)

#print("df1")
#printDf(df1)
df3tmp = df3

cond = df3tmp.iloc[:,0].isin(df.iloc[:,0])
df3.drop(df3[cond].index, inplace = True)

#print("df2tmp")
#printDf(df2)



#df = df.append(df2,ignore_index=True,sort=False)

#print("self.df")
#printDf(self.df)

#df = df.append(df3, ignore_index=True, sort=False)
"""
df2 = df2.append(df3, ignore_index=True, sort=False)

printDf(df2)


dfRes = pd.read_csv(r"C:\Users\ANTHONY\Desktop\EvaluationCode\test.csv")

printDf(dfRes)

dfFinal = pd.DataFrame(columns=["File name - column - row - URI","Cel Annoted","Cel Correcly annoted","Target Cell","Value Target Annoted"])
rowCountDfRes = len(dfRes.index)
i = 0
isHttpRes = False
isHttpTarget = False
j = 0



while i < rowCountDfRes:

    #Première colonne
    if str(df2.at[i,"A"]).startswith("http"):
        isHttpTarget= True
    else:
        isHttpTarget = False

    if str(dfRes.at[i,"Core attribute"]).startswith("http"):
        isHttpRes= True
    else:
        isHttpRes = False

    if dfRes.at[i,"Core attribute"] in df2.at[i,"A"]:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"],1,1,df2.at[i,"A"],1)
       #print('ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"]+' 1'+' 1 '+df2.at[i,"A"]+' 1')

    elif dfRes.at[i,"Core attribute"] not in df2.at[i,"A"] and isHttpTarget and isHttpRes:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"],1,0,df2.at[i,"A"],1)
        #print('ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"]+' 1'+' 0 '+df2.at[i,"A"]+' 1')

    elif dfRes.at[i,"Core attribute"] not in df2.at[i,"A"] and not isHttpRes and isHttpTarget:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"],0,0,df2.at[i,"A"],1)
    #print('ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"]+' 0'+' 0 '+df2.at[i,"A"]+' 1')

    elif dfRes.at[i,"Core attribute"] not in df2.at[i,"A"] and isHttpRes and not isHttpTarget:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"],1,0,'nan',0)
        #print('ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"]+' 1'+' 0 '+df2.at[i,"A"]+' 0')
    else:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"],0,0,'nan',0)
        #print('ResultatDataset1 '+'"'+str(0)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"Core attribute"]+' 0'+' 0 '+df2.at[i,"A"]+' 0')

    j = j + 1
    #Deuxième colonne
    if str(df2.at[i,"B"]).startswith("http"):
        isHttpTarget= True

    if str(dfRes.at[i,"http://dbpedia.org/ontology/president"]).startswith("http"):
        isHttpRes= True

    if dfRes.at[i,"http://dbpedia.org/ontology/president"] in df2.at[i,"B"]:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"],1,1,df2.at[i,"B"],1)
        #print('ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"]+' 1'+' 1 '+df2.at[i,"B"]+' 1')

    elif dfRes.at[i,"http://dbpedia.org/ontology/president"] not in df2.at[i,"B"] and isHttpTarget and isHttpRes:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"],1,0,df2.at[i,"B"],1)
        #print('ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"]+' 1'+' 0 '+df2.at[i,"B"]+' 1')

    elif dfRes.at[i,"http://dbpedia.org/ontology/president"] not in df2.at[i,"B"] and not isHttpRes and isHttpTarget:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"],0,0,df2.at[i,"B"],1)
        #print('ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"]+' 0'+' 0 '+df2.at[i,"B"]+' 1')

    elif dfRes.at[i,"http://dbpedia.org/ontology/president"] not in df2.at[i,"B"] and isHttpRes and not isHttpTarget:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"],0,0,'nan',0)
        #print('ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"]+' 1'+' 0 nan 0')
    else:
        finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"],0,0,'nan',0)
        #print('ResultatDataset1 '+'"'+str(1)+'"'+' "'+str(i)+'" URI:'+dfRes.at[i,"http://dbpedia.org/ontology/president"]+' 0'+' 0 nan 0')

    j = j + 1
    #Troisième colonne pas de target
    finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(2)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/staff"]),0,0,'nan',0)
    #print('ResultatDataset1 '+'"'+str(2)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/staff"])+' 0'+' 0 nan 0')

    j = j + 1
    #Quatrième colonne pas de target
    finalDf(dfFinal,False,j,'ResultatDataset1 '+'"'+str(3)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/facultySize"]),0,0,'nan',0)
    #print('ResultatDataset1 '+'"'+str(3)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/facultySize"])+' 0'+' 0 nan 0')

    j = j + 1
    #Cinquième colonne ADD column
    if dfRes.at[i,"http://dbpedia.org/ontology/city"] != 'nan':
        finalDf(dfFinal,True,j,'ResultatDataset1 '+'"'+str(4)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/city"]),1,1,str(dfRes.at[i,"http://dbpedia.org/ontology/city"]),1)
        #print('ResultatDataset1 '+'"'+str(4)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/city"])+' 1'+' 1 '+str(dfRes.at[i,"http://dbpedia.org/ontology/city"])+' 1')
    else:
        finalDf(dfFinal,True,j,'ResultatDataset1 '+'"'+str(4)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/city"]),0,0,'nan',0)
        #print('ResultatDataset1 '+'"'+str(4)+'"'+' "'+str(i)+'" URI:'+str(dfRes.at[i,"http://dbpedia.org/ontology/city"])+' 0'+' 0 nan 0')

    j = j + 1
    i = i + 1


print(totCelAnnoted)
print(totCelCorrectlyAnnoted)
print(totTargetAnnoted)
print(totCelAddedAnnoted)
print(totCelAddedCorrectlyAnnoted)
print(totTargetAddedAnnoted)
printDf(dfFinal)
dfFinal.to_excel(r'EvaluationDataset.xlsx', index=False)
