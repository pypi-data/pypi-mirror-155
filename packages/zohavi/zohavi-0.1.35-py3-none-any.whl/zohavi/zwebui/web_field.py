import re, json 

from zohavi.zbase.staple import Staple
from mclogger import MCLogger

class WebField( Staple ):
	def __init__(self, fields, app=None, logger=None):
		super().__init__(app = app, logger = logger )
		self.debug = True

		self._fields = fields
		self._calc_web_field_lookup()

		self.log_debug(f"Stored: {json.dumps(fields) }")

	def get_field(self, field_name):
		# for field in self._fields:
		# 	if field['id'] == field_name: return field
		return self._fields[field_name]

	def _calc_web_field_lookup(self):
		self._field_lookup = {}
		for table_name in self._fields.keys():
			#create new dict entry for each of the web fields
			for web_field_name in self._fields[table_name]['fields'].keys():
				self._field_lookup[ web_field_name ] =  table_name 

	#############################################################################################################
	#Validate form data in json format
	@MCLogger.logfunc_cls('logger')
	def validate(self, data):
		validation_ok = True 
		logger.debug( "validating:" + json.dumps(data ) )
		logger.debug( "Master:" + json.dumps(self._fields ) )

		for data_row in data:	#loop through each web data field
			web_field_name = data_row['id']
			table_name = self._field_lookup[ web_field_name ]

			field_info = self._fields[table_name]['fields'][ web_field_name ]

			if field_info.get('validation', False):  #has validation
				self.log_debug( f" Checking validation {table_name}-{web_field_name}=>[{data_row['value']}] Rule:{json.dumps( field_info['validation']) } ") 

				validation_ok = validation_ok and self._validate_run_validation_rule( data_row['value'] , field_info['validation']  )

			if field_info.get('transform', False):  #has transformation
				data_row['value'] = self._run_transformation( data_row['value'] , field_info['transform'] )
		return validation_ok


	#############################################################################################################
	#
	def _run_transformation(self, data_value, transform_rules):
		logger.debug( f" data_value={data_value}; transform={json.dumps(transform_rules) }")

		ret_value = data_value
		for rule in transform_rules: 
			func = getattr(Transform, rule, Transform._func_not_found)  
			ret_value = func( ret_value , transform_rules[rule] )

		return ret_value


	#############################################################################################################
	#Run the actual validation rule
	def _validate_run_validation_rule(self, data_value, validation_rules):
		validation_ok = True 
		# if not data_value: breakpoint()
		self.log_debug( f" data_value={data_value}; validation_rule={'required' in validation_rules.keys()}; required={validation_rules['required']== False}")
		if not data_value and 'required' in validation_rules.keys() and validation_rules['required'] == False: return True
		for rule in validation_rules: 
			func = getattr(Validate, rule, Validate._func_not_found)  
			ret_check = func( data_value , validation_rules[rule])

			log_message = f"Validation check [{rule}:{validation_rules[rule]}] on [{data_value}] => {ret_check}"
			self.log_debug( log_message ) if ret_check else logger.error( log_message )

			validation_ok = validation_ok and ret_check


		self.log_debug("Returning validation check from :" + json.dumps(validation_rules) + " => " + str(validation_ok) )
		return validation_ok



class Transform(Staple):

	@staticmethod
	def _func_not_found( value, param):
		Transform.log_error("transformation function not found")

	#############################################################################################################
	#Check if the current 
	@staticmethod
	def to_bool(value, param):
		return Transform._map_value( value, {'':False, 'false':False, '0':False, 
											'True':True, 'true':True, '1':True, True:True} )
	@staticmethod
	def _map_value(value, map):
		return map.get( value, None)



class Validate(Staple):
	#############################################################################################################
	#Check if the current 
	@staticmethod
	def _get_data_field_field(  value, field_name):
		for data_fld in value:	#find the relevant data field in there
			if data_fld['id'] == field_name:
				return data_fld
		return None

	#############################################################################################################
	#validation function not found
	@staticmethod
	def _func_not_found( value, param):
		Validate.log_error("validtion function not found")

	#############################################################################################################
	#Check that field is required 
	@staticmethod
	def required(  value, param):  
		if not param: return True
		return False if not value else True
		# return True

	#############################################################################################################
	#Check that field has min length as required
	@staticmethod
	def text_min_len(  value, param): 
		if len( str( value  ) ) >= param: return True
		return False

	#############################################################################################################
	#Check that field has max length as required
	@staticmethod
	def text_max_len(  value, param): 
		if len( str( value ) ) <= param: return True
		return False

	#############################################################################################################
	#Check that number is gte
	@staticmethod
	def num_gte(   value, param ): 
		if int( value ) >= int(param): return True
		return False

	#############################################################################################################
	#Check that number is gte
	def num_lte(  value, param ): 
		if int( value ) <= int(param): return True
		return False

	#############################################################################################################
	#Check that field has max length as required
	@staticmethod
	def is_url(  value, param=None):  
		url_re = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))'
		url = re.findall(url_re, value )
		return True if url else False

	#############################################################################################################
	#Check that field has max length as required
	@staticmethod
	def is_ip(  value, param=None):  
		url_re = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
		url = re.findall(url_re, value )
		return True if url else False


	#############################################################################################################
	#Check that number is gte
	@staticmethod
	def is_unix_path(  value , param=None): 
		path_re = r'\/?(\/?.+?)+[\/]?'
		path = re.findall(path_re, value )
		return True if path else False