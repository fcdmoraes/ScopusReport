import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Source(object):
	name
	soup

def second_try(name):
	print("second try:", name)
	name = name.replace('-',' ')
	name = name.replace('&','And')
	url = 'https://www-scopus.ez67.periodicos.capes.gov.br/results/results.uri?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1={}&field1=SRCTITLE&dateType=Publication_Date_Type&yearFrom=2006&yearTo=Present&loadDate=7&documenttype=All&accessTypes=All&resetFormLink=&st1={}&st2=&sot=b&sdt=b&sl=25&s=SRCTITLE%28{}%29&sid=bcb197c7d0aeae158eb956eccdf7e5a1&searchId=bcb197c7d0aeae158eb956eccdf7e5a1&txGid=0d239eb0691e9b092f906f8218cbddc0&sort=plf-f&originationType=b&rr='.format(name,name,name)
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	try:
		Areas = soup.find('ul', id = "cluster_SUBJAREA")
		Areas = Areas.find_all('span', class_="btnText")
		Areas_text = list(map(lambda area: area.get_text().replace('\n',''), Areas))
		if ("Social Sciences" in Areas_text):
			return check_duplicity()
			# return 'Unsure'
		else:
			return False
	except:
		return 'Not Found'

def check_duplicity():
	soup = Source.soup
	Source_title = soup.find('ud', id_="cluster_EXACTSRCTITLE")
	Source_title = Source_title.find_all('span', class_='btnText')
	if len(Source_title)==1:
		return 'Ok'
	else:
		return 'Unsure'
	# Source_title = list(map(lambda source: source.get_text(), Source_title))



	

ini = 0
results = 100
first_time = True
output_filename = "teste_05.10.csv"

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

nome = "Nature Climate Change"
url = "https://www-scopus.ez67.periodicos.capes.gov.br/results/results.uri?sort=plf-f&src=s&st1={}&nlo=&nlr=&nls=&sid=65f022fdb8a1532543084f624d780d48&sot=b&sdt=cl&cluster=scoexactsrctitle%2c%22{}%22%2ct&sl=35&s=SRCTITLE%28{}%29+AND+PUBYEAR+%3e+2005&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid=564a84a1d55c56449e36e21586ef0bd7".format(nome,nome,nome)
driver = webdriver.Chrome()
driver.get(url)
# time.sleep(25)

trues = []
context = []
i = ini
j = 0
while j < results:
	next_ = False
	nome = '"'+titles[i]+'"'
	exact_name = titles[i].replace('-',' ').title()
	exact_name = exact_name.replace('&','And')
	Source.name = exact_name
	url = "https://www-scopus.ez67.periodicos.capes.gov.br/results/results.uri?sort=plf-f&src=s&st1={}&nlo=&nlr=&nls=&sid=65f022fdb8a1532543084f624d780d48&sot=b&sdt=cl&cluster=scoexactsrctitle%2c%22{}%22%2ct&sl=35&s=SRCTITLE%28{}%29+AND+PUBYEAR+%3e+2005&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid=564a84a1d55c56449e36e21586ef0bd7".format(nome,exact_name,exact_name)
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
		result = second_try(nome)
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

