# on the other side

import requests
import time
import json
import os

unique_id = 'thisismyniqueid'
domain = 'http://localhost:8080'
path_to_watch = os.getcwd()

def send_file_to_server(filename):
	print path_to_watch
	print filename
	print os.path.join(path_to_watch, filename)
	files = { 'photo': open(path_to_watch+'/'+filename, 'rb') }
	data = { 'timestamp': time.time(), 'unique_id': unique_id }
	save_credentials_r = requests.post(url = domain+'/castaneda/check_identity', data = data, files = files)


send_file_to_server('base_identities/sad.bmp')
# So actually I am a fucking genious, because what I do I just have a fucking while True loop
# that everytime the filesystem changes I send the image to the server with a timestamp.
# then the server has to take care of deleting it if it is not used within 2 minutes.

before = dict([(f, None) for f in os.listdir (path_to_watch)])
while 1:
	time.sleep (2)
	after = dict([(f, None) for f in os.listdir (path_to_watch)])
	added = [f for f in after if not f in before]
	removed = [f for f in before if not f in after]
	if added:
		send_file_to_server(added[-1])
	before = after