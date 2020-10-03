# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:01:48 2020

@author: NNAIR
"""

# Importing header files
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait


main_url="https://www.swiggy.com"

# Opening the web driver
driver=webdriver.Chrome()

driver.implicitly_wait(5)
driver.maximize_window()

driver.get(main_url)


# Setting the location for swiggy 
city = 'Mumbai'
search_item = driver.find_element_by_xpath("//*[@id='location']")
search_item.send_keys(city)
WebDriverWait(driver, 500).until(lambda driver: driver.find_element_by_xpath("//*[@class='_2W-T9']"))
cityname = driver.find_element_by_xpath("//*[@class='_2W-T9']")
cityname.click()

# Wait for swiggy.com/restaurnts link to validate location
WebDriverWait(driver,100).until(lambda driver: driver.find_element_by_xpath("//*[@class='_3XX_A']"))


# Initialising dataframe
df = pd.DataFrame(columns=['restaurant name','cuisine','rating','price for two','location','url'])


# Initialsing cuisine options
cuisine_options=["chinese","north indian thalis","italian"]


# Running a loop across the options
for cuisine in cuisine_options:
    
    # Opening cuisine specific URL
    search_url="https://www.swiggy.com/search?q=" + "+".join(str(ci) for ci in cuisine.split())
    driver.get(search_url) 
    
    # Getting all the search result links
    listings=driver.find_elements_by_xpath("//*[@class='_3XX_A']/a")
    current_window=driver.current_window_handle
    
    
    for listing in listings:
        
        # Getting restaurant URL
        url=listing.get_attribute('href')
        
        # Opening the restaurant url
        driver.execute_script('window.open(arguments[0]);',url)
        new_window= driver.window_handles[1]
        driver.switch_to.window(new_window)

        # Getting restaurant name
        rest_name=driver.find_element_by_xpath("//*[@class='_3aqeL']").text
        
        # Getting restaurant cuisines
        cuisine_list=driver.find_element_by_xpath("//*[@class='_3Plw0 JMACF']").text
        print(cuisine_list)
        

        # Getting restaurant rating        
        rest_rating=driver.find_elements_by_xpath("//*[@class='_2l3H5']")[0].text
        print(rest_rating)
        
        # Getting restaurant price
        rest_price=driver.find_elements_by_xpath("//*[@class='_2l3H5']")[2].text
        print(rest_price)
        
        
        # Getting restaurant location
        try:
            rest_location=driver.find_element_by_xpath("//*[@class='Gf2NS _2Y6HW']").text
        except:
            rest_location=driver.find_element_by_xpath("//*[@class='Gf2NS _2Y6HW _2x0-U']").text

        # Adding elements to dataframe
        df = df.append({'restaurant name': rest_name,'cuisine': cuisine_list,'rating':rest_rating,'price for two':rest_price,'location':rest_location, 'url':url}, ignore_index=True)

        # Setting up the size of each cuisine
        if(len(df)%5==0):
            
            driver.close()
            driver.switch_to.window(current_window)
            break
                
            
        # Closing the restaurant URL    
        driver.close()
        driver.switch_to.window(current_window)

# Closing the main driver    
driver.close()


# Saving the data into a csv file
df.to_csv("Swiggy_data.csv",index=False) 
