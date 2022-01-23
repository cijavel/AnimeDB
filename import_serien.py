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
from sys import platform






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
const_path_DB                           = config.get_KeyValue("settings", "path_DB")
const_path_serienimport                 = config.get_KeyValue("serienImport", "path_serienimport")
const_first_language                    = config.get_KeyValue("serienImport", "first_language")
const_storage                           = config.get_KeyValue("serienImport", "storage")
const_importedDIR                       = config.get_KeyValue("serienImport", "importedDIR")
const_levenshtein_distance_percent      = config.get_KeyValue("serienImport", "levenshtein_distance_percent")


# different between Linux and Windows T.T
if platform == "linux" or platform == "linux2":
	const_separator = '/'
elif platform == "darwin":
	const_separator = '/'
elif platform == "win32":
	const_separator = '\\'

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
# Name: get_extractAnimeNamefromDir
# - extract anime name from directory name
#----------------------------------------
def get_extractAnimeNamefromDir(name):
	if name:
		name = re.sub('\[[a-zA-Z0-9_ .-]+\]', '', name)

	return name.rstrip(" ")

#----------------------------------------
# Name: get_extractAnimeAttributefromDir
# - extract anime attribute from directory name
#----------------------------------------
def get_extractAnimeAttributefromDir(name):
	if name:
		name = re.findall('\[[a-zA-Z0-9_ .-]+\]',  name)
	return name

#----------------------------------------
# Name: get_languagefromFileName
# - extract anime name from directory name
#----------------------------------------
def get_languagefromFileName(nametable):
	cleartag = ""
	if nametable:
		for n in nametable:
			list_of = re.findall('\[[a-zA-Z]{5,6}\]',  n)

			for i in list_of:
				subtag = re.findall('[a-zA-Z]+', i)
				for cleartag in subtag:
					return cleartag


#----------------------------------------
# Name: get_subdirectories
# - get folders from os path
#----------------------------------------
def get_subdirectories():
	if const_path_serienimport:
		subdirectories = []
		directory_contents = os.listdir(const_path_serienimport)

		# get root path
		if const_path_serienimport == ".":
			path = os.getcwd()
		else:
			path = const_path_serienimport
			
		# check if subfolder
		for item in directory_contents:
			if os.path.isdir(path + const_separator + const_separator + item) and item != const_importedDIR:
				subdirectories.append(item)
		return (subdirectories)
	else:
		print("get_subdirectories - no path in config file")
		return ()


#----------------------------------------
# Date: 2021.07.07
# Name: check_levenshtein_for_anime_in_DB
# - check if anime already in DB
#----------------------------------------
def check_levenshtein_for_anime_in_DB(DBconn):
	all_animefoldername = connectAnimeDB.get_SQL_all_animefoldername(DBconn)
	subdirectories = get_subdirectories()
	viewtable = []
	i = 0
	
	if subdirectories:
		for fname in subdirectories:
			iDistanceCache01 = 0
			iDistanceCache02 = 0
			singleAnimeName = ""
			i = i + 1
			for singleAnime in all_animefoldername:
				extractName = get_extractAnimeNamefromDir(fname)
				iDistanceCache02 = get_levenshtein_percent(get_extractAnimeNamefromDir(fname), singleAnime[0], 2)

				if(iDistanceCache01 < iDistanceCache02):
					iDistanceCache01 = iDistanceCache02
					singleAnimeName = singleAnime[0]
			if iDistanceCache01 > float(const_levenshtein_distance_percent):
				viewtable.append([i, "*", str(iDistanceCache01), fname, extractName,  singleAnimeName, ""])
			else:
				viewtable.append([i, "", str(iDistanceCache01),  fname, extractName,  singleAnimeName, ""])
			
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
			eingabe = input("move? [y/N]: ")
			h[6] = eingabe
		
		return(viewtable)
	else:
		print("check_levenshtein_for_anime_in_DB - there is no folder")
		return()

#----------------------------------------
# Date: 2021.07.10
# Name: change_animelist_to_dict
#----------------------------------------
def change_animelist_to_dict(list_of_animes):
	header = ["ID", " ", "prozent", "folder", "search for",  "found", "move"]
	
	dict = {}
	list = []
	if list_of_animes:
		for i in list_of_animes:
			dict = {}
			dict["ID"]      = i[0]
			dict["prozent"] = i[2]
			dict["folder"]  = i[3]
			dict["search"]  = i[4]
			dict["found"]   = i[5]
			dict["move"]    = i[6]
			list.append(dict)
	else:
		print("change_animelist_to_dict - no list")
	return(list)


#----------------------------------------
# Date: 2021.07.07
# Name: insert_anime_in_DB
# - check if anime already in DB
#----------------------------------------
def insert_anime_in_DB(DBconn, list_of_anime):
	conn = sqlite3.connect(DBconn)
	todayformat = date.today().strftime("%Y.%m.%d")
	storageID = connectAnimeDB.get_SQL_StorageID(const_path_DB, const_storage )
	first_languageID  = connectAnimeDB.get_SQL_spracheID(const_path_DB, const_first_language)

	if list_of_anime:
		for a in list_of_anime:
			folder = a["folder"]
			mov = a["move"]
			if mov == "y":
				with conn:
					cursor = conn.cursor()
					strInsertSQL = "INSERT INTO anime (foldername, fs_storage, fs_sprache, entrydate) VALUES (:xfolder, :xSto, :xSpr, :xdat)"
					cursor.execute(strInsertSQL,  {"xfolder": get_extractAnimeNamefromDir(folder), "xSto": storageID, "xSpr": first_languageID, "xdat": todayformat })
					conn.commit()
				print("Add Anime (" + folder + ") to DB")
	else:
		print("insert_anime_in_DB - no folder list")
	return()

#----------------------------------------
# Date: 2021.08.01
# Name: move_dir_to_importedDIR
# - move a list of dir to the importedDIR. Only if value of the key 'move' = y
#----------------------------------------
def move_dir_to_importedDIR(list_of_dirs):
	if list_of_dirs:
		for singleDir in list_of_dirs:
			dirName = singleDir["folder"]
			mov    = singleDir["move"]
			if mov =="y":
				original = const_path_serienimport + const_separator + dirName
				target   = const_path_serienimport + const_separator + const_importedDIR + const_separator + dirName
				shutil.move(original,target)
				print("move directory (" + dirName + ") to " + const_importedDIR)
	else:
		print("move_dir_to_importedDIR - no directory list")
	return()



# MAIN
list_of_compared_animes  = check_levenshtein_for_anime_in_DB(const_path_DB)
dirct_of_anime = change_animelist_to_dict(list_of_compared_animes)
move_dir_to_importedDIR(dirct_of_anime)
insert_anime_in_DB(const_path_DB, dirct_of_anime)


