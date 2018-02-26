from selenium import webdriver
from PIL import Image
import time
import sys

# global variables
raw_file = ""
final_file = ""
channel = ""

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
    raw_file = "splunk_screenshot_" + str_time + "_raw.png"
    final_file = "splunk_screenshot_" + str_time + ".png"

    return

def take_screenshot(driver):
    set_filenames()
    driver.save_screenshot(raw_file) # saves screenshot of entire page
    driver.quit()
    return

def slack_image_upload(screenshot_file):
    data = {}
    data['token'] = "bot_token"
    data['file'] = screenshot_file
    data['channel'] = channel

    filepath = data['file']
    files = {
        'file': (filepath, open(filepath, 'rb'), 'image/jpg', {
            'Expires': '0'
        })
    }
    data['media'] = files

    response = requests.post(
        url='https://slack.com/api/files.upload',
        data=data,
        headers={'Accept': 'application/json'},
        files=files)

    return

def crop_screenshot(element, location, size):
    im = Image.open(raw_file) # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(final_file) # saves new cropped image
    slack_image_upload(final_file)
    return

def auth(driver):
        driver.find_element_by_xpath('//*[@id="username"]').send_keys('slack_screenshots')
        driver.find_element_by_xpath('//*[@id="password"]').send_keys('test_password')
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/form/fieldset/input[1]').click()
        except:
            print "can't log in"

        return

def main(option, value):
    start_time = time.time()
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
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

    print time.time() - start_time
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
