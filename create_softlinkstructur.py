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
trans_asr_i = {}
trans_i_asr = {}
edges_trans = []

def create_softlinkstructure(DBconn):

	
	#Check IF anime has already Content 
	strSelectSQL = "SELECT count(ID) from anime WHERE fs_as_anime IS NOT NULL;"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL)
		results_anime_count = cursor.fetchall()

	strSelectSQL2 = "SELECT fs_as_anime, foldername from anime WHERE fs_as_anime IS NOT NULL;"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL2)
		results_anime_anisearch = cursor.fetchall()
	
	
	strSelectSQL3 = "SELECT asr.fs_as_anime_from, asr.fs_as_anime_to from as_relation as asr WHERE asr.fs_as_anime_to IN (SELECT a.fs_as_anime from anime as a WHERE a.fs_as_anime IS NOT NULL) AND asr.fs_as_anime_from != asr.fs_as_anime_to;"
	conn = sqlite3.connect(DBconn)
	with conn:
		cursor = conn.cursor()
		cursor.execute(strSelectSQL3)
		anime_edges = cursor.fetchall()
		
	
	# Create a directed graph
	g = ig.Graph(directed=False)# Add 1347 Animes
	g.add_vertices(results_anime_count[0][0])

	# Add ids and labels to vertices
	for i in range(len(g.vs)):
		g.vs[i]["id"]= results_anime_anisearch[i][0]
		g.vs[i]["label"]= results_anime_anisearch[i][1]
		trans_asr_i[results_anime_anisearch[i][0]] = i
	
	# Add edges
	for e in anime_edges:

		found_from = -1
		found_to = -1

		found_from = trans_asr_i.get(e[0])
		found_to = trans_asr_i.get(e[1])
		
		if found_from != None and found_to != None:
			edges_trans.append([found_from,found_to])
			#print(str(e) + " -- > " + str(found_from) + " , " + str(found_to))

	
	g.add_edges(edges_trans)# Add weights and edge labels
	
	visual_style = {}
	out_name = "graph.png"					# Set bbox and margin
	visual_style["bbox"] = (8000,8000)
	visual_style["margin"] = 27				# Set vertex colours
	visual_style["vertex_color"] = 'white'	# Set vertex size
	visual_style["vertex_size"] = 10		# Set vertex lable size
	visual_style['vertex_label_dist'] = 1.5
	visual_style["vertex_label_size"] = 12	# Don't curve the edges
	visual_style["edge_curved"] = False		# Set the layout
	visual_style['vertex_label_color'] = 'black'
	visual_style['edge_color'] = '#C0C0C0'
	visual_style['vertex_color'] = ['#e6004c', '#9f25e6', '#2542e6', '#3deb74', '#97eb3d', '#ffe608', '#ffad08', '#ff0808']

	my_layout = g.layout_lgl()
	visual_style["layout"] = my_layout# Plot the graph
	ig.plot(g, out_name, **visual_style)
	
	sgs = g.decompose(mode="WEAK")
	
	j = 0
	for s in sgs:
		j = j + 1
		size = len(s.vs)
		visual_style["bbox"] = (size*120,size*120)
		ig.plot(s, "img//"+str(j) + out_name, **visual_style)
		
		for x in range(len(s.vs)):
			print(str(s.vs[x]["id"]) + " " + s.vs[x]["label"])
		print('---------------')
		

create_softlinkstructure(const_path_DB)