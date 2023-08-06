import json , re

from flask import url_for

from zohavi.zcommon import Utils

class JCFunc:
	######################################################################################################
	# Test function
	def test():
		return "hello JCFunc world"

	def defaulter(value, default):
		return value if value else default
	# def breakpoint():
	# 	breakpoint()


	def breakpoint(data):
		breakpoint()
		
	
	######################################################################################################
	# Take an existing list or dict, and then convert the field names from A to B
	def translate_obj(obj, field_mapping, field_inserts ): 
		new_obj = None

		if not obj: return []	

		if isinstance(obj, list):
			new_obj = []
			for item in obj:	#Look through each of the rows
				curr_row = {}

				for field in item:
					if field in field_mapping:	#for each of the field mapping - "field" = original field
						curr_row[ field_mapping[field] ] = item[ field ]
					else:
						curr_row[ field ] = item[ field ]

				# if field_inserts: breakpoint() 
				for curr_insert in field_inserts:	#Go through each of the insert items
					search_match = True
					for search_item in curr_insert["search"]:	#check if the search criteria matches.  if so, then add it to the item
					 	if not ( search_item in item and item[search_item] == curr_insert["search"][ search_item ] ) :
					 		search_match = False

					if search_match:  curr_row.update (    curr_insert[ "insert" ]  )
							
				new_obj.append( curr_row )

		else:
			raise Exception( 'error')
		# print( json.dumps( new_obj ) )
		# print('deondone')
		return json.dumps( new_obj )
		# return json.dumps( obj )
		# breakpoint()
	######################################################################################################
	# Helper function for set_elt_attribs() to render each attribute in a HTML tag
	def concat_dirs(base_dir, *sub_dirs):
		return Utils.concat_dirs( base_dir, *sub_dirs)
		# pass


	######################################################################################################
	# Helper function for set_elt_attribs() to render each attribute in a HTML tag
	def _set_elt_attribs_print_str(item, data_value ): 
		if isinstance(data_value, dict):
			# print( f"####:{data_value}")
			return f" {item}='{ json.dumps(data_value) }' "
		return f' {item}="{data_value}" '

	

	######################################################################################################
	# Set the attributes of a HTML tag where **defaults_dict will be added if no entry in the field provided
	def set_elt_attribs(field, **defaults_dict ):
		attrib_str = "" 
		for item in defaults_dict:
			if item in field: 
				attrib_str += JCFunc._set_elt_attribs_print_str( item, field[item] )
			else:
				attrib_str += JCFunc._set_elt_attribs_print_str( item, defaults_dict[item] )   

		print( f"****:{attrib_str}")
		return attrib_str

	######################################################################################################
	# expand the url from the config files
	# scenario 1: url_for:member.home
	# scenario 2: url_for:members.home?var1=abc 
	# scenario 3: url_for:members.home?var1=abc&var2=xyz
	# scenario 3: url_for:members.home?var1=abc&var2=[data_field] abd data_table is a hash containing key 'data_field'
	def extract_url_from_config_str(urlStr, data_table = None):
		strTokens = re.split("[:\?]", urlStr )		#split into two parts, first bit into main link, then param
		arg_hash = {}

		if( len(strTokens) > 2):					#if we have parameters
			arg_list = re.split("[=&]", strTokens[2] )	#split each parameter

			#create dictionary.  arg_list[::2] = every seond item, arg_list[1::2]  = every first item
			arg_hash = dict( zip( arg_list[::2], arg_list[1::2] ) ) 

			if data_table:			#if we have data to replace
				for key in arg_hash:
					if arg_hash[key].startswith("[") and arg_hash[key].endswith("]"):	#if we have a bracked item
						arg_hash[key] = data_table.get(arg_hash[key][1:-1], arg_hash[key])	#check if key exists in table
	 
		return strTokens[1], arg_hash


	######################################################################################################
	# Custom Template Function: try to convert url_string
	def render_url(urlStr, data_table = None):

		if 'url_for' in urlStr:
			# strTokens = urlStr.split(":")
			# logger.debug("Tokens:" + str(strTokens))
			(link, args) = JCFunc.extract_url_from_config_str( urlStr, data_table )

			return url_for( link , **args)
		else:
			return  urlStr

	######################################################################################################
	# Custom Template Function: try to get url string, if not exist, return blank
	def url_for_lazy(urlStr ):

		try:
			return url_for( urlStr );
		except Exception as e:
			# logger.debug(f"URL converstaion failed:{urlStr}")
			return ""
		 
	 ######################################################################################################
	# enable creation of lists using the SET command under JINJA
	def make_list(*list_items): 
		return list_items

		

