from pprint import pprint
import requests
from lxml import html
import re

def check_column(field):
	if field.lower() == 'opponent':
		return '//*[@id="{}"]/tbody/tr[{}]/td[{}]/a//text()'
	elif field.lower() == 'date':
		return '//*[@id="{}"]/tbody/tr[{}]/th//text()'
	else:
		return '//*[@id="{}"]/tbody/tr[{}]/td[{}]//text()'


class ParseTeam:
    def __init__(self, url):
        self.url = url
        r = requests.get(url)
        self.tree = html.fromstring(r.content)


    def parse_column(self, table_xpath='matchlogs_for', args=[]):
        xpath_header_url = '//*[@id="{}"]/thead/tr//text()'.format(table_xpath)

        l = self.tree.xpath('//*[@id="{0}"]/tbody/tr//text()'.format(table_xpath))

        # parse columns name
        # header = re.findall(r' \w+ ',str(self.tree.xpath(xpath_header_url)))
        re.findall(r'\w+', str(self.tree.xpath(xpath_header_url)))
        list_header = re.findall(r'\w+', str(self.tree.xpath(xpath_header_url)))
        print('lstheader:', list_header)
        d = {}
        count = 0
        # create dict of columns name
        for x in list_header:
            d[x] = count
            count += 1

        # output table by column name
        # *args -- the list of name columns
        json_team = {}
        json_team['team'] = self.tree.xpath('//*[@id="meta"]/div[2]/h1/span[1]//text()')[0]

        for key, value in d.items():
            json_team[key] = []

            for arg in args:
                json_team['id'] = 0

                if arg.lower() == key.lower():
                    json_team['team'] = self.tree.xpath('//*[@id="meta"]/div[2]/h1/span[1]//text()')[0]
                    for column in range(1, len(l)):
                        u = self.tree.xpath(check_column(arg).format(table_xpath, column, value))
                        # print(u[0])
                        try:
                            json_team[key].append(u[0])
                        except Exception:
                            break
                # self.tree.xpath(url))

            # json_team['total_suma'] = lambda json_team['sum_column'] : json_team['column_count'] + len(l)
        return json_team


spain = ParseTeam('https://fbref.com/en/squads/b561dd30/Spain-Stats#matchlogs_for')
poland = ParseTeam('https://fbref.com/en/squads/8912dcf0/Poland-Stats#matchlogs_for')

json_spain = spain.parse_column(args=['result', 'Venue', 'GF', 'Day', 'Opponent', 'Date'])
json_poland = poland.parse_column(args=['result', 'Venue', 'GF', 'Day', 'Opponent', 'Date'])

pprint(json_spain)
total_poland = sum([int(x) for x in json_poland['GF']])
total_spain  = sum([int(x) for x in json_spain['GF']])

# Выводим моду забитых голов: 
def moda_goals(goals):

	d = {}
	for x in goals:
		try: 
			d[x] +=1
		except KeyError:
			d[x] = 1

	#pprint(d)
	Max = 0
	Max_var = None
	for k, v in d.items():
		if v > Max: 
			Max = v
			Max_var = k

	return f'Often Count Goals {Max} times of {Max_var}'

def add_points_by_result(fields):
	total_points = 0
	for field in fields:
		if field.lower() == 'w':
			total_points += 3
		elif field.lower() == 'd':
			total_points += 1.5
		elif field.lower() == 'l':
			total_points += 0
	return total_points




#total_procent = (total_goal_poland + total_goal_spain) / 100

print(total_poland)
print(total_spain)

print(moda_goals(json_spain['GF']))
print(moda_goals(json_poland['GF']))

print(add_points_by_result(json_spain['Result']))
print(add_points_by_result(json_poland['Result']))

#
# pprint(json_spain)

# //*[@id="matchlogs_for"]/tbody/tr[1]/td[6]
# pprint(spain.parse_column())
# pprint(poland.parse_column())
# team_procent = 100
# (team1 + team2) = total / 100% = total team procent
# total / delim na 2 = % procent


