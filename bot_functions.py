import re
import time
from collections import namedtuple

from selenium.webdriver.common.by import By

dish_re = r'([^\s].*?)\s*\(' # Regex to get dish name and price

Food = namedtuple('food', ['name', 'price', 'kcals', 'fat', 'sat_fat', 'protein', 'carbs', 'sugar', 'fiber', 'salt', 'score'])

def getDishes(div_id, utils) -> list:
    cnt = 1
    drv = utils.drv
    menu_list = []
    while True:
        try:
            food_name = drv.find_element(By.XPATH, '//*[@id="'+div_id+'"]/div/div['+str(cnt)+']/div/a/div[2]/div[1]').text
            food_price = drv.find_element(By.XPATH, '//*[@id="'+div_id+'"]/div/div['+str(cnt)+']/div/div/div[1]').text[:-1]
            if food_price == '': 
                food_price = '+ 0'
            nutrients = []
            utils.openLinkInNewTab('//*[@id="'+div_id+'"]/div/div['+str(cnt)+']/div/a')         
            kcals = float(utils.getText('//*[@id="root"]/div/div/div[2]/div[3]/div/div[2]/div[2]/table/tbody/tr[2]/td[3]').replace(',', '.')[:-4])
            for i in range(3, 10): # Get nutritional info
                nutrients.append(float(utils.getText('//*[@id="root"]/div/div/div[2]/div[3]/div/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[3]').replace(',', '.')[:-2]))
            drv.close() # Return to previous page
            drv.switch_to.window(drv.window_handles[0])
            current_food = Food(food_name, food_price, kcals, nutrients[0], nutrients[1], nutrients[2], nutrients[3], nutrients[4], nutrients[5], nutrients[6], None)
            menu_list.append(current_food)
            print(f'Got {cnt} dishes from {div_id}', end='\r', flush=True)
            cnt += 1
        except:
            print()
            return menu_list
            

def findDishes(dishes_number, menu_list, utils):
    found_cnt = 0
    cnt = 1
    drv = utils.drv
    while True:
        try:
            if found_cnt == dishes_number:
                print()
                print('All dishes found')
                break
            food_description = drv.find_element(By.XPATH, '//*[@id="block-5d23f2af-f305-4473-a656-0db498f1d989"]/div/div/div/div/div/div/fieldset/div[2]/div/div[2]/div/div/div['+str(cnt)+']/div/div/div/div[3]/div[2]/div').text
            match = re.match(dish_re, food_description)
            if match:
                found_dish = match.group(1).strip()
            else:
                print('No match for ' + food_description)
                found_dish = None

            for food in menu_list:
                if food.name == found_dish:
                    utils.click('//*[@id="block-5d23f2af-f305-4473-a656-0db498f1d989"]/div/div/div/div/div/div/fieldset/div[2]/div/div[2]/div/div/div['+str(cnt)+']/div')
                    found_cnt += 1
            time.sleep(0.1)
            print(f'Added {found_cnt} dishes to order', end='\r', flush=True)
            cnt += 1
        except:
            print('Not all dishes found')
            break

def sortDishList(food_list, daily_macro, macro_weights):
    sorted_list = []
    protein_weight = macro_weights["protein"]
    carbs_weight = macro_weights["carbs"]
    fat_weight = macro_weights["fat"]

    for food in food_list:
        # Calculate the deviation of each dish's macronutrient content from your daily objectives.
        protein_deviation = abs(food.protein - daily_macro["protein"])
        carbs_deviation = abs(food.carbs - daily_macro["carbs"])
        fat_deviation = abs(food.fat - daily_macro["fat"])

        # Normalize the deviation scores to a comparable scale.
        protein_deviation /= daily_macro["protein"]
        carbs_deviation /= daily_macro["carbs"]
        fat_deviation /= daily_macro["fat"]

        # Apply the weights.
        protein_deviation *= protein_weight
        carbs_deviation *= carbs_weight
        fat_deviation *= fat_weight

        # Calculate a total score for each dish based on the deviations.
        total_score = (protein_deviation + carbs_deviation + fat_deviation) / (protein_weight + carbs_weight + fat_weight)

        # Invert the score and present it as a percentage (higher score is better).
        total_score = 100 - total_score * 100

        # Add the food item with its score to the list.
        sorted_list.append(food._replace(score=round(total_score)))

    # Sort the list of Food items based on their scores (ascending order).
    sorted_list.sort(key=lambda x: x.score, reverse=True)

    return sorted_list