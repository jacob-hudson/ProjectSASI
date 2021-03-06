from selenium import webdriver
from PIL import Image
import time
import sys
import os
import requests
try:
    from slackclient import SlackClient
except ImportError:
    print "Please install `slackclient` using pip"

# global variables
channel = ""
str_time = str(int(time.time()))

def screenshot_statistics(driver):
    take_screenshot(driver)
    element = driver.find_element_by_xpath('/html/body')
    location = element.location
    size = element.size
    take_screenshot(driver)
    crop_screenshot(element, location, size)
    return

def poll_single_search(driver, number):
    time.sleep(10)
    opacity = "0.0"
    base_id = "element" + number + "-header-"
    while opacity < "1":
        opacity = driver.find_element_by_xpath('//*[starts-with(@id, base_id)]/div[2]/div/div/div').value_of_css_property("opacity")
    return

def screenshot_panel(driver, number):
    panel = "panel" + str(number)
    element = driver.find_element_by_id(panel)
    location = element.location
    size = element.size
    poll_single_search(driver, number)
    take_screenshot(driver)
    crop_screenshot(element, location, size)
    return

def screenshot_row(driver, number):
    row = "row" + str(number)
    element = driver.find_element_by_id(row)
    location = element.location
    size = element.size
    time.sleep(120)
    take_screenshot(driver)
    crop_screenshot(element, location, size)
    return

def screenshot_full(driver):
    element = driver.find_element_by_id("dashboard1")
    location = element.location
    size = element.size
    time.sleep(180)
    take_screenshot(driver)
    crop_screenshot(element, location, size)
    return

def set_filenames():
    int_time = int(time.time())
    str_time = str(int_time)

    return

def take_screenshot(driver):
    set_filenames()
    driver.save_screenshot("splunk_screenshot_raw_" + str(str_time) + ".png") # saves screenshot of entire page
    driver.quit()
    return

def slack_image_upload(screenshot_file):
    slack_token = "xoxb-your-token-here"
    sc = SlackClient(slack_token)

    with open(screenshot_file) as file_content:
        sc.api_call(
            "files.upload",
            channels=channel,
            file=file_content,
            title=""
        )

    return

def crop_screenshot(element, location, size):
    im = Image.open("splunk_screenshot_raw_" + str(str_time) + ".png") # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save("splunk_screenshot_" + str(str_time) + ".png") # saves new cropped image
    os.remove("splunk_screenshot_raw_" + str(str_time) + ".png")
    slack_image_upload("splunk_screenshot_" + str(str_time) + ".png")
    os.remove("splunk_screenshot_" + str(str_time) + ".png")
    return

def auth(driver):
        driver.find_element_by_xpath('//*[@id="username"]').send_keys('username')
        driver.find_element_by_xpath('//*[@id="password"]').send_keys('test_pwd')
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/fieldset/input[1]').click()
        except:
            print "can't log in"

        return

def main(option, value):
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--webdriver-loglevel=NONE'])
    os.remove('ghostdriver.log')
    driver.get(url)

    try: # seeing if the session has expired
        driver.find_element_by_xpath('/html/body/div[1]/header/div[1]/a/i')
    except: # session has expired, need to re-auth
        auth(driver)

    time.sleep(10) # have to let the UI load

    if (option == "full"):
        screenshot_full(driver)
    elif (option == "panel"):
        screenshot_panel(driver, value)
    elif (option == "row"):
        screenshot_row(driver, value)
    elif (option == "statistics"):
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/ul/li[3]/a').click()
        except:
            pass
        screenshot_statistics(driver)
    elif (option == "visualization"):
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/ul/li[4]/a').click()
        except:
            pass
        screenshot_visualization(driver)
    else: # something else
        pass

    return

if __name__ == "__main__":
    url = sys.argv[1]
    option = sys.argv[2]
    channel = sys.argv[3]
    try:
        value = sys.argv[4]
    except:
        value = ""
    main(option, value)
