

import requests
from bs4 import BeautifulSoup

def get_angebot(soup):

	uberschrift = []
	werte = []


	table = soup.find("form", {"class": "categoryForm"})
	tbody = soup.find("tbody")
	thead = soup.find("thead")
	
	for th in thead.find_all('th'):
		uberschrift.append(th.text)
		
	werte.append(uberschrift)
	for tr in tbody.find_all('tr'):
		test = list(map(lambda x:x.text,tr.find_all('td')))
		try:
			if test[0]:
				werte.append(test)
		except:
			pass

	return werte
	

def get_webpage(link):
	try:
		r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
	except:
		print("get_html: wrong url ?")
	if str(r.status_code) == "200":
		soup = BeautifulSoup(r.text, 'html.parser')
		return soup
	else:
		print(" webpage error for: " + link + " - Pease check adress. error: " + str(r.status_code))
		return 0
	return 0
	

#soup = get_webpage("https://www.auer-packaging.com/de/de/RL-KLT-Beh%C3%A4lter.html?bstock")
soup = get_webpage("https://www.auer-packaging.com/de/de/Eurobeh%C3%A4lter-geschlossen.html?bstock")
if soup != 0:
	for i in get_angebot(soup):
		print(i)
else:
	print("no webpage")