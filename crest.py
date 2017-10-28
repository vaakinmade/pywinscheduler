# installed pycairo using windows binary wheel file
#installed cffi to install cairocffi
# installed cairocffi to install cairosvg
import os
import requests
from footyapi import FootballDataAPI

import cairosvg
import boto
from boto.s3.key import Key
from decouple import config


class Crest():
	S3_ACCESS_KEY = config('AWS_ACCESS_KEY_ID', cast=str)
	S3_SECRET_KEY = config('AWS_SECRET_ACCESS_KEY', cast=str)
	S3_BUCKET = config('AWS_STORAGE_BUCKET_NAME', cast=str)
	HOST_REGION = "s3.us-east-2.amazonaws.com"

	@classmethod
	def upload_to_s3(cls, image_file):
		f = open(image_file, 'rb')
		conn = boto.connect_s3(cls.S3_ACCESS_KEY,
			cls.S3_SECRET_KEY,
			host=cls.HOST_REGION)

		bucket = conn.get_bucket(cls.S3_BUCKET)

		k = Key(bucket)
		filename_base = image_file.split("/")
		k.key = "crests/" + filename_base[-1]
		file_size = k.set_contents_from_file(f)

		s3_file = "https://s3.us-east-2.amazonaws.com/{}/crests/{}".format(
			cls.S3_BUCKET,
			filename_base[-1])
		return s3_file

	def svg2png(self, svg_url, team_id):
		if svg_url[-3:].lower() == "svg":
			try:
				cairosvg.svg2png(url=svg_url,
					write_to="img/crests/{}.png".format(team_id))
				result = self.upload_to_s3("img/crests/{}.png".format(team_id))
			except:
				print("Exception Raised. SVG to PNG conversion failed!")
				result = svg_url
		elif svg_url[-3:].lower() == "png":
			result = svg_url
		else:
			# Return none if expected file type != png || svg
			print("File is neither is SVG or PNG")
			result = None
		return result

	def team_crest(self, competition_id, home_id, away_id):
		home_crest = os.path.isfile("img/crests/{}.png".format(home_id))
		away_crest = os.path.isfile("img/crests/{}.png".format(away_id))

		if home_crest:
			s3_home_url = "https://{}/{}/crests/{}.png".format(
			type(self).HOST_REGION,
			type(self).S3_BUCKET,
			home_id)
		else:
			clubs = FootballDataAPI().get_clubs(competition_id)
			svg_url = clubs.get(str(home_id).encode('utf-8'))
			s3_home_url = self.svg2png(svg_url.decode('utf-8'), home_id)
		
		if away_crest:
			s3_away_url = "https://{}/{}/crests/{}.png".format(
			type(self).HOST_REGION,
			type(self).S3_BUCKET,
			away_id)
		else:
			clubs = FootballDataAPI().get_clubs(competition_id)
			svg_url = clubs.get(str(away_id).encode('utf-8'))
			s3_away_url = self.svg2png(svg_url.decode('utf-8'), away_id)
				
		return s3_home_url, s3_away_url