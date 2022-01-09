import pylev
import sqlite3


try:
    import functions.get_configfile as confi
except ImportError:
    topdir = os.path.realpath(os.path.join(os.path.dirname(__file__)+".."))
    sys.path.insert(0,topdir)
    from functions import get_configfile as confi

config               = confi.get_configfile()
const_path_DB        = config.get_KeyValue("settings", "path_DB")


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
		

def check_anisearchlinks(DBconn):

	#Check IF anime has already Content 
	strSelectSQL = "SELECT id,fs_as_anime, foldername,anisearch_link from anime WHERE fs_as_anime IS NOT NULL;"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL)
		list_of_animes  = cursor.fetchall()


		for a in list_of_animes:
			anime_id = a[1]
			anime_name = a[2]
			anime_link = a[3]

			x = anime_link.replace("https://www.anisearch.de/anime/", "")
			x = x.replace(str(anime_id), "")
			x = x.replace(",", "")
			x = x.replace("-", " ")
			DistanceCache = get_levenshtein_percent(x, anime_name.lower(), 1)
			
			if DistanceCache < 75:
				print(str(DistanceCache))
				print("DB: " +  anime_name)
				print("LK: " +  x )
			#replaced = re.sub('\?', ' ', strEpisoden) 
			#x = re.findall(r'~[0-9 ]*min', replaced)
			#y = re.findall("[0-9]* ", replaced)



		

check_anisearchlinks(const_path_DB)