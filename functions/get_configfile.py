'''
Created on 05.07.2021
@author: Ci
'''


import configparser

file = 'config.ini'

class get_configfile:
	
	
	#----------------------------------------
	# Date: 2021.07.05
	# Name: __init__
	# 
	#----------------------------------------  
	def __init__(self):
		config = configparser.ConfigParser()
		try:
			config.read(file)   
		except:
			print("No config.ini found. Generate default config.ini")
			get_configfile.create_defaultconfiguration(self)

	#----------------------------------------
	# Date: 2021.07.05
	# Name: check_exist_of_config
	# - check if there is a config file
	#----------------------------------------
	def check_exist_of_config(self):
		try:
			with open(file, 'r') as f:
				return True	  
		except FileNotFoundError:
			print("No config.ini found. Generate default config.ini")
			get_configfile.create_defaultconfiguration(self)
			return -1
		except IOError:
			print ("Could not read file: %s", file)
			return -1
		return ()
		

	#----------------------------------------
	# Name: create_defaultconfiguration
	# - create a default config files
	#----------------------------------------
	def create_defaultconfiguration(self):
		config = configparser.ConfigParser()
		config['settings']={'path_DB':'animeDB.db'}
		config['serienImport'] = {
			'path_serienimport':'.',
			'importedDIR':'-imported-',
			'first_language':'GerSub',
			'storage':'NAS'}
		with open(file, 'w') as get_configfile:
			config.write(get_configfile)
		return ()

	

	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_KeyallItems
	# - get all keyitems
	#----------------------------------------			
	def get_KeyallItems(self):
		config = configparser.ConfigParser()
		get_configfile.check_exist_of_config(self)
		config.read(file)
		listi = []
		for section in config.sections():
			for option in config.options(section):
				value = config.get(section, option)
				listi.append([option,section, value])
		return listi	
	
	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_KeyallItemsinSection
	# - get all items of the section
	#----------------------------------------	
	def get_KeyallItemsinSection(self, categori):
		config = configparser.ConfigParser()
		get_configfile.check_exist_of_config(self)
		config.read(file)
		return config.items(categori)

	#----------------------------------------
	# Date: 2021.07.05
	# Name: get_KeyValue
	# - get value of an item
	#----------------------------------------
	def get_KeyValue(self, categori, key):
		config = configparser.ConfigParser()
		get_configfile.check_exist_of_config(self)
		config.read(file)	
		
		return config.get(categori, key)
	
	#----------------------------------------
	# Date: 2021.07.05
	# Name: set_KeyItem
	# - set value of an item
	#----------------------------------------
	def set_KeyItem(self,categori, key, text ):
		config = configparser.ConfigParser()
		get_configfile.check_exist_of_config(self)
		config.write(get_configfile)
		config.set(categori, key, text)				
		return ()   



