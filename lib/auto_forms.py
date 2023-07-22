from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

import json

with open('./credentials/openai.txt', 'r') as f:
    openai_api_key = f.read()


def do_work(form, user_info):
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.1)

    # print(form)

    form_template = ""

    review_template = """\
    For the following HTML form, find what information is needed to submit form
    
    The output format as JSON
    If for example Name, Surname and Email is needed to submit form write the output as follows:
    Name: input tag of this Name to write, 
    Surname: input tag of this Surname to write, 
    Email: input tag of this Email to write, 
    
    HTML Form: {form} 
    """

    prompt_template = ChatPromptTemplate.from_template(review_template)
    print(prompt_template)
    messages = prompt_template.format(form=form_template)
    response = llm(messages)
    print(response)
    # print(response.content)


def scrape_web_page(url):
    # Fetch the web page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to fetch the web page.")
        return None

    # Parse the HTML with Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    return soup

if __name__ == '__main__':
    url_to_scrape = "https://nofluffjobs.com/pl/job/programista-web-regular-ework-group-warszawa"

    driver = webdriver.Chrome()

    # Open the web page
    driver.get(url_to_scrape)

    # Find the form element by its tag name "form"
    id_button = '//*[@id="applyButton"]'
    form_tag = '//form'
    aplikuj_button = WebDriverWait(driver, 10).until(lambda x: x.find_element('xpath', id_button))
    driver.execute_script("arguments[0].scrollIntoView();", aplikuj_button)
    aplikuj_button.click()
    form = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.TAG_NAME, 'form'))

    myForm = driver.find_element(By.TAG_NAME, 'form')
    # content_form = driver.find_element("xpath", form_tag)
    

    with open('./data/example_personal_info.json', 'r') as f:
        user_info = json.load(f)

    content = myForm.get_attribute("outerHTML")
    # print(content)
    do_work(content, user_info=user_info)