'''
Created on 05.07.2021
@author: Ci
'''

import os
import pylev
import re
import sqlite3
import termtables
import shutil
from datetime import date


try:
    import functions.get_configfile as confi
except ImportError:
    topdir = os.path.realpath(os.path.join(os.path.dirname(__file__)+".."))
    sys.path.insert(0,topdir)
    from functions import get_configfile as confi

try:
    import functions.get_sql_anime as sqlAni
except ImportError:
    topdir = os.path.realpath(os.path.join(os.path.dirname(__file__)+".."))
    sys.path.insert(0,topdir)
    from functions import get_sql_anime as sqlAni

# Object

config = confi.get_configfile()
path_DB				= config.get_KeyValue("settings", "path_DB")
path_serienimport 	= config.get_KeyValue("serienImport", "path_serienimport")
first_language 		= config.get_KeyValue("serienImport", "first_language")
storage 			= config.get_KeyValue("serienImport", "storage")
const_importedDIR                       = config.get_KeyValue("serienImport", "importedDIR")

connectAnimeDB = sqlAni.get_sql_anime()

#----------------------------------------
# Date: 2021.07.07
# Name: get_levenshtein_percent
# - get levenshtein as percent
#----------------------------------------
def get_levenshtein_percent(string1, string2, kommastelle):
	
	if (string1) or (string2):
		if len(string1) <= len(string2):
			max_lenght = len(string2)
		else:
			max_lenght = len(string1)
			
		percent = (1 - ( pylev.levenshtein(string1, string2) / max_lenght ))*100

		return(round(percent, kommastelle))
	else:
		print("get_levenshtein_percent - both strings are empty")
		return ()

#----------------------------------------
# Date: 2021.07.07
# Name: get_onlyName
# - abstract anime name from folder name
#----------------------------------------
def get_onlyName(name):
	if name:
		name = re.sub('\[[a-zA-Z0-9_ .-]+\]', '', name)
		
	return name.rstrip(" ")
	
#----------------------------------------
# Date: 2021.07.07
# Name: get_folder
# - get folders from os path
#----------------------------------------
def get_folder(path_serienimport):
	if path_serienimport:
		folder = []
		directory_contents = os.listdir(path_serienimport)
		if path_serienimport == ".":
			path = os.getcwd()
		else:
			path = path_serienimport
			
		print(path)
		for item in directory_contents:
			if os.path.isdir(path + "\\" + "\\" + item) and item != const_importedDIR:
				folder.append(item)
		return (folder)
	else:
		print("get_folder - no path in config file")
		return ()


#----------------------------------------
# Date: 2021.07.07
# Name: check_for_anime_in_DB
# - check if anime already in DB
#----------------------------------------
def check_for_anime_in_DB(DBconn):
	anime = connectAnimeDB.get_SQL_all_animefoldername(DBconn)
	folder = get_folder(path_serienimport)
	viewtable = []
	i = 0
	
	if folder:
		for fname in folder:
			iId2 = 0
			iId1 = 0
			aniName = ""
			i = i + 1
			for a in anime:
				extractName = get_onlyName(fname)
				iId = get_levenshtein_percent(get_onlyName(extractName), a[0], 2)

				if(iId2 < iId):
					iId2 = iId
					aniName = a[0]
			if iId2 > 80:
				viewtable.append([i, "*", str(iId2), fname, extractName,  aniName, ""])
			else:
				viewtable.append([i, "", str(iId2),  fname, extractName,  aniName, ""])
			
		header = ["ID", " ", "prozent", "folder", "search for",  "found", "move"]
		termtables.print( viewtable, header=header,  style="            -  ")
		
		# choose_to_move
		for h in viewtable:
			eingabe = ""
			a = []
			a.append(h)
			print("")
			print("-----------------------------------------------------------------")
			header = ["ID", " ", "prozent", "folder", "search for",  "found", "move"]
			termtables.print( a, header=header,  style="               ")
			print("")
			eingabe = input("don't move ?  ")
			h[6] = eingabe
		
		return(viewtable)
	else:
		print("check_for_anime_in_DB - there is no folder")
		return()

#----------------------------------------
# Date: 2021.07.10
# Name: change_to_dict
# - check if anime already in DB
#----------------------------------------
def change_to_dict(list_of_animes):
	header = ["ID", " ", "prozent", "folder", "search for",  "found", "move"]
	
	dict = {}
	list = []
	if list_of_animes:
		for i in list_of_animes:
			dict = {}
			dict["ID"] 		= i[0]
			dict["prozent"] = i[2]
			dict["folder"]	= i[3]
			dict["search"]	= i[4]
			dict["found"]	= i[5]
			dict["move"]	= i[6]
			list.append(dict)
	else:
		print("change_to_dict - no list")
	return(list)




#----------------------------------------
# Date: 2021.07.07
# Name: check_for_anime_in_DB
# - check if anime already in DB
#----------------------------------------
def insert_anime_in_DB(DBconn, list_of_anime):
	conn = sqlite3.connect(DBconn)
	todayformat = date.today().strftime("%d.%m.%Y")
	storageID = connectAnimeDB.get_SQL_StorageID(path_DB, storage)
	first_languageID  = connectAnimeDB.get_SQL_spracheID(path_DB, first_language)

	if list_of_anime:
		for a in list_of_anime:
			folder = a["folder"]
			mov = a["move"]
			if mov == "y":
				with conn:
					cursor = conn.cursor()
					strInsertSQL = "INSERT INTO anime (foldername, fs_storage, fs_sprache, entrydate) VALUES (:xfolder, :xSto, :xSpr, :xdat)"
					cursor.execute(strInsertSQL,  {"xfolder": folder, "xSto": storageID, "xSpr": first_languageID, "xdat": todayformat })
					conn.commit()
				print("Add Anime (" + folder + ") to DB")
	else:
		print("insert_anime_in_DB - no folder list")



	return()

#----------------------------------------
# Date: 2021.07.07
# Name: moving_folder
# - move folder with dict
#----------------------------------------
def moving_folder(list_of_anime):
	if list_of_anime:
		for h in list_of_anime:
			folder = h["folder"]
			mov = h["move"]
			if mov =="y":
				original = path_serienimport  + "\\" + folder
				target = path_serienimport + "\\" + const_importedDIR + "\\" + folder
				shutil.move(original,target)
				print("move folder (" + folder + ") to " + const_importedDIR)
	else:
		print("moving_folder - no folder list")
	return()





# MAIN
list_of_animes = check_for_anime_in_DB(path_DB)
dirct = change_to_dict(list_of_animes)
moving_folder(dirct)
insert_anime_in_DB(path_DB, dirct)












