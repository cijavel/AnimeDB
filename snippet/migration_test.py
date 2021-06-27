
import pyodbc
import re
import sqlite3

def sync_Festplatte_storage():

	DBconn = "DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\DEPLOYMENT\PHYTON\ANIMEDB\Anime.mdb;"

	conn = pyodbc.connect(DBconn)

	with conn:
		cursor = conn.cursor()
		cursor.execute("SELECT ID, Name, Groesse, Jahr FROM Festplatte")

		festplatte = cursor.fetchall()

	for id, name, gross, jahr in festplatte:

		connection = sqlite3.connect("animeDB.db")

		# Datensatz-Cursor erzeugen
		cursor = connection.cursor()

		# Datenbanktabelle erzeugen
		sql = "INSERT INTO storage (storagename, size, year) VALUES (?, ? , ?)"
		cursor.execute(sql, (name, gross, jahr))
		connection.commit()
		connection.close()

def sync_genre():

	DBconn = "DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\DEPLOYMENT\PHYTON\ANIMEDB\Anime.mdb;"

	conn = pyodbc.connect(DBconn)

	with conn:
		cursor = conn.cursor()
		cursor.execute("SELECT ID, Genre FROM Genre")

		festplatte = cursor.fetchall()
		print(festplatte)

	for id, genre in festplatte:
		print(id)
		print(genre)

		connection = sqlite3.connect("animeDB.db")

		# Datensatz-Cursor erzeugen
		cursor = connection.cursor()

		# Datenbanktabelle erzeugen
		sql = "INSERT INTO as_genre (genre) VALUES (?)"
		cursor.execute(sql, (genre,))
		connection.commit()
		connection.close()
		
#***********************************************************************************************************************************************************
#***********************************************************************************************************************************************************
#***********************************************************************************************************************************************************



#----------------------------------------
# set_SQL_update_nisearchPrimaryKey
# string
#----------------------------------------
def get_anisearch_clear_link(link):
	if link is not None:
		try:
			link = link.replace("#", "")
		except:
			print("ERROR - get_anisearch_clear_link - please check link: " + link )
		
	return link








#***********************************************************************************************************************************************************
#***********************************************************************************************************************************************************



#----------------------------------------
# sync_Anime
# string
#----------------------------------------
def sync_Anime():
	DBconn = "DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\DEPLOYMENT\PHYTON\ANIMEDB\Anime.mdb;"

	conn = pyodbc.connect(DBconn)

	with conn:
		cursor = conn.cursor()
		cursor.execute("SELECT ID, name, Festplatte, anisearch_de, Bewertung, Gruppe, Kommentar, Sprache, Datum FROM anime")
		festplatte = cursor.fetchall()
		
	#for ID in festplatte:
	#	print(ID)


	for ID, name, Festp, anisearch_de, Bewertung, Gruppe, Kommentar, Sprache, Datum in festplatte:

		connection = sqlite3.connect("animeDB.db")
		# Datensatz-Cursor erzeugen
		cursor = connection.cursor()
		
		# Datenbanktabelle erzeugen
		sql = "INSERT INTO anime (foldername, fs_savelocation, anisearch_link, rating, fansubgroup, comment, fs_sprache, entrydate ) VALUES (?, ?, ? , ?, ?, ?, ?, ?, ?)"
		print(ID, name)
		cursor.execute(sql, (name, Festp, get_anisearch_clear_link(anisearch_de), Bewertung, Gruppe, Kommentar, Sprache, Datum ))	

		connection.commit()
		connection.close()
			



















