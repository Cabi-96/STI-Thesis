
import sys
import subprocess

#
# pip install pandas
# pip install requests
# pip install tabulate
# pip install selenium==3.141.0
# pip install isbnlib
# pip install nltk
# pip install validators
# pip install sparqlwrapper
# pip install tkinterweb
# pip install openpyxl
# pip install sparqlwrapper.skipssl

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install','logging'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','tabulate'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','selenium==3.141.0'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','isbnlib'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','nltk'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','validators'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','sparqlwrapper'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','tkinterweb'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','openpyxl'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','sparqlwrapper.skipssl'])


import nltk
nltk.download('stopwords')