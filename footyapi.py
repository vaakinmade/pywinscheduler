from urllib import request
from xml.etree import ElementTree
import http.client
import json


class FootballDataAPI():
	def __init__(self):
		self.connection = http.client.HTTPConnection('api.football-data.org')
		self.headers = {
			'X-Auth-Token': '8128fabfbba5438faf651bf3fd29f54a',
			'X-Response-Control': 'minified'
		}

	def current_matchday(self):
		self.connection.request('GET',
			'/v1/competitions/445/',
			None, self.headers)
		response = json.loads(self.connection.getresponse().read().decode())
		return response["currentMatchday"]

	def retrieve_matchday_fixtures(self):
		self.connection.request('GET',
			'/v1/competitions/445/fixtures?matchday={}'.format(
			self.current_matchday()
			),
			None, self.headers )
		response = json.loads(self.connection.getresponse().read().decode())
		return response

	def get_club_crest(self, club_id):
		self.connection.request('GET',
			'/v1/teams/{}'.format(club_id),
			None, self.headers )
		response = json.loads(self.connection.getresponse().read().decode())
		return response["crestUrl"]


print(FootballDataAPI().get_club_crest(66))