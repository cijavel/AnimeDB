import requests
from bs4 import BeautifulSoup
import re

class webparser_anisearch:
	#----------------------------------------
	# infodetails
	# table
	#----------------------------------------
	def get_infodetails(self, soup):
		skey = ""
		sValue = ""
		infodetails = {}


		details = soup.find(id='infodetails')
		if details:
			for tag in details.find_all('li'):
				skey = tag.find('span').text
				sValue = tag.text.replace(skey, "")
				infodetails.update({skey: sValue})
		else:
			print("ERROR - get_infodetails - No anime details found")
			
		return infodetails
		
	#----------------------------------------	
	# Description
	# lang, descipt
	#----------------------------------------
	def get_description(self, soup):
		werte = {}

		for div in soup.find_all("i", {'class':'hidden'}): 
			div.decompose()
		for div in soup.find_all("ul", {'class':'cloud'}): 
			div.decompose()
			
		desc = soup.find(id='description')

		if desc:
			for tr in desc.find_all("div", {'itemprop':'description'}):
				sValue = tr.text
				skey = tr.get('lang')
				werte.update({skey: sValue})
		else:
			print("ERROR - get_description - No description found")

		return werte
		
	#----------------------------------------
	# AnimeName Anisearch
	# lang, name
	#----------------------------------------
	def get_animename(self, soup):

		skey = ""
		sValue = ""
		animeName = {}

		name = soup.find(id='information')
		if name:
			for tag in name.find_all("div", {"class": "title"}): 
				sValue = tag.find('strong').text
				skey = tag.get('lang')
				animeName.update({skey: sValue})
		else:
			print("ERROR - get_animename - No animename found")
			
		return animeName
	
	#----------------------------------------
	# Rating Anisearch
	# number, procent
	#----------------------------------------
	def get_rating(self, soup):
		rating = soup.find(id='ratingstats')
		daten = ""
		if rating:
			for rat in rating.find_all("span"): 
				if rat.has_attr('itemprop'):
					big = rat.find_parent("span").text
					daten = big.split("=")
					break
		else:
			print("ERROR - get_rating - No rating found")
		return daten

	#----------------------------------------
	# relation Anisearch
	#----------------------------------------
	def get_relations(self, soup):
		
		relationlist = []
		relationblock = soup.find("table", {"class": "responsive-table"})
		if relationblock:
			tbody = relationblock.find("tbody")
			tr = tbody.find_all("th")
			for ds in tr:
				reldescrip = ""
				end_number = ""
				end_link = ""
				end_name = ""
				end_lang = ""
				end_rel_descrip = ""

				lin = ds.find('a', href=True)
				reldescrip = ds.find("div", {"class": "f12"})
				end_number = lin.get('href').replace("anime/", "").split(',')[0]
				end_link = lin.get('href')
				end_name = lin.text
				end_lang = lin.get('lang')
				if reldescrip:
					end_rel_descrip = reldescrip.text
					end_rel_direct = 1
				else:
					end_rel_direct = 0
				relationlist.append([end_number, end_link, end_name,end_lang, end_rel_descrip , end_rel_direct])

		else:
			print("ERROR - get_relations - No relations found")


		return relationlist
	#----------------------------------------
	# PrimaryKey Anisearch
	# ID
	#----------------------------------------
	def get_anisearchPrimaryKey(self, link):
		number = ""
		try:
			p = re.compile(r'\/\d+')
			get_animeNumber= p.findall(link)
			number = get_animeNumber[0]
			number = number.replace("/", "")
		except:
			print("ERROR - get_anisearchPrimaryKey - please check link: " + link )
			
		return number



class open_webpage:
	#----------------------------------------
	# webseite aufrufen
	#----------------------------------------
	def get_webpage(self, link):
		soup = "no html"
		try:
			r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
		except:
			print("get_html: wrong url ?")
		if str(r.status_code) == "200":
			soup = BeautifulSoup(r.text, 'html.parser')

		else:
			print(" webpage error for: " + link + " - Pease check adress. error: " + str(r.status_code))

		return soup
	




