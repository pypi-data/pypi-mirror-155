from selenium import webdriver
import time
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def checkup(site):
    print('''
    ░██████╗███████╗░█████╗░██████╗░██╗░░░██╗
    ██╔════╝██╔════╝██╔══██╗██╔══██╗╚██╗░██╔╝
    ╚█████╗░█████╗░░██║░░██║██████╔╝░╚████╔╝░
    ░╚═══██╗██╔══╝░░██║░░██║██╔═══╝░░░╚██╔╝░░
    ██████╔╝███████╗╚█████╔╝██║░░░░░░░░██║░░░
    ╚═════╝░╚══════╝░╚════╝░╚═╝░░░░░░░░╚═╝░░░
    ''')
    print('''
    █▄▄ █▄█   █▀▄ █░█ █ █▀█ ▄▀█ ░░█   █▄▄ █▀▀ █▀█ █
    █▄█ ░█░   █▄▀ █▀█ █ █▀▄ █▀█ █▄█   █▄█ ██▄ █▀▄ █
    ''')

    # print("\n\n")
    # site = input('''
    # █▀▀ █▄░█ ▀█▀ █▀▀ █▀█   █▄█ █▀█ █░█ █▀█   █▀ █ ▀█▀ █▀▀   █▄░█ ▄▀█ █▀▄▀█ █▀▀ ▀
    # ██▄ █░▀█ ░█░ ██▄ █▀▄   ░█░ █▄█ █▄█ █▀▄   ▄█ █ ░█░ ██▄   █░▀█ █▀█ █░▀░█ ██▄ ▄
    # ''')

    chromeOptions=Options()
    chromeOptions.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager(path=os.getcwd()).install(), options=chromeOptions)

    # driver = webdriver.Chrome('./chromedriver')
    driver.get("https://seositecheckup.com/")

    time.sleep(5)

    search_bar = driver.find_element_by_xpath('//*[@id="field-10"]')
    search_bar.send_keys(site)

    driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/section[1]/div/div/div[1]/div[2]/form/div/div[1]/button').click()

    print("Please wait, we are analyzing your site!!!")
    time.sleep(5)
    print("Getting SEO Score...")
    time.sleep(5)
    print("Getting Site Issues...")
    time.sleep(5)
    print("Almost Ready...")
    time.sleep(5)

    seo_score = driver.find_element_by_xpath('//*[@id="seo-score"]/div/div[2]/div[1]/div[1]/div/div/span').text
    time.sleep(5)
    print("\n\n")
    print('''
    █▀ █▀▀ █▀█   █▀ █▀▀ █▀█ █▀█ █▀▀
    ▄█ ██▄ █▄█   ▄█ █▄▄ █▄█ █▀▄ ██▄
    ''')
    print(seo_score)

    issue_to_fix = driver.find_element_by_xpath('//*[@id="header-seo-summary"]/div[3]/div').text
    time.sleep(2)
    print("\n\n")
    print('''
    █ █▀ █▀ █░█ █▀▀ █▀   ▀█▀ █▀█   █▀▀ █ ▀▄▀
    █ ▄█ ▄█ █▄█ ██▄ ▄█   ░█░ █▄█   █▀░ █ █░█
    ''')
    print(issue_to_fix)
