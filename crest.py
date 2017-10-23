# installed pycairo using windows binary wheel file
#installed cffi to install cairocffi
# installed cairocffi to install cairosvg
import os
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
		S3_ACCESS_KEY = config('AWS_ACCESS_KEY_ID', cast=str)
		S3_SECRET_KEY = config('AWS_SECRET_ACCESS_KEY', cast=str)
		S3_BUCKET = config('AWS_STORAGE_BUCKET_NAME', cast=str)
		HOST_REGION = "s3.us-east-2.amazonaws.com"


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

	@classmethod
	def svg2png(cls, svg_url, team_id):
		png_file = cairosvg.svg2png(url=svg_url,
			write_to="img/crests/{}.png".format(team_id))
		result = cls.upload_to_s3("img/crests/{}.png".format(team_id))
		return result

	@classmethod
	def team_crest(cls, competition_id, home_id, away_id):
		home_crest = os.path.isfile("img/crests/{}.png".format(home_id))
		away_crest = os.path.isfile("img/crests/{}.png".format(away_id))

		if home_crest and away_crest:
			s3_home_url = "https://{}/{}/crests/{}.png".format(
			cls.HOST_REGION,
			cls.S3_BUCKET,
			home_id)

			s3_away_url = "https://{}/{}/crests/{}.png".format(
			cls.HOST_REGION,
			cls.S3_BUCKET,
			away_id)
			
		if home_crest is False:
			print("home crest is absent... processing new one")
			clubs = FootballDataAPI().get_clubs(competition_id)
			svg_url = clubs.get(str(home_id).encode('utf-8'))
			s3_home_url = cls.svg2png(svg_url.decode('utf-8'), home_id)
						
		if away_crest is False:
			print("away crest is absent... processing new one")
			clubs = FootballDataAPI().get_clubs(competition_id)
			svg_url = clubs.get(str(home_id).encode('utf-8'))
			s3_away_url = cls.svg2png(svg_url.decode('utf-8'), away_id)
				
		return s3_home_url, s3_away_url