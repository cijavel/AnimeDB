import pyodbc

conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\DEPLOYMENT\PHYTON\DBTEST\Anime.mdb;')
cursor = conn.cursor()


#strSQL_anz = 'SELECT count(Anime.ID) FROM Anime WHERE ((Anime.anisearch_sync=False) AND (Anime.anisearch_de IS NOT NULL))'
#strSQL_list = 'SELECT Anime.ID, Anime.Name, Anime.anisearch_sync, Anime.anisearch_de FROM Anime WHERE ((Anime.anisearch_sync=False) AND (Anime.anisearch_de IS NOT NULL))'

strSQL = "UPDATE Anime SET  Anime.Folgenanzahl = '1', Anime.anisearch_sync = 0  WHERE Anime.ID = 10 "


strSQL_list = 'SELECT Anime.ID, Anime.Name,  Anime.Folgenanzahl,  Anime.anisearch_sync FROM Anime WHERE Anime.ID = 10'
strSQL_list = "SELECT Genre.ID, Genre.Genre FROM Genre "

cursor.execute(strSQL_list)

ara_list = cursor.fetchall()
for row in ara_list:
	print (row)
	
	
cursor.execute(strSQL) 


cursor.execute(strSQL_list)
ara_list = cursor.fetchall()

conn.commit()

for row in ara_list:
	print (row)
	
	


    

      

       


    
