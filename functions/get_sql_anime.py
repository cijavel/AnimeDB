'''
Created on 10.07.2021
@author: Ci
'''

import os
import pylev
import sqlite3



class get_sql_anime:


	#----------------------------------------
	# Date: 2021.07.31
	# Name: get_SQL_all_animefoldername
	# - get anime names from DB
	#----------------------------------------
	def get_SQL_all_animefoldername(self, DBconn):
		strSelectSQL = "SELECT foldername FROM anime" 
		id = ""
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			cursor.execute(strSelectSQL)
			results = cursor.fetchall()
		return(results)

	
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_SQL_StorageID
	#----------------------------------------
	def get_SQL_StorageID(self, DBconn, storageName):
		strSelectSQL = "SELECT storage.ID, storage.storagename FROM storage WHERE storage.storagename =:v_storage" 
		id = ""
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			cursor.execute(strSelectSQL, {"v_storage": storageName})
			results = cursor.fetchall()
			
		if not results:
			conn = sqlite3.connect(DBconn)
			with conn:
				cursor = conn.cursor()
				strInsertSQL = "INSERT INTO storage (storagename) VALUES (:v_storage)"
				cursor.execute(strInsertSQL, {"v_storage": storageName})
				conn.commit()
				print(cursor.rowcount, "storage record(s) added ( " + storageName + " )" ) 
				cursor.execute(strSelectSQL, {"v_storage": storageName})
				results = cursor.fetchall()

		if results:
			for row in results:
				(id, name) = row	
		
		return(id)
		
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_SQL_spracheID
	#----------------------------------------
	def get_SQL_spracheID(self, DBconn, spracheName):
		strSelectSQL = "SELECT sprache.ID, sprache.sprache FROM sprache WHERE sprache.sprache =:v_sprache" 
		id = ""
		conn = sqlite3.connect(DBconn)
		with conn:
			cursor = conn.cursor()
			cursor.execute(strSelectSQL, {"v_sprache": spracheName})
			results = cursor.fetchall()
			
		if not results:
			conn = sqlite3.connect(DBconn)
			with conn:
				cursor = conn.cursor()
				strInsertSQL = "INSERT INTO sprache (sprache) VALUES (:v_sprache)"
				cursor.execute(strInsertSQL, {"v_sprache": spracheName})
				conn.commit()
				print(cursor.rowcount, "sprache record(s) added ( " + spracheName + " )" ) 
				cursor.execute(strSelectSQL, {"v_sprache": spracheName})
				results = cursor.fetchall()

		if results:
			for row in results:
				(id, name) = row	
		
		return(id)		
		
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_SQL_unsync_anime_anisearch
	# - get the list of anime, which hasn't syncronized with anisearch jet - toDo List ;)
	# in:  DB connention
	# out: list of unsync animes
	#----------------------------------------
	def get_SQL_unsyncList_anime_anisearch(self, DBconn):
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
	# Date: 2021.07.05
	# Name: get_SQL_GenreID
	# - get ID from genre name
	# in:  Name of genre, DB connention
	# out: ID of genre
	#----------------------------------------
	def get_SQL_GenreID(self, DBconn, genreName):
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
	# Date: 2021.07.05
	# Name: get_SQL_TypeID
	# - get ID from type name
	# in:  Name of type, DB connention
	# out: ID of type
	#----------------------------------------
	def get_SQL_TypeID(self, DBconn, typeName):
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
	# Date: 2021.07.05
	# Name: get_SQL_originID
	# - get ID from origin name
	# in:  Name of origin, DB connention
	# out: ID of origin
	#----------------------------------------
	def get_SQL_originID(self, DBconn, originName):
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
	# Date: 2021.07.05
	# Name: get_SQL_AdaptionID
	# - get ID from adaption name
	# in:  Name of adaption, DB connention
	# out: ID of adaption
	#----------------------------------------
	def get_SQL_AdaptionID(self, DBconn, AdaptionName):
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
	# Date: 2021.07.05
	# Name: get_SQL_TargetGroupID
	# - get ID from target group name
	# in:  Name of target group, DB connention
	# out: ID of target group
	#----------------------------------------
	def get_SQL_TargetGroupID(self, DBconn, GroupName):
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
		