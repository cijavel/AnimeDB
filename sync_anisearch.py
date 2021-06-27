# ********************************************************************* 
import pyodbc
import sqlite3
import re

try:
    import functions.get_webpageparser as pars
except ImportError:
    from functions import get_webpageparser as parser

# Object
parser = pars.webparser_anisearch()
openpage = pars.open_webpage()




#----------------------------------------
# get_SQL_unsync_anime_anisearch - good
# -> list of results
# get the list of anime, which hasn't syncronized with anisearch jet - toDo List ;)
#----------------------------------------
def get_SQL_unsyncList_anime_anisearch(DBconn):
	strSQL = 'SELECT anime.ID, anime.anisearch_link, anime.foldername FROM anime WHERE (((anime.fs_as_anime IS NULL OR anime.fs_as_anime ="")) AND (anime.anisearch_link IS NOT NULL))'
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSQL)
		results = cursor.fetchall()
	return(results)


# **************************************************************************
# ********************* get Number for DB **********************************
# **************************************************************************

#----------------------------------------
# get_SQL_GenreID - good
# <- Name of genre
# -> number ID
# get ID from genre name
#----------------------------------------
def get_SQL_GenreID(DBconn, genreName):
	strSelectSQL = "SELECT as_genre.ID, as_genre.genre FROM as_genre WHERE as_genre.genre =:v_genre" 
	id = ""
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"v_genre": genreName})
		results = cursor.fetchall()
		
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_genre (genre) VALUES (:v_genre)"
			cursor.execute(strInsertSQL, {"v_genre": genreName})
			conn.commit()
			print(cursor.rowcount, "genre record(s) added ( " + genreName + " )" ) 
			cursor.execute(strSelectSQL, {"v_genre": genreName})
			results = cursor.fetchall()

	if results:
		for row in results:
			(id, name) = row	
	
	return(id)

#----------------------------------------
# get_SQL_TypeID - good
# <- Name of type
# -> number ID
# get ID from type name
#----------------------------------------
def get_SQL_TypeID(DBconn, typeName):
	strSelectSQL = "SELECT as_type.ID, as_type.type FROM as_type WHERE as_type.type = :v_type" 
	id = ""
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"v_type": typeName})
		results = cursor.fetchall()
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_type (type) VALUES (:v_type)"
			cursor.execute(strInsertSQL, {"v_type": typeName})
			conn.commit()
			print(cursor.rowcount, "Type record(s) added ( " + typeName + " )" ) 
			cursor.execute(strSelectSQL, {"v_type": typeName})
			results = cursor.fetchall()

	for row in results:
		(id, name) = row		
	
	return(id)

#----------------------------------------
# get_SQL_originID - good
# <- Name of origin
# -> number ID
# get ID from origin name
#----------------------------------------
def get_SQL_originID(DBconn, originName):
	strSelectSQL = "SELECT as_origin.ID, as_origin.origin FROM as_origin WHERE as_origin.origin = :v_origin" 
	id = ""
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"v_origin": originName})
		results = cursor.fetchall()
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_origin (origin) VALUES (:v_origin)"
			cursor.execute(strInsertSQL, {"v_origin": originName})
			conn.commit()
			print(cursor.rowcount, "origin record(s) added ( " + originName + " )" ) 
			cursor.execute(strSelectSQL, {"v_origin": originName})
			results = cursor.fetchall()

	for row in results:
		(id, name) = row		
	
	return(id)

#----------------------------------------
# get_SQL_AdaptionID - good
# <- Name of adaption
# -> number ID
# get ID from adaption name
#----------------------------------------
def get_SQL_AdaptionID(DBconn, AdaptionName):
	strSelectSQL = "SELECT as_adaption.ID, as_adaption.adaption FROM as_adaption WHERE as_adaption.adaption = :v_adaption" 
	id = ""
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"v_adaption": AdaptionName})
		results = cursor.fetchall()
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_adaption (adaption) VALUES (:v_adaption)"
			cursor.execute(strInsertSQL,  {"v_adaption": AdaptionName})
			conn.commit()
			print(cursor.rowcount, "Adaption record(s) added ( " + AdaptionName + " )" ) 
			cursor.execute(strSelectSQL,  {"v_adaption": AdaptionName})
			results = cursor.fetchall()

	for row in results:
		(id, name) = row		
	
	return(id)

#----------------------------------------
# get_SQL_TargetGroupID - good
# <- Name of target group
# -> number ID
# get ID from target group name
#----------------------------------------
def get_SQL_TargetGroupID(DBconn, GroupName):
	strSelectSQL = "SELECT as_targetgroup.ID, as_targetgroup.targetgroup FROM as_targetgroup WHERE as_targetgroup.targetgroup = :v_group" 
	id = ""
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"v_group": GroupName})
		results = cursor.fetchall()
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_targetgroup (targetgroup) VALUES (:v_group)"
			cursor.execute(strInsertSQL,  {"v_group": GroupName})
			conn.commit()
			print(cursor.rowcount, "target group record(s) added ( " + GroupName + " )" ) 
			cursor.execute(strSelectSQL,  {"v_group": GroupName})
			results = cursor.fetchall()

	for row in results:
		(id, name) = row		
	
	return(id)


# **************************************************************************
# ********************* UPDATE FUNCTIONS ***********************************
# **************************************************************************

#----------------------------------------
# set_SQL_update_infordetails - good
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

	infosD = parser.get_infodetails(soup)
	
	if 'Typ' 			in infosD: vTyp =         get_SQL_TypeID(DBconn, infosD['Typ'])
	if 'Veröffentlicht' in infosD: vPubDate = 	infosD['Veröffentlicht']
	if 'Hauptgenres' 	in infosD: vGenre = get_SQL_GenreID(DBconn, infosD['Hauptgenres'])
	if 'Herkunft' 		in infosD: vOrigin =    get_SQL_originID(DBconn, infosD['Herkunft'])
	if 'Adaptiert von'	in infosD: vAdapt =     get_SQL_AdaptionID(DBconn, infosD['Adaptiert von'])
	if 'Zielgruppe' 	in infosD: vGroup = 	get_SQL_TargetGroupID(DBconn, infosD['Zielgruppe'])
	if 'Episoden' 		in infosD: 
		strEpisoden = infosD['Episoden']
		x = re.findall("~[0-9]*min", strEpisoden)
		y = re.findall("[0-9]* ", strEpisoden)
		vEpisoden_length = x[0]
		vEpisoden_Nr = y[0].strip()
	

	#Check IF anime has already Content 
	strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :v_ID"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"v_ID": vID_Anime})
		results = cursor.fetchall()

		
	# If NOT insert - else CONTENT update
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_anime (ID, episodesnumber, length , publicationdate, fs_as_genre, fs_as_type, fs_as_origin, fs_as_adaption, fs_as_targetgroup) VALUES (:xID, :xepisNR, :xlength , :xpubdate, :xgenre, :xtype, :xorigin, :xadaption, :xtargetgroup)"
			cursor.execute(strInsertSQL,  {"xID": vID_Anime, "xepisNR": vEpisoden_Nr, "xlength": vEpisoden_length, "xpubdate": vPubDate, "xgenre": vGenre, "xtype": vTyp, "xorigin": vOrigin, "xadaption": vAdapt, "xtargetgroup": vGroup})
			conn.commit()
			print(cursor.rowcount, " record(s) added from anisearch for " + vID_Anime + ": infordetails") 
	else:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strUpdatetSQL = "UPDATE as_anime SET episodesnumber=:xepisNR, length=:xlength , publicationdate=:xpubdate, fs_as_genre=:xgenre, fs_as_type=:xtype, fs_as_origin=:xorigin, fs_as_adaption=:xadaption, fs_as_targetgroup=:xtargetgroup WHERE as_anime.ID = :xID"
			cursor.execute(strUpdatetSQL,  {"xepisNR": vEpisoden_Nr, "xlength": vEpisoden_length, "xpubdate": vPubDate, "xgenre": vGenre, "xtype": vTyp, "xorigin": vOrigin, "xadaption": vAdapt, "xtargetgroup": vGroup, "xID": vID_Anime})
			conn.commit()
			print(cursor.rowcount, " record(s) change from anisearch for " + vID_Anime + ": infordetails" ) 	
	
	return("Done")	

#----------------------------------------
# set_SQL_update_description - good
#----------------------------------------
def set_SQL_update_description(DBconn, soup, vID_Anime):
	description_de = ""
	description_en = ""

	
	infosD = parser.get_description(soup)

	if 'en' in infosD: description_en = infosD['en']
	if 'de' in infosD: description_de = infosD['de']
	
	
	#Check IF anime has already Content 
	strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :xID"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"xID": vID_Anime})
		results = cursor.fetchall()

		
	# If NOT insert - else CONTENT update
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_anime (ID, description_en, description_de) VALUES (:xID, :xDE, :xEN)"
			cursor.execute(strInsertSQL,  {"xID": vID_Anime, "xDE": description_de, "xEN": description_en })
			conn.commit()
			print(cursor.rowcount, " record(s) added from anisearch for " + vID_Anime + ": description") 
	else:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strUpdatetSQL = "UPDATE as_anime SET description_en=:xEN, description_de=:xDE  WHERE as_anime.ID = :xID"
			cursor.execute(strUpdatetSQL,  {"xID": vID_Anime, "xDE": description_de, "xEN": description_en })
			conn.commit()
			print(cursor.rowcount, " record(s) change from anisearch for " + vID_Anime + ": description" ) 
		
	return("Done")



#----------------------------------------
# set_SQL_update_animename - good
# string
#----------------------------------------
def set_SQL_update_animename(DBconn, soup, vID_Anime):
	animename_de = ""
	animename_en = ""
	animename_ja = ""

	infosD = parser.get_animename(soup)

	if 'en' in infosD: animename_en = infosD['en']
	if 'de' in infosD: animename_de = infosD['de']
	if 'ja' in infosD: animename_ja = infosD['ja']
	
	
	#Check IF anime has already Content 
	strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :xID"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"xID": vID_Anime})
		results = cursor.fetchall()

		
	# If NOT insert - else CONTENT update
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_anime (ID, name_de, name_en, name_ja) VALUES (:xID, :xDE, :xEN, :xJA)"
			cursor.execute(strInsertSQL,  {"xID": vID_Anime, "xDE": animename_de, "xEN": animename_en, "xJA": animename_ja })
			conn.commit()
			print(cursor.rowcount, " record(s) added from anisearch for " + vID_Anime + ": animename") 
	else:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strUpdatetSQL = "UPDATE as_anime SET name_en=:xEN, name_de=:xDE, name_ja=:xJA  WHERE as_anime.ID = :xID"
			cursor.execute(strUpdatetSQL,  {"xID": vID_Anime, "xDE": animename_de, "xEN": animename_en, "xJA": animename_ja })
			conn.commit()
			print(cursor.rowcount, " record(s) change from anisearch for " + vID_Anime + ": animename")
	
	return("done")

#----------------------------------------
# set_SQL_update_rating - good
# string
#----------------------------------------
def set_SQL_update_rating(DBconn, soup, vID_Anime):
	rating_per = ""
	rating_val = ""
	infosD = parser.get_rating(soup)
	rating_val = infosD[0]
	rating_per = infosD[1]
	
	
	#Check IF anime has already Content 
	strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :xID"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL, {"xID": vID_Anime})
		results = cursor.fetchall()

		
	# If NOT insert - else CONTENT update
	if not results:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strInsertSQL = "INSERT INTO as_anime (ID, rating_number, rating_percent) VALUES (:xID, :xNR, :xPE)"
			cursor.execute(strInsertSQL,  {"xID": vID_Anime, "xNR": rating_val, "xPE": rating_per })
			conn.commit()
			print(cursor.rowcount, " record(s) added from anisearch for " + vID_Anime + ": rating") 
	else:
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			strUpdatetSQL = "UPDATE as_anime SET rating_number=:xNR, rating_percent=:xPE  WHERE as_anime.ID = :xID"
			cursor.execute(strUpdatetSQL,  {"xID": vID_Anime, "xNR": rating_val, "xPE": rating_per })
			conn.commit()
			print(cursor.rowcount, " record(s) change from anisearch for " + vID_Anime + ": rating")
			
	return(0)

#----------------------------------------
# set_SQL_update_relations  XXXXXXXXXXXXXXXXXXXX
# string
#----------------------------------------
def set_SQL_update_relations(DBconn, soup, vID_Anime):

	
	infosD = parser.get_relations(soup)
	print(infosD)
	return(0)
	
	
	
#----------------------------------------
# set_SQL_update_nisearchPrimaryKey  XXXXXXXXXXXXXXXXXXXX
# string
#----------------------------------------
def set_SQL_update_anisearchPrimaryKey(DBconn, link):
	infosD = parser.get_anisearchPrimaryKey(link)
	print(infosD)
	return(0)



#----------------------------------------
# Test
#----------------------------------------
def get_test_parser(connection):
	animelink = "https://www.anisearch.de/anime/15898,vivy-fluorite-eyes-song"
	animeSoup = openpage.get_webpage(animelink)
	animelink_rela = animelink + "/relations"
	print(animelink_rela)
	animeSoup_rela = openpage.get_webpage(animelink_rela)
	print(animeSoup_rela)
	
	if animeSoup != "":
		animeInfosD = parser.get_infodetails(animeSoup)
		animeDescrip = parser.get_description(animeSoup)
		animeName = parser.get_animename(animeSoup)
		animeRating = parser.get_rating(animeSoup)
		animeNr = parser.get_anisearchPrimaryKey(animelink)
	else:
		print ("animeSoup: no html")
		
	if animeSoup_rela != "":
		animeRelations = parser.get_relations(animeSoup_rela)
	else:
		print("animeSoup_rela: no html")
	return()
	
def get_test_SQLids(connection):
	result = get_SQL_unsyncList_anime_anisearch(connection) # good
	for rs in result:
		print(rs)
	result = get_SQL_GenreID(connection, "-") # good
	print(result)
	result = get_SQL_TypeID(connection, "-") # good
	print(result)
	result = get_SQL_originID(connection, "-") # good
	print(result)
	result = get_SQL_AdaptionID(connection, "-") # good
	print(result)
	result = get_SQL_TargetGroupID(connection, "-") # good
	print(result)

	
	
	return()
	
	
#----------------------------------------
# start_anisearSyncro
#----------------------------------------
def start_anisearSyncro(connection):

	list_unsync_anime_anisearch = get_SQL_unsyncList_anime_anisearch(connection)

	for row in list_unsync_anime_anisearch:
		(id, animelink, name) = row
				
		animelink = animelink.lstrip("#")
		animelink = animelink.rstrip("#")
		
		print("-----------------------------------")
		print(animelink)
		
		animeSoup = openpage.get_webpage(animelink)
		animelink_rela = animelink + "/relations"
		animeSoup_rela = openpage.get_webpage(animelink_rela)
		animeNr = parser.get_anisearchPrimaryKey(animelink)	

		set_SQL_update_infordetails(connection, animeSoup, animeNr)
		set_SQL_update_description(connection, animeSoup, animeNr)
		set_SQL_update_animename(connection, animeSoup, animeNr)
		set_SQL_update_rating(connection, animeSoup, animeNr)
		set_SQL_update_relations(connection, animeSoup_rela, animeNr)
		
		break
	
	return()		
	
#variablen
connection = "animeDB.db"
start_anisearSyncro(connection)









