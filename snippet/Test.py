import pyodbc

def SQL_anisearch_sync():
	strSQL_list = 'SELECT Anime.ID, Anime.anisearch_de, Anime.Name FROM Anime WHERE ((Anime.anisearch_sync=False) AND (Anime.anisearch_de IS NOT NULL))'
	conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\DEPLOYMENT\PHYTON\DBTEST\Anime.mdb;')
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSQL_list)
		ara_list = cursor.fetchall()

	return(ara_list)
	

	
ara_list3 = SQL_anisearch_sync()

urli ="https://www.anisearch.de/anime/11174,udon-no-kuni-no-kiniro-kemari"


for row in ara_list3:
	(id, link, name) = row
			
	link = link.lstrip("#")
	link = link.rstrip("#")
	
	#print("--")
	#print(id)
	#print(link)
	#print(name)

