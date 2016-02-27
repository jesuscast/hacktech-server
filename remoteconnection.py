#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


# -----------------------------
# |                            |
# |  Firebase Connection       |
# |                            |
# -----------------------------

class RemoteConnection:
	def __init__(self, url, token):
		self.FIREBASE_URL = url
		self.token = token
		self.ending = "?auth="+self.token
	def to_url(self, stringT):
		return self.FIREBASE_URL+stringT+"/.json"+self.ending
	def post(self, direction, data):
		result = requests.patch(url = self.to_url(direction), data=json.dumps(data))
		return result
	def get(self, child):
		url = self.to_url(child)
		#print url
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None
	def delete(self, child):
		url = self.to_url(child)
		#print url
		r = requests.delete(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None

