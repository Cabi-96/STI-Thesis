from selenium import webdriver

url = 'https://dbpedia.mtab.app/mtab'

# open browser
driver = webdriver.Firefox(executable_path=r'C:/Program Files/Mozilla Firefox/geckodriver.exe')

# load page
driver.get(url)

# find field
item = driver.find_element_by_id('table_text_content')

# put text
driver.find_element_by_id('table_text_content').clear()
item.send_keys('W. S. Coffin,Yale Divinity School,E. Rubinstein,"Strafford, Vermont",New York City\r W. S. Coffin,Yale Divinity School,E. Rubinstein,"Strafford, Vermont",New York City')

# find button
item = driver.find_element_by_id('annotation1')

# click button
item.click()

all_answers = driver.find_elements_by_class_name('table-info')
print("CTA:\r")
for answer in all_answers:
   links = answer.find_elements_by_xpath(".//th/a")
   for link in links:
   # print link href
      print(link.get_attribute("href"))

all_answers = driver.find_elements_by_class_name('table-success')
print("CPA:\r")
for answer in all_answers:
   links = answer.find_elements_by_xpath(".//th/a")
   for link in links:
      # print link href
      print(link.get_attribute("href"))


all_answers = driver.find_elements_by_xpath('*//table[@class="table table-bordered"]/tbody')
print("CEA:\r")
for answer in all_answers:
   links = answer.find_elements_by_xpath(".//td/a")
for link in links:
   # print link href
   print(link.get_attribute("href"))

#elems = driver.find_elements_by_xpath("//a[@href]")
#for elem in elems:
#   print(elem.get_attribute("href"))

# find all red numbers
#all_answers = driver.find_elements_by_class_name('table-info')
#for answer in all_answers:
#   print(answer.text)


