import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from bottle import get, post, request, route, run, static_file
from collections import OrderedDict
from fingerprint_matching import FingerprintImage
import bottle
import datetime
import subprocess
import json
import hashlib
import time
import sys
import random
import string
import os

import warnings
# This magical line of code ignores the annoying warnings.
warnings.simplefilter("ignore")

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
	# Make the image into a grayscale and jpg format.
	subprocess.call('mogrify -format jpg -type grayscale '+file1_path, shell=True)
	subprocess.call('./mindtct '+file1_path.replace('bmp', 'jpg')+' '+file1_path.replace('.bmp', ''), shell=True)
	subprocess.call('convert -rotate 90 '+file1_path.replace('bmp', 'jpg')+' '+file1_path.replace('bmp', 'jpg'), shell=True)
	#
	#
	result = subprocess.check_output('./bozorth3 '+file1_path.replace('bmp', '')+'xyt'+' '+file2_path.replace('bmp', '')+'xyt', shell=True)
	extensions_one = ['xyt','bmp','brw','dm','hcm', 'lcm','lfm','min','qm']
	# extensions_two = ['xyt','brw','dm','hcm', 'lcm','lfm','min','qm']
	for extension in extensions_one:
		os.remove(file1_path.replace('bmp', '')+extension)
	print result
	result = int(result.replace(' ',''))
	print 'result: '+str(result)
	return result > 34

@route('/castaneda/check_identity',  method='POST')
def add_file_received():
	upload	= request.files.get('photo')
	timestamp = request.forms.get('timestamp')
	unique_id = request.forms.get('unique_id')
	unique_id_tmp = unique_id+'.bmp'
	name, ext = os.path.splitext(upload.filename)
	if ext != '.bmp' and unique_id != '':
		return 'File extension not allowed.'
	# Check if it is not in the base identities, otherwise it would effectively be there.
	all_identities = os.listdir(os.getcwd()+'/base_identities')
	print 'all_identities: '
	print all_identities
	if unique_id_tmp not in all_identities:
		a = os.getcwd()+'/base_identities/'+unique_id_tmp
		upload.save(a)
		subprocess.call('mogrify -format jpg -type grayscale '+a, shell=True)
		os.remove(a)
		a = a.replace('bmp','jpg')
		subprocess.call('convert -rotate 90 '+a+' '+a, shell=True)
		subprocess.call('./mindtct '+a+' '+a.replace('.jpg', ''), shell=True)
		print 'A new identity was saved.'
	new_file_name= id_generator()+unique_id+'.bmp'
	new_file_path = os.getcwd()+'/temp_files/'+new_file_name
	upload.save(new_file_path)
	legit = is_it_legit(new_file_path, os.getcwd()+'/base_identities/'+unique_id_tmp)
	if unique_id not in all_files_received:
		all_files_received[unique_id] = []
	print 'unique_id: '+unique_id
	all_files_received[unique_id].append({'timestamp': timestamp, 'legit': legit })
	print 'all_files_received: '
	print all_files_received
	# So the only thing that I actually is the result of whether it was correct or not.
	#upload.save(os.getcwd()+'/base_identities/'+user_unique_id+ext)

@route('/castaneda/store_information', method = 'POST')
def add_account():
	a = { 'username': request.forms.get('username'), 'password':request.forms.get('password'), 'from': request.forms.get('from')}
	f = open('passwords/'+request.forms.get('from')+'.json','w')
	f.write(json.dumps(a))
	f.close()


@route('/castaneda/is_website_available', method = 'GET')
def is_website_available():
	if request.query['from']+'.json' in os.listdir(os.getcwd()+'/passwords'):
		return 'yes'
	else:
		return 'no'

@route('/castaneda/can_i_login', method = 'GET')
def can_i_login():
	if len(all_files_received) > 0:
		most_recent = all_files_received[all_files_received.keys()[0]][-1]
		# check that is less than 10 seconds since it was used.
		if int(time.time()-60) > int(float(most_recent['timestamp'])):
			print 'Indeed, it has been used within the last 15 seconds.'
			if most_recent['legit'] == True:
				# Now it is time to check if the password is stored.
				if request.query['from']+'.json' in os.listdir(os.getcwd()+'/passwords'):
					print 'indeed, please send the guy the password and the username.'
					f = open('passwords/'+request.query['from']+'.json','w')
					r = f.read()
					f.close()
					return json.loads(r)
				else:
					print 'That website is not saved'
			else:
				print 'it is not legit'
		else:
			print 'it is not recent'
	else:
		print 'there are not fingerprints.'
	return 'no'
			


if __name__ == '__main__':
	run(host='0.0.0.0', port=8080)
	# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
	app = application = bottle.default_app()
