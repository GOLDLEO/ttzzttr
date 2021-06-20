import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import requests
from lxml import html
import re


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
                        url = '//*[@id="{}"]/tbody/tr[{}]/td[{}]//text()'.format(table_xpath, column, value)
                        u = self.tree.xpath(url)
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

json_spain = spain.parse_column(args=['Result'])
json_poland = poland.parse_column(args=['result', 'Venue', 'GF', 'Day'])

pprint(json_poland)
# pprint(json_spain)

# //*[@id="matchlogs_for"]/tbody/tr[1]/td[6]
# pprint(spain.parse_column())
# pprint(poland.parse_column())
# team_procent = 100
# (team1 + team2) = total / 100% = total team procent
# total / delim na 2 = % procent


