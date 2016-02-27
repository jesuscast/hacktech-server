import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from bottle import get, post, request, route, run, static_file
from collections import OrderedDict
from fingerprint_matching import FingerprintImage
import bottle
import datetime
import hashlib
import time
import sys
import random
import string
import os

SECRET = 'gPN0xF21ui0IIFH8Ec3uqy9bCOu7k76f'
dateStr = lambda(x): datetime.date.fromtimestamp(int(x)).strftime('%Y-%m')

# sys.stdout = open('web_server.log', 'a')
# sys.stderr = sys.stdout
testing = False

all_files_received = {}

@route('/castaneda')
def index():
	return 'your welcome.'



# now the most important of all aspects, obtain an email from post and save it to database.

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def is_it_legit(file1_path, file2_path):
	""" I assume all of the photos need to be rotated 90ds to the right.
	Transformed through mninic. And analyzed through bazardoct or whatever.
	"""
	print 'file1_path: '+file1_path
	print 'file2_path: '+file2_path
	return True

@route('/castaneda/check_identity',  method='POST')
def add_file_received():
	upload	= request.files.get('photo')
	timestamp = request.forms.get('timestamp')
	unique_id = request.forms.get('unique_id')
	unique_id_tmp = unique_id+'.bmp'
	name, ext = os.path.splitext(upload.filename)
	if ext != '.bmp' and user_unique_id != '':
		return 'File extension not allowed.'
	# Check if it is not in the base identities, otherwise it would effectively be there.
	all_identities = os.listdir(os.getcwd()+'/base_identities')
	print 'all_identities: '
	print all_identities
	if unique_id_tmp not in all_identities:
		upload.save(os.getcwd()+'/base_identities/'+unique_id_tmp)
		tmp_holder = FingerprintImage(os.getcwd()+'/base_identities/'+unique_id_tmp)
		tmp_holder.rotate()
		print 'A new identity was saved.'
	new_file_name= id_generator()+unique_id+'.bmp'
	new_file_path = os.getcwd()+'/temp_files/'+new_file_name
	upload.save(new_file_path)
	# rotation
	tmp_holder = FingerprintImage(new_file_path)
	tmp_holder.rotate()
	# end rotation
	legit = is_it_legit(new_file_path, os.getcwd()+'/base_identities/'+unique_id_tmp)
	os.remove(new_file_path)
	if unique_id not in all_files_received:
		all_files_received[unique_id] = []
	print 'unique_id: '+unique_id
	all_files_received[unique_id].append({'timestamp': timestamp, 'legit': legit })
	print 'all_files_received: '
	print all_files_received
	# So the only thing that I actually is the result of whether it was correct or not.
	#upload.save(os.getcwd()+'/base_identities/'+user_unique_id+ext)



if __name__ == '__main__':
	run(host='0.0.0.0', port=8080)
	# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
	app = application = bottle.default_app()

"""
mogrify -format jpg -type grayscale identify_2016-02-27_02-08-31_00.bmp

./mindtct /home/jesus/jesos/learning/hackteck/images/jason/identify_2016-02-27_02-08-31_00.jpg final



./mindtct /home/jesus/jesos/learning/hackteck/images/jason/identify_2016-02-27_02-05-27_00.jpg final_3
"""