from urllib import request
from xml.etree import ElementTree


class Weather():

	def __init__(self, station_id='KLAX'):
		self.station_id = station_id

	def retrieve_data(self):
		url_general = 'http://www.weather.gov/xml/current_obs/{}.xml'
		url = url_general.format(self.station_id)
		request_data = request.urlopen(url)
		content = request_data.read().decode()
		return content

	def get_xml_elements(self):
		# Retrieve the tags we are interested in
		weather_data_tags_dict = {
		    'observation_time': '',
		    'weather': '',
		    'temp_f':  '',
		    'temp_c':  '',
		    'dewpoint_f': '',
		    'dewpoint_c': '',
		    'relative_humidity': '',
		    'wind_string':   '',
		    'visibility_mi': '',
		    'pressure_string': '',
		    'pressure_in': '',
		    'location': ''
		    }

		xml_root = ElementTree.fromstring(self.retrieve_data())

		for data_point in weather_data_tags_dict.keys():
			weather_data_tags_dict[data_point] = xml_root.find(data_point).text

		icon_url_base = xml_root.find('icon_url_base').text
		icon_url_name = xml_root.find('icon_url_name').text
		icon_url = icon_url_base + icon_url_name
    
		return icon_url


#Weather().retrieve_data()
Weather().get_xml_elements()