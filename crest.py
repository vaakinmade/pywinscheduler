# installed pycairo using windows binary wheel file
#installed cffi to install cairocffi
# installed cairocffi to install cairosvg
from footyapi import FootballDataAPI

import cairosvg
import tinys3
from decouple import config


class Crest():
	@classmethod
	def upload_to_s3(cls, file):
		S3_ACCESS_KEY = config('AWS_ACCESS_KEY_ID', cast=str)
		S3_SECRET_KEY = config('AWS_SECRET_ACCESS_KEY', cast=str)
		S3_BUCKET = config('AWS_STORAGE_BUCKET_NAME', cast=str)
		conn = tinys3.Connection(
			S3_ACCESS_KEY,
			S3_SECRET_KEY,
			tls=True)
		print("File", file)
		f = open('{}'.format(file), 'rb')
		conn.upload('crests/{}'.format(file), f, S3_BUCKET)

	@classmethod
	def svg2png(cls, svg_url, team_id):
		png_file = cairosvg.svg2png(url=svg_url,
			write_to="img/crests/{}.png".format(team_id))

		cls.upload_to_s3("crests/{}.png".format(team_id))
		return png_file

	@classmethod
	def team_crest(cls, competition_id, home_id, away_id):
		clubs = FootballDataAPI().get_clubs(competition_id)

		# attempt to retrieve crest from crest list
		home_crest = clubs.get(str(home_id).encode('utf-8'))
		away_crest = clubs.get(str(away_id).encode('utf-8'))

		home_crest = home_crest.decode('utf-8')
		away_crest = away_crest.decode('utf-8')
		
		print(cls.svg2png(home_crest, home_id),
			cls.svg2png(away_crest, away_id))
		return cls.svg2png(home_crest), cls.svg2png(away_crest)