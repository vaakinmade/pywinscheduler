import urllib.request


class Weather():

	def __init__(station_id='KLAX'):
		self.station_id = station_id

	def retrieve_weather_data():
		url_general = 'http://www.weather.gov/xml/current_obs/{}.xml'
		url = url_general.format(self.station_id)
		request = urllib.request.urlopen(url)
		content = request.read().decode()