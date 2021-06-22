import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome('./chromedriver')

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

class TypeLoginError(Exception):
	pass


class Auth:
	''' This is class may  make connect to parimatch account. We can add modifications for interact with parimatch, '''

	def __type_login_choice(type_login):
		slct_type = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div/div[2]/select')
		ActionChains(driver).move_to_element(slct_type).click_and_hold().perform()

		if type_login == 3 or type_login == 'email':
			button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/select/option[3]')))
		elif type_login == 2 or type_login == 'phone': 
			button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/select/option[2]')))
		elif type_login == 1 or type_login == 'id':
			button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[2]/div/form/div[1]/div[2]/div[2]/select/option[1]')))
			
		else: 
			raise TypeLoginError("Wrong type login. Use 1(id), 2(phone), 3(email).")

		button.click() # select of login types

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


try: 
	user = Auth('123', '12345')
	print('Success auth.')
except Exception as err: 
	print('Access denied (', err,').')



class ParsParimatch:
    def __init__(self, url):
        self.url = url

        headers= {'content-type': 'application/json', 
        'User-Agent': ua.chrome,
        }
       	driver = webdriver.Chrome('./chromedriver')
       	driver.get(url)

        #r = requests.get(url, headers=headers)
        #print(r.headers)




        # print('Украина' in r.text)



        # self.tree = html.fromstring(r.text)


    def parse_main(self):
    	xp_url_result_first = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[{}]/span[{}]//text()'
    	
    	#print(self.tree.xpath(xp_url_result_first))
    	for x in range(1,3+1):
    		for y in range(1,2+1):
    			data = print(self.tree.xpath(xp_url_result_first.format(x, y)))
    			print(data)


#uaat = ParsePage('https://www.bet365.com/#/AC/B1/C1/D8/E102526950/F3/')

#uaat.parse_main()


#driver.get('https://parimatch.com/ru/')
	#'https://parimatch.com/ru/events/croatia-scotland-5841562/1')

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
