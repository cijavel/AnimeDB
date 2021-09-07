'''
Created on 05.07.2021
@author: Ci
'''
import requests
from bs4 import BeautifulSoup
import re
import logging
from logging import config
config.fileConfig("config/logging.conf")
logger = logging.getLogger("func")

class webparser_anisearch:
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_infodetails
	# - parse infodetails of anime from html source
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
	
			if infodetails:
				return infodetails
			else:
				logger.error("parsing error. Can't parse values. webpage struktur might have changed")
				return None
		else:
			logger.error('parsing error. No anime details section found')
			return None
		
	#----------------------------------------	
	# Date: 2021.07.05
	# Name: get_description
	# - parse description from html source
	# out: list (lang, descipt)
	#----------------------------------------
	def get_description(self, soup):
		werte = {}

		for div in soup.find_all("i", {'class':'hidden'}): 
			div.decompose()
		for div in soup.find_all("ul", {'class':'cloud'}): 
			div.decompose()
			
		desc = soup.find(id='description')

		if desc:
			for tr in desc.find_all("div", {"class": "details-text"}):
				sValue = tr.text
				skey = tr.get('lang')
				werte.update({skey: sValue})
			if werte:
				return werte
			else:
				logger.error("parsing error. Can't parse values. webpage struktur might have changed")
				return None
		else:
			logger.error('parsing error. No description section found')
			return None

			
		
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_animename
	# - parse animename from html source
	# out: animename
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
			if animeName:
				return animeName
			else:
				logger.error("parsing error. Can't parse values. webpage struktur might have changed")
				return None	
		else:
			logger.error('parsing error. No animename section found')
			return None
			

		
	
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_rating
	# - parse rating from html source
	# out: dict
	#----------------------------------------
	def get_rating(self, soup):
		rating = soup.find(id='ratingstats')
		daten = {}
		if rating:
			for rat in rating.find_all("td"):

				minus = rat.find("span")
				if minus is not None:
					soup_name = BeautifulSoup(str(rat).replace(str(minus), ""), 'html.parser')
					name = soup_name.find("td").text
					soup_value = BeautifulSoup(str(minus), 'html.parser')
					value = soup_value.find("span").text

					if name == "Rang":
						daten.update({"rating_rank": value.lstrip('#')})
					if name == "Klarwert":
						rating_value = value.split("=")
						daten.update({"rating_val": rating_value[0]})
						daten.update({"rating_per": rating_value[1]})

			if daten:
				return daten
			else:
				logger.error("parsing error. Can't parse values. webpage struktur might have changed")
				return None
		else:
			logger.error('parsing error. No rating section found')
			return None

	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_relations
	# - parse relation from html source
	# out: list (number, link, name,lang, rel_descrip , rel_direct)
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

			if relationlist:
				return relationlist
			else:
				logger.error("parsing error. Can't parse values. webpage struktur might have changed")
				return None
		else:
			relationblock = soup.find("div", {"class": "helptext"})
			if -1 == int(relationblock.text.index("Werke eine Relation")):
				logger.error('parsing error. No relations section found')
			return None

		

		
	#----------------------------------------
	# Date: 2021.07.05
	# Name: PrimaryKey Anisearch - good
	# - get PrimaryKey from anisearch web link
	# in:  anisearch web link for anime
	# out: PrimaryKey from anisearch weblink
	#----------------------------------------
	def get_anisearchPrimaryKey(self, link):
		number = ""
		if link:
			try:
				p = re.compile(r'\/\d+')
				get_animeNumber= p.findall(link)
				number = get_animeNumber[0]
				number = number.replace("/", "")
			except:
				logger.error('please check link: %s' + link)

		if number:
			return number
		else:
			logger.error("parsing error. Can't parse values. Link struktur might have changed")
			return None


class open_webpage:
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_webpage
	# - get html source from Internet
	# out: html source
	#----------------------------------------
	def get_webpage(self, link):
		soup = "no html"

		try:
			r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
		except:
			logger.error('wrong url: %s', link)
		if str(r.status_code) == "200":
			soup = BeautifulSoup(r.text, 'html.parser')
			return soup
		else:
			logger.error('webpage error: %s - Pease check adress. error: %s', link, str(r.status_code))
			return None

		
	




