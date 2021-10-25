import views
import os


print("run mantistable_main_test")

file_csv = os.path.abspath(os.curdir) + "\\mantistable\\Jeuxvideos.csv"

column_subject_index = views.get_subject_index_mantistable(file_csv)


print(column_subject_index)
print("end mantistable_main_test")