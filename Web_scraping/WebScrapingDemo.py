# -*- coding: utf-8 -*-
"""

@author: nnair
"""
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait

main_url="https://www.swiggy.com/search?q=chinese"

driver= webdriver.Chrome()

# Good practices
# driver.implicitly_wait(5)
driver.maximize_window()

driver.get(main_url)


city='Mumbai'

search_item= driver.find_element_by_id("location")
search_item.send_keys(city)

WebDriverWait(driver, 500).until(lambda driver: driver.find_element_by_xpath("//*[@class='_2W-T9']"))

cityname=driver.find_element_by_xpath("//*[@class='_2W-T9']")
cityname.click()


df=pd.DataFrame(columns=['restaurant name'])

WebDriverWait(driver, 500).until(lambda driver: driver.find_element_by_xpath("//*[@class='_3XX_A']"))


search_url="https://www.swiggy.com/search?q=Chinese"
driver.get(search_url)

WebDriverWait(driver, 500).until(lambda driver: driver.find_element_by_xpath("//*[@class='nA6kb']"))

# rest_names= driver.find_elements_by_xpath("//*[@class='nA6kb']")
# print(rest_names)

# for rest in rest_names:
#          print(rest.text)
                   
listings=driver.find_elements_by_xpath("//*[@class='_3XX_A']/a")

current_window=driver.current_window_handle

for listing in listings:
    url= listing.get_attribute('href')
    
    driver.execute_script('window.open(arguments[0]);',url)
    new_window=driver.window_handles[1]
    driver.switch_to.window(new_window)
    
    
    rest_name=driver.find_element_by_xpath("//*[@class='_3aqeL']").text
    print(rest_name)
    
    df= df.append({'restaurant name': rest_name}, ignore_index=True)
    
    
    if(len(df)%5==0):
        driver.close()
        driver.switch_to.window(current_window)
        break
    
    driver.close()
    driver.switch_to.window(current_window)
   
driver.close()    
    
print(df)    
    
    

