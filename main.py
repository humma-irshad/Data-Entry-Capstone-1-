import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


URL_zillow = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.61529005957031%2C%22east%22%3A-122.25136794042969%2C%22south%22%3A37.65742356937156%2C%22north%22%3A37.892971720854746%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url=URL_zillow, headers=headers)
html = response.content

soup = BeautifulSoup(html, 'lxml')
soup.prettify()

# scraping all links and adding them to a list
links = soup.select('a.list-card-link')
# list(set()) to remove duplicates
href_list_1 = list(set([href['href']
                   for href in links if href['href'][0] == 'h']))
href_list_2 = list(set(['https://www.zillow.com' + href['href']
                   for href in links if href['href'][0] != 'h']))
href_list = href_list_1 + href_list_2

# scraping property prices and adding them to a list
price_tag = soup.select('div.list-card-price')
price_list = list(set([price.text for price in price_tag]))

# scraping all the addresses
address_tag = soup.select('address.list-card-addr')
address_list = list(set([address.get_text().split(' | ')[-1]
                    for address in address_tag]))

# fill the form using above scraped data
CHROME_DRIVER_PATH = 'YOUR DRIVER PATH'
FORM_URL = 'FORM LINK'

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

driver.maximize_window()
for i in range(len(href_list)):
    driver.get(FORM_URL)
    time.sleep(2)
    input_one = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_one.send_keys(address_list[i])
    input_two = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_two.send_keys(price_list[i])
    input_three = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_three.send_keys(href_list[i])
    
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit.click()
