import views
import os
import csv

print("run mantistable_main_test")

file_csv = os.path.abspath(os.curdir) + "\\mantistable\\Jeuxvideos.csv"

column_subject_index = views.get_subject_index_mantistable(file_csv)




with open(file_csv, 'r', encoding='utf-8') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj, quotechar='\'', delimiter=',',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)
    # Iterate over each row in the csv using reader object
    inputText =''
    for row in csv_reader:
        # row variable is a list that represents a row in csv
        #print(row)
        #rowFinal = str(row)[1:]
        #rowFinal = rowFinal[:-1]
        #inputText = inputText + rowFinal + '\r'

        # with mantistable move the subject column to first index
        row.insert(0, row.pop(1))


        firstWordLine = True
        for rowWord in row:
            if firstWordLine == True:
                inputText = inputText+'\r'+rowWord
                firstWordLine = False
            else:
                inputText = inputText+','+rowWord
    #print(inputText)



#print(column_subject_index)
print("end mantistable_main_test")