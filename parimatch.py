import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint

from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(5)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')


class TypeLoginError(Exception):
    pass


class Auth:
	# This is class may  make connect to parimatch account. We can add modifications for interact with parimatch


	def __type_login_choice(type_login):
		slct_type = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div/div[2]/select')
		ActionChains(driver).move_to_element(slct_type).click_and_hold().perform()
		if type_login == 3 or type_login == 'email':
			button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/select/option[3]')))
		elif type_login == 2 or type_login == 'phone':
			button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/select/option[2]')))
		elif type_login == 1 or type_login == 'id':
			button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/select/option[1]')))
		else:
			raise TypeLoginError("Wrong type login. Use 1(id), 2(phone), 3(email).")

		button.click()  # select of login types

	def __init__(self, login, password, type_login=1):
		"""type_login for select how to login(
		1 = > id
		2 = > phone
		3 = > email
		)
		"""
		self.login = login
		self.password = password

		driver.get('https://parimatch.com/ru/login')
		__type_login_choice(type_login)
		# enter login
		inpt_login = driver.find_element_by_xpath('//*[@id="id"]')
		inpt_login.send_keys(self.login)
		# enter password
		inpt_password = driver.find_element_by_xpath('//*[@id="password"]')
		inpt_password.send_keys(self.password)
		apply_register = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div[2]/div/form/button')
		apply_register.click()
		ans = input('Run captcha? y/n')
		if ans == 'y' or ans == 'Y':
			pass
		else:
			raise


class ParseParimatch:
	def __init__(self, url='', obj_class_auth=None):
		self.url = url
		if obj_class_auth == None:
			pass
		elif isinstance(obj_class_auth, Auth):
			self.account = obj_class_auth
		else:
			raise TypeLoginError('Incorrect obj_class_auth. Object class need created by Auth.')

	def parse_main(self):
		xp_url_result_first = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[{}]/span[{}]//text()'
		# print(self.tree.xpath(xp_url_result_first))
		for x in range(1, 3 + 1):
			for y in range(1, 2 + 1):
				data = print(self.tree.xpath(xp_url_result_first.format(x, y)))
				print(data)


	def future_football_game(self):
		driver.get('https://parimatch.com/ru/')
		all_games = []
		for x in range(1, 25):
			d = dict(date_game=None, team1=None, team2=None, bet=[])
			team1 = '//*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[{}]/div/div/a[2]/div[2]/div/span[1]'
			team2 = '//*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[{}]/div/div/a[2]/div[2]/div/span[2]'
			date_game = '//*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[{}]/div/div/a[1]/div[1]/div'
			WIN1 = '//*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[{}]/div/div/div/a/div/div/div/div[1]/div[2]/div/span'
			dX = '//*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[{}]/div/div/div/a/div/div/div/div[2]/div[2]/div/span'
			WIN2 = '//*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[{}]/div/div/div/a/div/div/div/div[3]/div[2]/div/span'

			try:
				d['team1'] = driver.find_element_by_xpath(team1.format(x)).text
				d['team2'] = driver.find_element_by_xpath(team2.format(x)).text
				d['date_game'] = driver.find_element_by_xpath(date_game.format(x)).text
				d['bet'].append(driver.find_element_by_xpath(WIN1.format(x)).text)
				d['bet'].append(driver.find_element_by_xpath(dX.format(x)).text)
				d['bet'].append(driver.find_element_by_xpath(WIN2.format(x)).text)
				all_games.append(d)
			except NoSuchElementException as err:
				break
			except Exception as err:
				print(err)
				raise
		return all_games


# //*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[1]/div/div/div/a/div/div/div/div[1]/div[2]/div/span
# //*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[1]/div/div/div/a/div/div/div/div[2]/div[2]/div/span
# //*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[1]/div/div/div/a/div/div/div/div[3]/div[2]/div/span

# //*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]/div[2]/div/div/div/a/div/div/div/div[1]/div[2]/div/span

"""
try:
    # user = Auth('123', '12345')
    # print('Success auth.')
    print('1')
except Exception as err:
    print('Access denied (', err, ').')
"""
game = ParseParimatch()
pprint(game.future_football_game())

# //*[@id="root"]/div[2]/div[1]/div[2]/div[3] ->  field row
# //*[@id="root"]/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/span -> field title

# //*[@id="root"]/div[2]/div[1]/div[2]/div[3]/div[2]/div //
# //*[@id="root"]/div[2]/div[1]/div[2]/div[4] //

# total
# //*[@id="root"]/div[2]/div[1]/div[2]/div[6]/div[2]/div[2] -> row 1
# //*[@id="root"]/div[2]/div[1]/div[2]/div[6]/div[2]/div[2]/div[1] - > title of rows total
# //*[@id="root"]/div[2]/div[1]/div[2]/div[6]/div[2]/div[2]/div[2] - > column 1 at row 1
# //*[@id="root"]/div[2]/div[1]/div[2]/div[6]/div[2]/div[2]/div[3] - > column 2 at row 1
# //*[@id="root"]/div[2]/div[1]/div[2]/div[6]/div[2]/div[3] -> row 2


# uaat = ParsePage('https://www.bet365.com/#/AC/B1/C1/D8/E102526950/F3/')

# uaat.parse_main()


# driver.get('https://parimatch.com/ru/')
# 'https://parimatch.com/ru/events/croatia-scotland-5841562/1')

'''


#el = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[1]/div/div[3]/div[2]/div/div[3]/div[2]/div/span')))
#print(el.text)
l_future_games = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div[2]/div[1]/div[2]/div/div[4]/div[1]/div[2]')))
print(len(l_future_games))



command_line = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div[3]/div[1]/div/div/div[4]/div[1]/div[2]')))
#a,b = re.findall(r'[А-Я]\w+', command_line.text) # teams
#print(f'{a} \t {b}')
url = '//*[@id="root"]/div[2]/div[1]/div/div[3]/div[2]/div/div[{}]/div[2]/div/span'

driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div/div[3]/div[2]/div/div[3]').click()

'''
