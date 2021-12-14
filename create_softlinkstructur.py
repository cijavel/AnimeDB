import igraph
import sqlite3
import igraph as ig

try:
    import functions.get_configfile as confi
except ImportError:
    topdir = os.path.realpath(os.path.join(os.path.dirname(__file__)+".."))
    sys.path.insert(0,topdir)
    from functions import get_configfile as confi

config               = confi.get_configfile()
const_path_DB        = config.get_KeyValue("settings", "path_DB")


def create_softlinkstructure(DBconn):
	arr_trans = {}
	edges_trans = []
	
	#Check IF anime has already Content 
	strSelectSQL = "SELECT count(ID) from anime;"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL)
		results_count = cursor.fetchall()

	strSelectSQL2 = "SELECT fs_as_anime, foldername from anime;"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL2)
		results = cursor.fetchall()
	
	
	strSelectSQL3 = "SELECT fs_as_anime_main, fs_as_anime_to from as_relation;"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL3)
		edges = cursor.fetchall()
		
	
	# Create a directed graph
	g = ig.Graph(directed=True)# Add 1347 Animes
	g.add_vertices(results_count[0][0])

	# Add ids and labels to vertices

	for i in range(len(g.vs)):
		g.vs[i]["id"]= results[i][0]
		g.vs[i]["label"]= results[i][1]
		arr_trans[results[i][0]] = i
	
	# Add edges
	for e in edges:

		found_from = -1
		found_to = -1
		
		
		
		found_from = arr_trans.get(e[0])
		found_to = arr_trans.get(e[1])
		
		if found_from != None and found_to != None:
			edges_trans.append([found_from,found_to])
			#print(str(e) + " -- > " + str(found_from) + " , " + str(found_to))

	
	g.add_edges(edges_trans)# Add weights and edge labels
	
	
	visual_style = {}
	out_name = "graph.png"					# Set bbox and margin
	visual_style["bbox"] = (8000,8000)
	visual_style["margin"] = 27				# Set vertex colours
	visual_style["vertex_color"] = 'white'	# Set vertex size
	visual_style["vertex_size"] = 30		# Set vertex lable size
	visual_style["vertex_label_size"] = 12	# Don't curve the edges
	visual_style["edge_curved"] = False		# Set the layout
	
	my_layout = g.layout_lgl()
	visual_style["layout"] = my_layout# Plot the graph
	ig.plot(g, out_name, **visual_style)
	
	
	
	#weights = [8,6,3,5,6,4,9]
	#g.es['weight'] = weights
	#g.es['label'] = weights

create_softlinkstructure(const_path_DB)