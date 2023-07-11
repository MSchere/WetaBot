import sys
import time

from selenium.webdriver.common.keys import Keys

import bot_utils
from bot_functions import findDishes, getDishes, sortDishList
from config import *

# CONFIGURATION
wetaca_polygonal_url = 'https://wetaca.typeform.com/polygonal-mind'
wetaca_url = 'https://wetaca.com'
wetaca_menu_url = 'https://wetaca.com/carta'
credentials = open('credentials.txt', 'r')  # File to load login credentials
name = credentials.readline().strip()  # Name
email = credentials.readline().strip()  # Email
card_name = name # Card name
card_number = credentials.readline().strip()  # Card number
card_date = credentials.readline().strip()  # Card date
card_cvv = credentials.readline().strip()  # Card CVV

# Global variables
menu_list = []

# BEGIN
print('------------------------WETABOT v' + VERSION + '-------------------------')
browser = sys.argv[1].lower()
dishes_number = int(sys.argv[2])

utils = bot_utils.Utils()
drv = utils.setupDriver(browser, headless=HEADLESS)
act = utils.setupActionChains(drv)

# Open pages
if HEADLESS:
    print('Starting bot on ' + browser + ' in headless mode')
else:
    print('Starting bot on ' + browser + ' in graphical mode')

print('Ordering ' + str(dishes_number) + ' dishes from ' + wetaca_url + '\n')

drv.get(wetaca_url) # navigate to the application home page to load cookies
time.sleep(3)
drv.get(wetaca_menu_url)

### WETACA PAGE:
utils.click('//*[@id="root"]/div/div/div[2]/div[3]/div[2]/button') # Click accept cookies

# Get dishes
menu_list.extend(getDishes('comidas', utils))    
menu_list.extend(getDishes('comidas-ligeras-cenas', utils))
menu_list.extend(getDishes('entrantes', utils))
menu_list.extend(getDishes('postres', utils))

# Get best dishes by macro objectives
menu_list = sortDishList(menu_list, daily_macros, macro_weights)
print('\n- Sorted dishes by score:\n')
print('{:<62} {:<10} {:<10} {:<10}'.format('Dish', 'Price xtra', 'Kcals', 'Score'))
print('{:<62} {:<10} {:<10} {:<10}'.format('-'*62, '-'*10, '-'*10, '-'*10))
for dish in menu_list:
    print('{:<62} {:<10} {:<10} {:<10}'.format(dish.name, str(dish.price) + ' €', str(dish.kcals) + ' kcl', '  ' + str(dish.score) + ' pts'))

# Get the first dishes_number items
menu_list = menu_list[:dishes_number]
total_score = 0
print('\n----------------------------Selected dishes----------------------------')
for dish in menu_list:
    total_score += dish.score
    print(' - ' + str(dish.name) + ' ' + str(dish.price) + '€ kcals: ' + str(dish.kcals) + ' kcl ' + str(dish.score) + ' pts')

print('Total score: ' + str(total_score))
print('-----------------------------------------------------------------------')

### WETACA POLYGONAL PAGE:
drv.get(wetaca_polygonal_url)
# Click start button
utils.click('//*[@id="root"]/main/div[1]/div/div[1]/div[2]/div/section/div[1]/div/div/div/div/div[3]/div/div/div/button')
# Fill name
utils.inputText(name, '//*[@id="block-b33b08b1-e091-4f18-844b-39ac08bc6a1e"]/div/div/div/div/div/div/div/div[2]/div[1]/input')
utils.sendKeys(Keys.ENTER)
# Find the dishes from the list
findDishes(dishes_number, menu_list, utils)
# Click accept
utils.sendKeys(Keys.ENTER)
# Click no
utils.click('//*[@id="block-06ac681e-3d31-47a7-b2cf-ba71fe13b671"]/div/div/div/div/div/div/fieldset/div[2]/div/div[1]/div/div/div[2]/div')
# Click accept
utils.click('//*[@id="block-f18c9b6a-721c-4ce6-a7fb-5b9d64a935ff"]/div/div/div/div/div/div/fieldset/div[2]/div/div[3]/div/div/div/div/div/button')
# Click continue
summary_txt = utils.getText('//*[@id="block-63a610b5-8d37-47cf-a292-f8681d020aa0"]/div/div/div/div/div/div/fieldset/div[1]/div[1]/span/span[1]/span[2]')
total_txt = utils.getText('//*[@id="block-63a610b5-8d37-47cf-a292-f8681d020aa0"]/div/div/div/div/div/div/fieldset/div[1]/div[1]/span/span[1]/span[4]')
print('Summary: ' + summary_txt)
print('Total: ' + total_txt)
utils.sendKeys('a')
# Input email
utils.inputText(email, '//*[@id="block-5690ced4-eb67-4d76-92b0-1f82a7983656"]/div/div/div/div/div/div/div/div[2]/div[1]/input')
utils.sendKeys(Keys.ENTER)
# Input credit card name, number, expiration date and cvv
utils.inputTextByCSS(card_name, "input[placeholder='Jane Smith']")
utils.inputTextByCSS(card_number, "input[placeholder='1234 1234 1234 1234']")
utils.inputTextByCSS(card_date, "input[placeholder='MM / AA']")
utils.inputTextByCSS(card_cvv, "input[placeholder='CVC']")

# Click send
utils.clickButton('//*[@id="block-7d21bce8-2abe-4e03-ba28-0a5345a64b83"]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div/button')
drv.quit()
print('----------------------WETABOT v' + VERSION + ' END-----------------------')