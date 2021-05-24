from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
PATH = "./chromedriver.exe"
driver = webdriver.Chrome(executable_path = r"./chromedriver.exe", options = options)

driver.get("https://www.covid19india.org/")

delay = 10 # in seconds

stateInput = input()

formatString = "/html/body/div/div/div[@class='Home']/div[@class='home-left']/div[@class='Table']/div[@class='table-container']/div[@class='table fadeInUp']/div[@class='row']"
formatStringDistrict = "/html/body/div/div/div[@class='Home']/div[@class='home-left']/div[@class='Table']/div[@class='table-container']/div[@class='table fadeInUp']/div[@class='row district']"

fields = ['District', 'Total Cases', 'Active', 'Recovered', 'Deceased']
found = 0
try:
    for i in range(1,37):
        stateList = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, formatString+"["+str(i)+"]")))
        listData = stateList.text.split('\n')
        if (stateInput.lower() == listData[0].lower()):
            found = 1
            driver.execute_script("arguments[0].click();", stateList)
            listSel = WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH, formatStringDistrict)))
            districtData = []
            for x in listSel:
                listPerDist = x.text.split('\n')
                listnew = []
                cnt = 0
                for val in listPerDist:
                    if cnt == 5:
                        districtData.append(listnew)
                        break
                    if val[0] != '↑' and val[0] != '-':
                        cnt += 1
                        listnew.append(val)
            df = pd.DataFrame(districtData, columns = fields)
            df.index += 1
            df.to_csv("./"+stateInput+".csv")
            df.to_excel('./'+stateInput+'.xlsx')
            print ("The files have been created and saved in the same directory.")
            break
    if found == 0:
        print("Please enter the correct name of the state!")

except TimeoutException:
    print ("The page didn't load!")

driver.quit()