'''
Created on 05.07.2021
@author: Ci
'''
import pyodbc
import sqlite3
import re
import logging
from logging import config
config.fileConfig("config/logging.conf")
logger = logging.getLogger("main")

try:
    import functions.get_configfile as confi
except ImportError:
    topdir = os.path.realpath(os.path.join(os.path.dirname(__file__)+".."))
    sys.path.insert(0,topdir)
    from functions import get_configfile as confi

try:
	import functions.get_webpageparser as pars
except ImportError:
	from functions import get_webpageparser as parser

try:
    import functions.get_sql_anime as sqlAni
except ImportError:
    topdir = os.path.realpath(os.path.join(os.path.dirname(__file__)+".."))
    sys.path.insert(0,topdir)
    from functions import get_sql_anime as sqlAni

# Object
connectAnimeDB = sqlAni.get_sql_anime()
parser         = pars.webparser_anisearch()
openpage       = pars.open_webpage()
config         = confi.get_configfile()
const_path_DB  = config.get_KeyValue("settings", "path_DB")





class set_sql_anime:
	# **************************************************************************
	# ********************* UPDATE FUNCTIONS ***********************************
	# **************************************************************************

	#----------------------------------------
	# Date: 2021.07.05
	# Name: set_SQL_update_infordetails
	# - update info details of the anime from anisearch
	# in:  DB connention, html raw, anisearch ID
	#----------------------------------------
	def set_SQL_update_infordetails(self, DBconn, soup, vID_Anisearch):
		results = ""
		vTyp = ""
		vEpisoden = ""
		vVeroeffentlicht = ""
		vHauptgenres = ""
		vHerkunft = ""
		vAdaptiert = ""
		vZielgruppe = ""

		infosD = parser.get_infodetails(soup)
		if infosD:
			if 'Typ'            in infosD: vTyp =       connectAnimeDB.get_SQL_TypeID(DBconn, infosD['Typ'])
			if 'Veröffentlicht' in infosD: vPubDate =   infosD['Veröffentlicht']
			if 'Hauptgenres'    in infosD: vGenre =     connectAnimeDB.get_SQL_GenreID(DBconn, infosD['Hauptgenres'])
			if 'Herkunft'       in infosD: vOrigin =    connectAnimeDB.get_SQL_originID(DBconn, infosD['Herkunft'])
			if 'Adaptiert von'  in infosD: vAdapt =     connectAnimeDB.get_SQL_AdaptionID(DBconn, infosD['Adaptiert von'])
			if 'Zielgruppe'     in infosD: vGroup =     connectAnimeDB.get_SQL_TargetGroupID(DBconn, infosD['Zielgruppe'])
			if 'Episoden'       in infosD: 
				strEpisoden = infosD['Episoden']
				strEpisoden = strEpisoden.encode("ascii", "replace").decode("utf-8") # replace unicode with ?
				replaced = re.sub('\?', ' ', strEpisoden)                            # replace ? with space
				x = re.findall(r'~[0-9 ]*min', replaced)
				y = re.findall("[0-9]* ", replaced)
				if x: vEpisoden_length = x[0]     
				else: vEpisoden_length = ''
				if x: vEpisoden_Nr = y[0].strip() 
				else: vEpisoden_Nr = ''
			

			#Check IF anime has already Content 
			strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :v_ID"
			conn = sqlite3.connect(DBconn)
			with conn:
				cursor = conn.cursor()
				cursor.execute(strSelectSQL, {"v_ID": vID_Anisearch})
				results = cursor.fetchall()

				
			# If NOT insert - else CONTENT update
			if not results:
				conn = sqlite3.connect(DBconn)
				with conn:
					cursor = conn.cursor()
					strInsertSQL = "INSERT INTO as_anime (ID, episodesnumber, length , publicationdate, fs_as_genre, fs_as_type, fs_as_origin, fs_as_adaption, fs_as_targetgroup) VALUES (:xID, :xepisNR, :xlength , :xpubdate, :xgenre, :xtype, :xorigin, :xadaption, :xtargetgroup)"
					cursor.execute(strInsertSQL,  {"xID": vID_Anisearch, "xepisNR": vEpisoden_Nr, "xlength": vEpisoden_length, "xpubdate": vPubDate, "xgenre": vGenre, "xtype": vTyp, "xorigin": vOrigin, "xadaption": vAdapt, "xtargetgroup": vGroup})
					conn.commit()
					logger.info('anime %s - added to database',vID_Anisearch)

			else:

				conn = sqlite3.connect(DBconn)
				# before
				with conn:
					cursor = conn.cursor()
					strSelectSQL = "SELECT as_anime.ID, as_anime.episodesnumber, as_anime.length , as_anime.publicationdate, as_anime.fs_as_genre, as_anime.fs_as_type, as_anime.fs_as_origin, as_anime.fs_as_adaption, as_anime.fs_as_targetgroup FROM as_anime WHERE as_anime.ID = :v_ID"
					cursor.execute(strSelectSQL,{"v_ID": vID_Anisearch})
					before = cursor.fetchall()
				# after
				after = "[("+str(vID_Anisearch)+", '"+str(vEpisoden_Nr)+"', '"+str(vEpisoden_length)+"', '"+str(vPubDate)+"', "+str(vGenre)+", "+str(vTyp)+", "+str(vOrigin)+", "+str(vAdapt)+", "+str(vGroup)+")]"

				if (str(before) == after):
					logger.info('anime %s - no change in database',vID_Anisearch)
				else:
					#action
					with conn:
						cursor = conn.cursor()
						strUpdatetSQL = "UPDATE as_anime SET episodesnumber=:xepisNR, length=:xlength , publicationdate=:xpubdate, fs_as_genre=:xgenre, fs_as_type=:xtype, fs_as_origin=:xorigin, fs_as_adaption=:xadaption, fs_as_targetgroup=:xtargetgroup WHERE as_anime.ID = :xID"
						cursor.execute(strUpdatetSQL,  {"xepisNR": vEpisoden_Nr, "xlength": vEpisoden_length, "xpubdate": vPubDate, "xgenre": vGenre, "xtype": vTyp, "xorigin": vOrigin, "xadaption": vAdapt, "xtargetgroup": vGroup, "xID": vID_Anisearch})
						conn.commit()
					logger.info('anime %s - changed in database  ',vID_Anisearch)

		return()

	#----------------------------------------
	# Date: 2021.07.05
	# Name: set_SQL_update_description
	# - update description of the anime from anisearch
	# in:  DB connention, html raw, anisearch Id
	#----------------------------------------
	def set_SQL_update_description(self, DBconn, soup, vID_Anisearch):
		description_de = ""
		description_en = ""

		infosD = parser.get_description(soup)
		if infosD:
			if 'en' in infosD: description_en = infosD['en']
			if 'de' in infosD: description_de = infosD['de']

			#Check IF anime has already Content 
			strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :xID"
			conn = sqlite3.connect(DBconn)
			with conn:
				cursor = conn.cursor()
				cursor.execute(strSelectSQL, {"xID": vID_Anisearch})
				results = cursor.fetchall()

			# If NOT insert - else CONTENT update
			if not results:
				conn = sqlite3.connect(DBconn)
				with conn:
					cursor = conn.cursor()
					strInsertSQL = "INSERT INTO as_anime (ID, description_en, description_de) VALUES (:xID, :xDE, :xEN)"
					cursor.execute(strInsertSQL,  {"xID": vID_Anisearch, "xDE": description_de, "xEN": description_en })
					conn.commit()
					logger.info('anime %s - added description',vID_Anisearch)
			else:
				conn = sqlite3.connect(DBconn)
				# before
				with conn:
					cursor = conn.cursor()
					strSelectSQL = "SELECT as_anime.ID, as_anime.description_en, as_anime.description_de FROM as_anime WHERE as_anime.ID = :v_ID"
					cursor.execute(strSelectSQL,{"v_ID": vID_Anisearch})
					before = cursor.fetchall()
				# after
				after = "[("+str(vID_Anisearch)+", '"+str(description_en)+"', '"+str(description_de)+"')]"
				
				if (str(before) == str(after)):
					logger.info('anime %s - no change for description',vID_Anisearch)
				else:
					#action
					with conn:
						cursor = conn.cursor()
						strUpdatetSQL = "UPDATE as_anime SET description_en=:xEN, description_de=:xDE  WHERE as_anime.ID = :xID"
						cursor.execute(strUpdatetSQL,  {"xID": vID_Anisearch, "xDE": description_de, "xEN": description_en })
						conn.commit()
						logger.info('anime %s - changed description',vID_Anisearch)

			
		return()



	#----------------------------------------
	# Date: 2021.07.05
	# Name: set_SQL_update_animename
	# - update anime name of the anime from anisearch
	# in:  DB connention, html raw, anisearch Id
	#----------------------------------------
	def set_SQL_update_animename(self, DBconn, soup, vID_Anisearch):
		animename_de = ""
		animename_en = ""
		animename_ja = ""

		infosD = parser.get_animename(soup)
		if infosD:
			if 'en' in infosD: animename_en = infosD['en']
			if 'de' in infosD: animename_de = infosD['de']
			if 'ja' in infosD: animename_ja = infosD['ja']
			
			
			#Check IF anime has already Content 
			strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :xID"
			conn = sqlite3.connect(DBconn)
			with conn:
				cursor = conn.cursor()
				cursor.execute(strSelectSQL, {"xID": vID_Anisearch})
				results = cursor.fetchall()

				
			# If NOT insert - else CONTENT update
			if not results:
				conn = sqlite3.connect(DBconn)
				with conn:
					cursor = conn.cursor()
					strInsertSQL = "INSERT INTO as_anime (ID, name_de, name_en, name_ja) VALUES (:xID, :xDE, :xEN, :xJA)"
					cursor.execute(strInsertSQL,  {"xID": vID_Anisearch, "xDE": animename_de, "xEN": animename_en, "xJA": animename_ja })
					conn.commit()
					logger.info('anime %s - added animename  ',vID_Anisearch)
			else:
				conn = sqlite3.connect(DBconn)
				with conn:
					cursor = conn.cursor()
					strUpdatetSQL = "UPDATE as_anime SET name_en=:xEN, name_de=:xDE, name_ja=:xJA  WHERE as_anime.ID = :xID"
					cursor.execute(strUpdatetSQL,  {"xID": vID_Anisearch, "xDE": animename_de, "xEN": animename_en, "xJA": animename_ja })
					conn.commit()
					logger.info('anime %s - changed animename  ',vID_Anisearch)
			
		return()

	#----------------------------------------
	# Date: 2021.07.05
	# Name: set_SQL_update_rating
	# - update rating of the anime from anisearch
	# in:  DB connention, html raw, anisearch Id
	#----------------------------------------
	def set_SQL_update_rating(self, DBconn, soup, vID_Anisearch):
		rating_per = ""
		rating_val = ""
		rating_ran = ""
		infosD = parser.get_rating(soup)
		if infosD:
			rating_val = infosD['rating_val']
			rating_per = infosD['rating_per']
			rating_ran = infosD['rating_rank']

			#Check IF anime has already Content 
			strSelectSQL = "SELECT as_anime.ID FROM as_anime WHERE as_anime.ID = :xID"
			conn = sqlite3.connect(DBconn)
			with conn:
				cursor = conn.cursor()
				cursor.execute(strSelectSQL, {"xID": vID_Anisearch})
				results = cursor.fetchall()


			# If NOT insert - else CONTENT update
			if not results:
				conn = sqlite3.connect(DBconn)
				with conn:
					cursor = conn.cursor()
					strInsertSQL = "INSERT INTO as_anime (ID, rating_number, rating_percent, rating_rank) VALUES (:xID, :xNR, :xPE, :xRA)"
					cursor.execute(strInsertSQL,  {"xID": vID_Anisearch, "xNR": rating_val, "xPE": rating_per, "xRA": rating_ran })
					conn.commit()
					logger.info('anime %s - added rating     ',vID_Anisearch)
			else:
				conn = sqlite3.connect(DBconn)
				with conn:
					cursor = conn.cursor()
					strUpdatetSQL = "UPDATE as_anime SET rating_number=:xNR, rating_percent=:xPE, rating_rank=:xRA  WHERE as_anime.ID = :xID"
					cursor.execute(strUpdatetSQL,  {"xID": vID_Anisearch, "xNR": rating_val, "xPE": rating_per, "xRA": rating_ran })
					conn.commit()
					logger.info('anime %s - changed rating     ',vID_Anisearch)

		return()
		
	#----------------------------------------
	# Date: 2021.07.05
	# Name: set_SQL_update_anisearchPrimaryKey
	# - update primary key of anisearch in the anime table after the update process is finished. After this is set, the anime will not shwon in the toDo list anymore
	# in:  DB connection, anime ID, anisearch ID
	#----------------------------------------
	def set_SQL_update_anisearchPrimaryKey(self, DBconn, vID_Anime, vID_Anisearch):

		#Check IF anime has already Content 
		strUpdatetSQL = "UPDATE anime SET fs_as_anime=:xAS_ID WHERE anime.ID = :xID"
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			cursor.execute(strUpdatetSQL, {"xAS_ID": vID_Anisearch, "xID": vID_Anime})
			results = cursor.fetchall()

		return()



	#----------------------------------------
	# Date: 2021.08.02
	# Name: set_SQL_update_relations
	# in:  DB connention, html raw, anisearch Id
	# mainID -> toID
	#----------------------------------------
	def set_SQL_update_relations(self, DBconn, soup, vID_Anisearch):
		
		infosD = parser.get_relations(soup)
		if infosD:
			for relation in infosD:
				r_toID    = relation[0]
				r_link  = "https://www.anisearch.de/"  + relation[1]
				r_name  =  relation[2]
				r_lang  =  relation[3]
				h_rela  =  relation[4]
				h_short =  relation[5]


				
				# Prüfe , ob es die Beziehung schon gibt  main -> to

				
				#Check IF relation has already Content 
				strSelectSQL = "SELECT as_relation.ID FROM as_relation WHERE as_relation.fs_as_anime_main = :xfrom AND as_relation.fs_as_anime_to = :xto "
				conn = sqlite3.connect(DBconn)
				with conn:
					cursor = conn.cursor()
					cursor.execute(strSelectSQL, {"xfrom": vID_Anisearch, "xto": r_toID})
					results = cursor.fetchall()
				# If NOT insert - else CONTENT update
				if not results:
					conn = sqlite3.connect(DBconn)
					with conn:
						cursor = conn.cursor()
						strInsertSQL = "INSERT INTO as_relation (fs_as_anime_main, fs_as_anime_to, name, name_language, link, relation_description, relation_direct) VALUES (:xfrom, :xto, :xName, :xLang, :xLink, :xDesc, :xDirc)"
						cursor.execute(strInsertSQL,  {"xfrom":vID_Anisearch, "xto":r_toID, "xName":r_name, "xLang":r_lang, "xLink":r_link, "xDesc":h_rela, "xDirc":h_short})
						conn.commit()
						logger.info('anime %s - added relations   %s to %s - %s',vID_Anisearch, vID_Anisearch, r_toID, r_name)
				else:
					xid = results[0][0]
					conn = sqlite3.connect(DBconn)
					with conn:
						cursor = conn.cursor()
						strUpdatetSQL = "UPDATE as_relation SET name=:xName, name_language=:xLang, link=:xLink, relation_description=:xDesc, relation_direct=:xDirc WHERE as_relation.ID = :xID"
						cursor.execute(strUpdatetSQL,  {"xfrom":vID_Anisearch, "xto":r_toID, "xName":r_name, "xLang":r_lang,  "xLink":r_link, "xDesc":h_rela, "xDirc":h_short, "xID":xid})
						conn.commit()
						logger.info('anime %s - changed relations   %s to %s - %s',vID_Anisearch, vID_Anisearch, r_toID, r_name)
		return()


#----------------------------------------
# Date: 2021.07.05
# Name: start_anisearSyncro
# in:   DB connection
#----------------------------------------
def start_anisearSyncro(connection):
	sq = set_sql_anime()
	list_unsync_anime_anisearch = connectAnimeDB.get_SQL_unsyncList_anime_anisearch(connection)
	vAS_Soup_rela = ""
	vAS_NR = "44"

	for row in list_unsync_anime_anisearch:
		(id, vAS_Link, name) = row
				
		vAS_Link = vAS_Link.lstrip("#")
		vAS_Link = vAS_Link.rstrip("#")
		
		print("-----------------------------------")
		print(vAS_Link)

		vAS_Soup = openpage.get_webpage(vAS_Link)
		vAS_Link_rela = vAS_Link + "/relations"
		vAS_Soup_rela = openpage.get_webpage(vAS_Link_rela)
		vAS_NR = parser.get_anisearchPrimaryKey(vAS_Link)
		
		sq.set_SQL_update_infordetails(connection, vAS_Soup, vAS_NR)
		sq.set_SQL_update_description(connection, vAS_Soup, vAS_NR)
		sq.set_SQL_update_animename(connection, vAS_Soup, vAS_NR)
		sq.set_SQL_update_rating(connection, vAS_Soup, vAS_NR)
		sq.set_SQL_update_relations(connection, vAS_Soup_rela, vAS_NR)
		#sq.set_SQL_update_anisearchPrimaryKey(connection, id, vAS_NR)
		
		break

	return()
	
# MAIN

start_anisearSyncro(const_path_DB)





