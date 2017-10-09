from urllib import request
from xml.etree import ElementTree
import http.client
import json


class FootballDataAPI():
	def __init__(self):
		self.connection = http.client.HTTPConnection('api.football-data.org')
		self.headers = { 'X-Response-Control': 'minified' }

	def retrieve_previous_fixtures(self):
		self.connection.request('GET',
			'/v1/competitions/445/fixtures?timeFrame=p14',
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