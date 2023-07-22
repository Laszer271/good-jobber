from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def wait_for_text(browser, xpath):
    print('waiting for element')
    print('Text:', f'"{browser.find_element("xpath", xpath).text}"')
    return len(browser.find_element("xpath", xpath).text) > 10
    # element = WebDriverWait(browser, 10).until(
    #     lambda x: len(x.find_element('xpath' xpath).text) > 10
    # )
    # return element

browser = webdriver.Firefox()
browser.get('https://en.wikipedia.org/wiki/Main_Page')

list_xpath = '//*[@id="vector-main-menu-dropdown-checkbox"]'
random = '/html/body/div[1]/header/div[1]/nav/div/div/div/div/div[2]/div[2]/ul/li[4]/a'
first_par = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2]'

# click on the checkbox
next_button = WebDriverWait(browser, 10).until(lambda x: x.find_element('xpath', list_xpath)) 
# next_button = browser.find_element("xpath", list_xpath)
browser.execute_script("arguments[0].scrollIntoView();", next_button)
next_button.click()

next_button = WebDriverWait(browser, 10).until(lambda x: x.find_element('xpath', random)) 
# next_button = browser.find_element("xpath", random)
browser.execute_script("arguments[0].scrollIntoView();", next_button)
next_button.click()

# not always working:
content = WebDriverWait(browser, 10).until(lambda x: wait_for_text(x, first_par))
content = browser.find_element("xpath", first_par).text
print(content)

# close browser
browser.close()