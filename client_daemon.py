# on the other side

import requests
import time
import json
import os
import uuid

import warnings
# This magical line of code ignores the annoying warnings.
warnings.simplefilter("ignore")

unique_id = str(uuid.uuid1())
domain = 'https://jesuscastaneda.me'
path_to_watch = os.getcwd()+'/watch_folder'

def send_file_to_server(filename):
	print path_to_watch
	print filename
	print os.path.join(path_to_watch, filename)
	files = { 'photo': open(path_to_watch+'/'+filename, 'rb') }
	data = { 'timestamp': time.time(), 'unique_id': unique_id }
	save_credentials_r = requests.post(url = domain+'/castaneda/check_identity', data = data, files = files, verify=False)


before = dict([(f, None) for f in os.listdir (path_to_watch)])
while 1:
	time.sleep (2)
	after = dict([(f, None) for f in os.listdir (path_to_watch)])
	added = [f for f in after if not f in before]
	removed = [f for f in before if not f in after]
	if added:
		send_file_to_server(added[-1])
	before = after