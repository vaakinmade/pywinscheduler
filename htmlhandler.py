from datetime import datetime
import iso8601
from dateutil import tz


class HtmlHandler():
	def date_converter(self, date_time):
		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()

		utc = iso8601.parse_date(date_time)
		local_time = utc.astimezone(to_zone)
		return local_time

	@classmethod
	def create_html_file(cls, list_dict, crest_url, html_file):
		utc_time = iso8601.parse_date('2012-11-01T04:16:13-04:00')

		print(datetime.strftime(utc_time, "%d %b %y"))
		with open(html_file, mode='w') as outfile:
			outfile.write('\t<tr><td align="center">'
				+ datetime.strftime(utc_time, "%d %b %y")
				+'</td></tr><br>\n')
			outfile.write('<img alt={} src={} height="16" width="16">'.format(
				"EPL Fixtures", crest_url))
			outfile.write('''<br>
				<span style="color:blue"><b>\tEPL Upcoming Fixtures:</b>\n''')
			outfile.write('<br>')    
			    
			outfile.write('<html><table border=1>\n')
			for data_dict in list_dict["fixtures"]:
			    outfile.write('''<tr>
					<td><b><span style="color:blue">{0}</b></td>
					<td>
						<strong>
							<span style="color:black">{2:%H:%M}</span>
						</strong>
					</td>
					<td align="left">
						<span style="color:blue"><b>{1}</b>
					</td>
					</tr>\n'''.format(
						data_dict["homeTeamName"],
						data_dict["awayTeamName"],
						HtmlHandler().date_converter(data_dict["date"]))
				)
			outfile.write('</table></html>\n')

			return outfile

# pseudo test
if __name__ == '__main__':
    from footyapi import FootballDataAPI
    obj = FootballDataAPI()
    list_dict, crest = obj.retrieve_matchday_fixtures(), obj.get_club_crest(66)
    HtmlHandler.create_html_file(list_dict, crest, "Footy_Email_File.html")

