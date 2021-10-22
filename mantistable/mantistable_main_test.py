import views
import os

print("run")

FILE = os.path.abspath(os.curdir) + "\\mantistable\\Australian_Test.json"

print(FILE)

f = open(FILE, "r")



views.create_tables(f)