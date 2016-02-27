import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from bottle import get, post, request, route, run, static_file
import bottle
import datetime
import hashlib
import time
import sys
import os

SECRET = 'gPN0xF21ui0IIFH8Ec3uqy9bCOu7k76f'
dateStr = lambda(x): datetime.date.fromtimestamp(int(x)).strftime('%Y-%m')

# sys.stdout = open('web_server.log', 'a')
# sys.stderr = sys.stdout
testing = False


@route('/castaneda')
def index():
	return 'your welcome.'


if __name__ == '__main__':
	run(host='0.0.0.0', port=8080)
	# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
	app = application = bottle.default_app()