import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Source(object):
	name = ''
	soup = ''

def second_try(name):
	print("second try:", name)
	name = name.replace('-',' ')
	name = name.replace('&','And')
	url = 'https://www-scopus.ez67.periodicos.capes.gov.br/results/results.uri?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1={}&field1=SRCTITLE&dateType=Publication_Date_Type&yearFrom=2006&yearTo=Present&loadDate=7&documenttype=All&accessTypes=All&resetFormLink=&st1={}&st2=&sot=b&sdt=b&sl=25&s=SRCTITLE%28{}%29&sid=bcb197c7d0aeae158eb956eccdf7e5a1&searchId=bcb197c7d0aeae158eb956eccdf7e5a1&txGid=0d239eb0691e9b092f906f8218cbddc0&sort=plf-f&originationType=b&rr='.format(name,name,name)
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	Source.soup = soup
	Areas = soup.find('ul', id = "cluster_SUBJAREA")
	if Areas != None:
		Areas = Areas.find_all('span', class_="btnText")
		Areas_text = list(map(lambda area: area.get_text().replace('\n',''), Areas))
		if ("Social Sciences" in Areas_text):
			return check_duplicity()
			# return 'Unsure'
		else:
			return False
	else:
		return 'Not Found'

def check_duplicity():
	soup = Source.soup
	Source_title = soup.find('div', id ="clusterAttribute_EXACTSRCTITLE")
	Source_title = Source_title.find_all('label', class_='checkbox-label')
	if len(Source_title)==1:
		return 'Ok'
	else:
		Source_title = list(map(lambda source: source.get_text().replace("\n",""), Source_title))
		# print(Source_title)
		exact_name = find_source(Source_title)
		if exact_name == False:
			return 'Unsure'
		else:
			print("third try: {}".format(exact_name))
			url = "https://www-scopus.ez67.periodicos.capes.gov.br/results/results.uri?sort=plf-f&src=s&st1={}&nlo=&nlr=&nls=&sid=65f022fdb8a1532543084f624d780d48&sot=b&sdt=cl&cluster=scoexactsrctitle%2c%22{}%22%2ct&sl=35&s=SRCTITLE%28{}%29+AND+PUBYEAR+%3e+2005&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid=564a84a1d55c56449e36e21586ef0bd7".format(exact_name,exact_name,exact_name)
			driver.get(url)
			soup = BeautifulSoup(driver.page_source, 'html.parser')
			Areas = soup.find('ul', id = "cluster_SUBJAREA")
			Areas = Areas.find_all('span', class_="btnText")
			Areas_text = list(map(lambda area: area.get_text().replace('\n',''), Areas))
			if ("Social Sciences" in Areas_text):
				return 'Probably Ok - checked: {}'.format(exact_name)
			else:
				return 'Probably False - checked: {}'.format(exact_name)

def find_source(source_list):
	list1 = Source.name.replace('"','').replace('-',' ').replace('&','And').lower().split()
	for source in source_list:
		list2 = source.lower().split()
		intersection = [word for word in list1 if word in list2]
		if len(intersection)/len(list1)>0.75 and len(intersection)/len(list2)>0.75:
			return source
	return False
	

ini = 739
results = 10
first_time = False
output_filename = "full_06.10.csv"

dados = pd.read_csv("JHG.csv", skiprows = 1)
# print(dados.head())
titles = dados["Full Journal Title"]
rk = dados["Rank"]
imp_f = dados["Journal Impact Factor"]

print('-'*50)
print("Número de revistas: {}".format(len(titles)))

if first_time:
	file = open(output_filename,'w')
	file.write("Full Journal Title,Journal Impact Factor,Search Result\n")
	file.close()

name = "Nature Climate Change"
url = "https://www-scopus.ez67.periodicos.capes.gov.br/results/results.uri?sort=plf-f&src=s&st1={}&nlo=&nlr=&nls=&sid=65f022fdb8a1532543084f624d780d48&sot=b&sdt=cl&cluster=scoexactsrctitle%2c%22{}%22%2ct&sl=35&s=SRCTITLE%28{}%29+AND+PUBYEAR+%3e+2005&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid=564a84a1d55c56449e36e21586ef0bd7".format(name,name,name)
driver = webdriver.Chrome()
driver.get(url)
# time.sleep(25)

trues = []
context = []
i = ini
j = 0
while j < results:
	next_ = False
	name = '"'+titles[i]+'"'
	exact_name = titles[i].replace('-',' ').title()
	exact_name = exact_name.replace('&','And')
	Source.name = exact_name
	url = "https://www-scopus.ez67.periodicos.capes.gov.br/results/results.uri?sort=plf-f&src=s&st1={}&nlo=&nlr=&nls=&sid=65f022fdb8a1532543084f624d780d48&sot=b&sdt=cl&cluster=scoexactsrctitle%2c%22{}%22%2ct&sl=35&s=SRCTITLE%28{}%29+AND+PUBYEAR+%3e+2005&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid=564a84a1d55c56449e36e21586ef0bd7".format(name,exact_name,exact_name)
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	Source.soup = soup
	try:
		Areas = soup.find('ul', id = "cluster_SUBJAREA")
		Areas = Areas.find_all('span', class_="btnText")
		Areas_texto = list(map(lambda area: area.get_text().replace('\n',''), Areas))
		if ("Social Sciences" in Areas_texto):
			context.append('Ok')
			trues.append(i)
			j += 1
	except:
		result = second_try(name)
		if result != False:
			context.append(result)
			trues.append(i)
			j += 1
	i+=1
driver.quit()

print("Revistas pesquisadas:", i)

file = open(output_filename,'a')
for (j,i) in enumerate(trues):
	print ("{:4} - {:40.35} - IF:{:7} - {}".format(rk[i],titles[i],imp_f[i],context[j]))
	file.write("{},{},{},{}\n".format(rk[i],titles[i],imp_f[i],context[j]))
file.close()

