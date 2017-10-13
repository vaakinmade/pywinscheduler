import http.client
import json
import redis


class FootballDataAPI():
	def __init__(self):
		self.connection = http.client.HTTPConnection('api.football-data.org')
		self.headers = {
			'X-Auth-Token': '8128fabfbba5438faf651bf3fd29f54a',
			'X-Response-Control': 'minified'
		}

	def _current_matchday(self, competition_id):
		self.connection.request('GET',
			'/v1/competitions/{}/'.format(competition_id),
			None, self.headers)
		response = json.loads(self.connection.getresponse().read().decode())
		return response["currentMatchday"]

	def retrieve_matchday_fixtures(self, competition_id):
		self.connection.request('GET',
			'/v1/competitions/{}/fixtures?matchday={}'.format(
			competition_id,
			self._current_matchday(competition_id)
			),
			None, self.headers )
		response = json.loads(self.connection.getresponse().read().decode())
		return response

	def latest_competition_results(self, competition_id):
		self.connection.request('GET',
			'/v1/competitions/{}/fixtures?matchday={}'.format(
			competition_id,
			self._current_matchday(competition_id)-1
			),
			None, self.headers )
		response = json.loads(self.connection.getresponse().read().decode())
		return response

	def single_team_fixtures(self, club_id):
		self.connection.request('GET',
			'/v1/teams/{}/fixtures?timeFrame=n10'.format(club_id),
			None, self.headers )
		response = json.loads(self.connection.getresponse().read().decode())
		return response

	def get_club(self, club_id):
		self.connection.request('GET',
			'/v1/teams/{}'.format(club_id),
			None, self.headers )
		response = json.loads(self.connection.getresponse().read().decode())
		print(response)
		return response


FootballDataAPI().get_club(66)