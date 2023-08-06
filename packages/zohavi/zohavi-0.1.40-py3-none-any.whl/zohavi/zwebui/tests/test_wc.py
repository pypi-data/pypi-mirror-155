import unittest
unittest.TestLoader.sortTestMethodsUsing = None

from pathlib import Path 
import sys, os, jsoncfg, json
sys.path.insert(0, '../../../')
 
# from zohavi.zcore.appcore import AppCore 

from flask import Flask, jsonify, render_template,send_file, request
from mclogger.mclogger import MCLogger

logger = MCLogger( 'test_log.txt' )
 

html = """<html>
			<body>
				<h1>hello world</h1>
			</body>
		</html>"""

app = Flask(__name__)
# myapp = AppCore(app, sccfg, 'dev' )

#################################################################
@app.route('/webui/<path:url>', methods=['GET' ])
def webui_path( url ):
	# path = current_app.config['ENV_BASE_DIR']
	search_file = os.getcwd()[:os.getcwd().rfind('/')] +"/" +url
	# breakpoint()

	if Path( search_file ).is_file():
		return send_file( search_file )

	print("file missing:" + str(search_file)   )
	abort(404)
	logger.debug(url)
	return render_template( 'test_table.html')

#################################################################
@app.route('/test/menu', methods=['GET' ] )
def test_menu( ):
	return render_template( 'test_menu.html')



#################################################################
@app.route('/test/table', methods=['GET' ] )
def test_table( ):
	return render_template( 'test_table.html')

#################################################################
@app.route("/test/table/ajax_add", methods=["POST"])
def test_table_add():
	logger.debug( request.json )
	return json.dumps({'success':True}), 200

#################################################################
@app.route("/routes", methods=["GET"])
def getRoutes( ):
	routes = {}
	for rule_item in app.url_map._rules:
		routes[rule_item.rule] = {}
		routes[rule_item.rule]["functionName"] = rule_item.endpoint
		routes[rule_item.rule]["methods"] = list(rule_item.methods)
	return jsonify(routes)

 
 #################################################################
 #################################################################
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=4601, debug=True)
