from datetime import datetime
import iso8601
from dateutil import tz

from footyapi import FootballDataAPI


class HtmlHandler():
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

	def create_html_file(self, fixture_list_dict, html_file):

		with open(html_file, mode='w') as outfile:
			outfile.write('\t<tr><td align="center">'
				+ datetime.strftime(datetime.now(), "%d %b %y")
				+'</td></tr><br>\n')
			outfile.write('''<br>
				<span style="color:blue"><b>\tEPL Upcoming Fixtures:</b>\n''')
			outfile.write('<br>')    
			
			outfile.write('<html><table border=1>\n')

			unique_dates = self.unique_dates(fixture_list_dict)
			for title_date in unique_dates:
				outfile.write('''<tr>
					<td align="center">
						{}
					</td>
					</tr>'''.format(title_date)
				)
				for data_dict in fixture_list_dict["fixtures"]:
					if title_date == self.extract_date(data_dict.get('date')):
						home_team_crest = FootballDataAPI().get_club_crest(
							data_dict["homeTeamId"])
						away_team_crest = FootballDataAPI().get_club_crest(
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
								data_dict.get('homeTeamName'),
								data_dict.get('awayTeamName'),
								self.time_converter(data_dict.get('date')),
								home_team_crest,
								away_team_crest
								)
						)
			outfile.write('</table></html>\n')

			return outfile

# pseudo test
if __name__ == '__main__':
	from footyapi import FootballDataAPI
	obj = FootballDataAPI()
	fixture_list_dict = obj.retrieve_matchday_fixtures()
	HtmlHandler().create_html_file(fixture_list_dict, "Footy_Email_File.html")
	#HtmlHandler().unique_dates(fixture_list_dict)

