# ********************************************************************* 
import pyodbc

try:
    import functions.get_webpageparser as pars
except ImportError:
    from functions import get_webpageparser as parser

# Object
parser = pars.webparser_anisearch()
openpage = pars.open_webpage()

#variablen
DBconn = "DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\DEPLOYMENT\PHYTON\DBTEST\Anime.mdb;"


#----------------------------------------
# get_SQL_unsync_anime_anisearch
# string
#----------------------------------------
def get_SQL_unsyncList_anime_anisearch(DBconn):
	strSQL = 'SELECT Anime.ID, Anime.anisearch_de, Anime.Name FROM Anime WHERE ((Anime.anisearch_sync=False) AND (Anime.anisearch_de IS NOT NULL))'
	conn = pyodbc.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSQL)
		results = cursor.fetchall()
	return(results)

#----------------------------------------
# get_SQL_Genre
# ID
#----------------------------------------
def get_SQL_Genre(DBconn, genreName):
	strSQL = "SELECT Genre.ID, Genre.Genre FROM Genre WHERE Genre.Genre = '%s'" 
	conn = pyodbc.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSQL % genreName)
		results = cursor.fetchall()
	if not results:
		conn = pyodbc.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			sql = "INSERT INTO Genre (Genre) VALUES ('%s')"
			cursor.execute(sql % genreName)
			conn.commit()
			print(cursor.rowcount, "genre record(s) added ( " + genreName + " )" ) 
			cursor.execute(strSQL % genreName)
			results = cursor.fetchall()

	for row in results:
		(id, name) = row		
	
	return(id)

#----------------------------------------
# get_SQL_Genre
# ID
#----------------------------------------
def get_SQL_Type(DBconn, typeName):
	strSQL = "SELECT Typ.ID, Typ.Typ FROM Typ WHERE Typ.Typ = '%s'" 
	conn = pyodbc.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSQL % typeName)
		results = cursor.fetchall()
	if not results:
		conn = pyodbc.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			sql = "INSERT INTO Typ (Typ) VALUES ('%s')"
			cursor.execute(sql % typeName)
			conn.commit()
			print(cursor.rowcount, "genre record(s) added ( " + typeName + " )" ) 
			cursor.execute(strSQL % typeName)
			results = cursor.fetchall()

	for row in results:
		(id, name) = row		
	
	return(id)

#----------------------------------------
# get_SQL_unsync_anime_anisearch
# string
#----------------------------------------
def set_SQL_update_infordetails(DBconn, soup, vID_Anime):
	results = ""
	vTyp = ""
	vEpisoden = ""
	vVeroeffentlicht = ""
	vHauptgenres = ""
	vHerkunft = ""
	vAdaptiert = ""
	vZielgruppe = ""

	#strSQL = """UPDATE Anime SET  Anime.Folgenanzahl = '1', Anime.anisearch_sync = 0  WHERE Anime.ID = 10 """
	#"UPDATE Anime SET Anime.Typ = '', Anime.Folgenanzahl = '', Anime.Erscheinungsjahr = '', Anime.Genre = '', Anime.Zielgruppe = '' WHERE Anime.ID=
	
	
	
	infosD = parser.get_infodetails(soup)
	print(infosD)
	
	if 'Typ' 			in infosD: vTyp = get_SQL_Type(DBconn,infosD['Typ'])
	if 'Episoden' 		in infosD: vEpisoden = 			infosD['Episoden']
	if 'Veröffentlicht' in infosD: vVeroeffentlicht = 	infosD['Veröffentlicht']
	if 'Hauptgenres' 	in infosD: vHauptgenres = get_SQL_Genre(DBconn,infosD['Hauptgenres'])
	if 'Herkunft' 		in infosD: vHerkunft = 			infosD['Herkunft']
	if 'Adaptiert' 		in infosD: vAdaptiert = 		infosD['Adaptiert von']
	if 'Zielgruppe' 	in infosD: vZielgruppe = 		infosD['Zielgruppe']



	print(vTyp)

	
	#conn = pyodbc.connect(DBconn)
	#with conn:
	#	cursor = conn.cursor()
	#	cursor.execute(strSQL)
	#	results = cursor.fetchall()
    #
	##cur.execute("SELECT * FROM userdata WHERE Name = %s;", (name,))

	return(results)

#----------------------------------------
# Test
#----------------------------------------
def get_test(DBconn_):
	web = "https://www.anisearch.de/anime/15898,vivy-fluorite-eyes-song"
	soup = openpage.get_webpage(web)
	set_SQL_update_infordetails(DBconn_, soup, 10)
	return()

get_test(DBconn)















#list_unsync_anime_anisearch = get_SQL_unsyncList_anime_anisearch(DBconn):


#for row in list_unsync_anime_anisearch:
#	(id, site, name) = row
			
#	site = site.lstrip("#")
#	site = site.rstrip("#")
	
#	print("-----------------------------------")
#	print(site)

	
#	site_rela = site + "/relations"
#
#	soup = openpage.get_webpage(site)
#	soup_rela = openpage.get_webpage(site_rela)
#
#	if soup != "":
#		infosD = parser.get_infodetails(soup)
#		print(infosD)
#		descrip = parser.get_description(soup)
#		print(descrip)
#		nameA = parser.get_anisearchPrimaryKey(soup)
#		rating = parser.get_rating(soup)
#		animeNr = parser.get_anisearchPrimaryKey(site)
#		print(animeNr)
#	else:
#		print ("get_webpageparser: no html")
#
#	if soup_rela != "":
#		parser.get_relations(soup_rela)
#	else:
#		print("get_webpageparser: no html")
	
		
	





