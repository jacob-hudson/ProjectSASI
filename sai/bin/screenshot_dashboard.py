from selenium import webdriver
from PIL import Image
import time
import sys

def poll_all_search(driver):
    return

# def poll_multi_search(driver, number, element):
#     panels = element.find_elements_by_xpath('//*[starts-with(@id, "element")]/div[2]/div/div/div')
#     # panels = element.find_elements_by_xpath('//*[starts-with(@id, "element")]/div[2]/div/div/div').value_of_css_property("opacity")
#     opacity = [len(panels) + 1]
#     min_opacity = "0.0"
#     while min_opacity < "1":
#         if min_opacity == "1":
#             break
#
#         for i, panel in enumerate(panels):
#             opacity[i] = panel.find_element_by_xpath('//*[starts-with(@id, "element")]/div[2]/div/div/div').value_of_css_property("opacity")
#             print opacity[i]
#
#             if opacity[i] < min_opacity:
#                 min_opacity = opacity[i]
#
#             if min_opacity == "1":
#                 break
#     return

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

def take_screenshot(driver):
    driver.save_screenshot('screenshot_splunk.png') # saves screenshot of entire page
    driver.quit()
    return

def crop_screenshot(element, location, size):
    im = Image.open('screenshot_splunk.png') # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png') # saves new cropped image

    return

def auth(driver):
        driver.find_element_by_xpath('//*[@id="username"]').send_keys('username')
        driver.find_element_by_xpath('//*[@id="password"]').send_keys('password')
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/fieldset/input[1]').click()

        return

def main(option, value):
    start_time = time.time()
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    driver.get('url')

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
    else: # something else
        pass

    print time.time() - start_time
    return

if __name__ == "__main__":
    option = sys.argv[1]
    try:
        value = sys.argv[2]
    except:
        value = ""
    main(option, value)
