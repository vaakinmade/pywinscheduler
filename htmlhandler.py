from datetime import datetime
import iso8601
from dateutil import tz

from footyapi import FootballDataAPI


class HtmlHandler():
	def __init__(self):
		self.html_file = "Footy_Email_File.html"

	def time_converter(self, date_time):
		to_zone = tz.tzlocal()

		utc = iso8601.parse_date(date_time)
		local_time = utc.astimezone(to_zone)
		return local_time

	def extract_date(self, date_time):
		utc = iso8601.parse_date(date_time)
		return datetime.strftime(utc, "%d %b %y")

	def unique_dates(self, list_dict):
		date_set = set()
		for item in list_dict["fixtures"]:
			fixture_date = self.extract_date(item.get('date'))
			date_set.add(fixture_date)
		return sorted(date_set)

	def create_html_file(self, fixtures_list, team_fixtures_list):
		self.write_team_to_file(team_fixtures_list, self.html_file)
		self.write_epl_to_file(fixtures_list, self.html_file)

	def write_team_to_file(self, team_fixtures, html_file):
		club_name = FootballDataAPI().get_club(66).get('name')

		with open(html_file, mode='w') as outfile:
			outfile.write('''
				<html><table cellpadding=5 style="min-width:40%">\n''')
			outfile.write('''<tr><td colspan="3">
				<br><b>\t {} Upcoming Fixtures:</b></center></td></tr>\n'''.
				format(club_name.replace("FC", ""))
			)
			outfile.write('<br>')

			unique_dates = self.unique_dates(team_fixtures)
			for title_date in unique_dates:
				outfile.write('''<tr>
					<td align="center" colspan="3"
						style="background-color:#e0e0e0">
						{}
					</td>
					</tr>'''.format(title_date)
				)
				for data_dict in team_fixtures["fixtures"]:
					if title_date == self.extract_date(data_dict.get('date')):
						home_team_crest = FootballDataAPI().get_club(
							data_dict["homeTeamId"])
						away_team_crest = FootballDataAPI().get_club(
							data_dict["awayTeamId"])

						outfile.write('''<tr>
							<td>
							<img alt="crest" src={3} height="16" width="16">
							&nbsp;&nbsp; <span style="color:blue"><b>{0}</b>
							</td>
							<td>
								<strong>
									<span style="color:black">{2:%H:%M}</span>
								</strong>
							</td>
							<td align="left">
							<img alt="crest" src={4} height="16" width="16">
							&nbsp;&nbsp; <span style="color:blue"><b>{1}</b>
							</td>
							</tr>\n'''.format(
								data_dict.get('homeTeamName').replace("FC", ""),
								data_dict.get('awayTeamName').replace("FC", ""),
								self.time_converter(data_dict.get('date')),
								home_team_crest.get('crestUrl'),
								away_team_crest.get('crestUrl')
								)
						)
			outfile.write('</table></html>\n')

			return outfile

	def write_epl_to_file(self, fixture_list_dict, html_file):
		with open(html_file, mode='a') as outfile:
			outfile.write('''
				<html>
					<table cellpadding=5 style="min-width:40%">\n'''
			)
			outfile.write('''<tr><td colspan="3">
				<br><b>\t EPL Upcoming Fixtures:</b></center></td></tr>\n\n''')
			
			unique_dates = self.unique_dates(fixture_list_dict)
			for title_date in unique_dates:
				outfile.write('''<tr>
					<td align="center" colspan="3"
						style="background-color:#e0e0e0">
						{}
					</td>
					</tr>'''.format(title_date)
				)
				for data_dict in fixture_list_dict["fixtures"]:
					if title_date == self.extract_date(data_dict.get('date')):
						home_team_crest = FootballDataAPI().get_club(
							data_dict["homeTeamId"])
						away_team_crest = FootballDataAPI().get_club(
							data_dict["awayTeamId"])

						outfile.write('''<tr>
							<td>
							<img alt="crest" src={3} height="16" width="16">
							&nbsp;&nbsp; <span style="color:blue"><b>{0}</b>
							</td>
							<td>
								<strong>
									<span style="color:black">{2:%H:%M}</span>
								</strong>
							</td>
							<td align="left">
							<img alt="crest" src={4} height="16" width="16">
							&nbsp;&nbsp; <span style="color:blue"><b>{1}</b>
							</td>
							</tr>\n'''.format(
								data_dict.get('homeTeamName').replace("FC", ""),
								data_dict.get('awayTeamName').replace("FC", ""),
								self.time_converter(data_dict.get('date')),
								home_team_crest.get('crestUrl'),
								away_team_crest.get('crestUrl')
								)
						)
			outfile.write('</table></html>\n')

			return outfile

# pseudo test
if __name__ == '__main__':
	from footyapi import FootballDataAPI
	obj = FootballDataAPI()
	fixtures_list = obj.retrieve_matchday_fixtures(445)
	team_fixtures_list = obj.team_fixtures(66)
	HtmlHandler().create_html_file(fixtures_list, team_fixtures_list)
	#HtmlHandler().unique_dates(fixture_list_dict)

