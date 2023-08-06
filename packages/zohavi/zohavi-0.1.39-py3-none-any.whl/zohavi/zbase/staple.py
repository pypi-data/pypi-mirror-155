
class Staple:
	def __init__(self, app=None, logger=None):
		self.logger = logger
		self.app = app
		self.debug = False


	def log_debug(self, message):
		if self.logger: self.logger.debug( message )
		else: print( "DEBUG:" + message )

	def log_error(self, message):
		if self.logger: self.logger.error( message )
		else: print( "ERROR:" + message )

	def log_info(self, message):
		if self.logger: self.logger.info( message )
		else: print( "INFO:" + message )

	def log_warning(self, message):
		if self.logger: self.logger.warning( message )
		else: print( "WARNING:" + message )
