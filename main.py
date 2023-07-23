import streamlit as st
import os, sys

@st.cache_resource
def installff():
  print('installing firefox')
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

import numpy as np
import re
from io import BytesIO
import base64
from PIL import Image
import json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions

from html_components import JOB_OFFER, DEFAULT_STYLE
from lib.utils import ChangeButtonColour


def get_content_from_wiki():
    def wait_for_text(browser, xpath):
        print('waiting for element')
        print('Text:', f'"{browser.find_element("xpath", xpath).text}"')
        return len(browser.find_element("xpath", xpath).text) > 10
        # element = WebDriverWait(browser, 10).until(
        #     lambda x: len(x.find_element('xpath' xpath).text) > 10
        # )
        # return element

    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)
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
    return content


def gift_idea_to_amazon(idea: str, budget_min: float, budget_max: float):
    pass


def update_image(interests: str, gender: str, age: str, gift_ideas, index):
    pass


def generate_text_and_image(interests: str, gender: str, age: str):
    pass


def populate_column(img_col, content_col, output_image, cnt, budget_min, budget_max):
    pass


def image_to_b64(img):
    pass


def img_to_html(img):
    pass


def add_job_position():
    next_job = max(st.session_state.jobs) + 1
    st.session_state.jobs.append(next_job)


def del_job_position(i):
    def del_job():
        to_del = st.session_state.jobs.index(i)
        del st.session_state.jobs[to_del]
    return del_job


def set_searching():
    # st.session_state.recommendations.append(get_content_from_wiki())
    st.session_state.searching = True
    st.session_state.get_jobs = True


def get_job_recommendations(candidate_preferences):
    # for now completely ignore the preferences
    # this should be run only once when job hunt is started
    print(candidate_preferences)

    with open('./data/job_offers.json', 'r') as f:
        job_list = json.load(f)

    return job_list


def del_job_offer(i):
    def del_job():
        del st.session_state.job_offers[i]
    return del_job


def accept_job_offer(i):
    # TODO: add the job to the list of accepted jobs
    def accept_job():
        del st.session_state.job_offers[i]
    return accept_job


def accept_all_job_offers(n_jobs):
    def accept_all():
        for i in range(n_jobs):
            accept_job_offer(0)()
    return accept_all


N_OFFERS_TO_SHOW = 5

if __name__ == '__main__':

    st.set_page_config(
        page_title='Streamlit cheat sheet',
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _ = installff()

    # st.set_page_config(layout="wide")
    N_IDEAS_TO_SHOW = 10

    model_gui = st.container()

    if 'jobs' not in st.session_state:
        st.session_state.jobs = [1]
    if 'searching' not in st.session_state:
        st.session_state.searching = False
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'get_jobs' not in st.session_state:
        st.session_state.get_jobs = False 

    job_titles = []

    with model_gui:
        st.markdown(DEFAULT_STYLE, unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Good Job Finder</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Find a job that matches your skills and interests</h3>", unsafe_allow_html=True)
        
        info_col, output_col = st.columns([1, 1])

        with info_col:
            st.markdown("<h4 style='text-align: center;'>Upload CV</h4>", unsafe_allow_html=True)
            # st.subheader('Upload CV')
            st.file_uploader('Upload your CV', type=['pdf'])
            st.divider()

            st.markdown("<h4 style='text-align: center;'>Your personal information</h4>", unsafe_allow_html=True)
            name_col, surname_col = st.columns(2)
            name = name_col.text_input('Name', placeholder='Oli')
            surname = surname_col.text_input('Surname', placeholder='Ali')
            birthdate = st.date_input('Birthdate', value=None, min_value=None, max_value=None)
            address = st.text_input('Address', placeholder='123 Main St, New York, NY 10030')
            email_col, nr_col = st.columns(2)
            email = email_col.text_input('Email', placeholder='person@gmail.com')
            phone_nr = nr_col.text_input('Phone number', placeholder='+1 123 456 789')
            st.divider()

            st.markdown("<h4 style='text-align: center;'>Your preferences</h4>", unsafe_allow_html=True)

            for i in st.session_state.jobs:
                del_col, job_col = st.columns([0.1, 0.9])
                with job_col:
                    job_titles.append(st.text_input(f'Job title {i}', placeholder='Data Scientist'))
                with del_col:
                    st.write(' ')
                    st.button('X', key=f'delete_job_{i}', on_click=del_job_position(i))

            print(st.session_state.jobs)
            add_more = st.button('Add more viable job positions', on_click=add_job_position)

            min_col, max_col = st.columns([1, 1]) 
            min_wage = min_col.number_input('Min Monthly Net $', value=1_000, min_value=0, step=50)
            max_wage = max_col.number_input('Max Monthly Net $', value=2_000, min_value=0, step=50)

            skills = st.text_area('Provide tags for skills and interests delimited by comma',
                                  placeholder='python, data science, machine learning')
            benefits = st.text_area('Provide benefits you are looking for in a job delimited by comma',
                                    placeholder='remote, flexible hours, health insurance')
            experience = st.selectbox('Years of experience', options=['No experience', '0-1 years', '1-2 years', '2-3 years',
                                                                     '3-5 years', '5-8 years', '8+ years'])
            

            _, submit_col = st.columns([0.70, 0.30])
            with submit_col:
                st.write('')
                st.write('')
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.css-z5fcl4.ea3mdgi4 > div:nth-child(1) > div > div:nth-child(2) > div > div.css-ocqkz7.e1f1d6gn3 > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(16) > div.css-1s60f5m.e1f1d6gn1 > div:nth-child(1) > div > div:nth-child(3) > div > div
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.css-z5fcl4.ea3mdgi4 > div:nth-child(1) > div > div:nth-child(2) > div > div.css-ocqkz7.e1f1d6gn3 > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(16) > div.css-1s60f5m.e1f1d6gn1 > div:nth-child(1) > div > div:nth-child(4) > div
                st.markdown("""
                <style>
                div:nth-child(4) > div > button {
                    background-color: #559955;
                    border-color: #226622;
                    color:#ffffff;
                }
                div:nth-child(4) > div > button:hover {
                    background-color: #448844;
                }
                </style>""", unsafe_allow_html=True)
                submit = submit_col.button('Start Job Hunt', on_click=set_searching, use_container_width=True, type='primary')
                # ChangeButtonColour('Start Job Hunt', font_color='white', background_color=0x55cc77)
                

        if st.session_state.searching:
            if st.session_state.get_jobs:
                # Values are loaded from all the streamlit fields
                comm_experience = f'With commercial experience of {experience}' if experience != 'No experience' else 'With no commercial experience'
                person_description = f'''
                Interested in following job titles: {', '.join(job_titles)} or similar
                Looking for a job with a salary between {min_wage} and {max_wage} $/month
                Especially interested in following skills and technologies: {skills} or similar
                Looking for a job with following benefits: {benefits}
                {comm_experience}
                '''
                st.session_state.job_offers = get_job_recommendations(person_description)
                st.session_state.get_jobs = False
            with output_col:
                st.markdown("<h4 style='text-align: center;'>Job recommendations</h4>", unsafe_allow_html=True)

                ### ADD THE RECOMMENDATIONS ###
                for i, job_offer in enumerate(st.session_state.job_offers[:N_OFFERS_TO_SHOW]):
                    _, job_col, buttons_col = st.columns([0.05, 0.73, 0.22])

                    job_title = job_offer['JobTitle']
                    company = job_offer['Company']
                    url = job_offer['Url']
                    description = job_offer['Description'] # TODO: to be changed to short description

                    current_div = JOB_OFFER.format(title=job_title, company=company, url=url, description=description)

                    with job_col:
                        job_titles.append(st.markdown(f'{current_div}', unsafe_allow_html=True))
                        st.write('')
                    with buttons_col:
                        st.write('')
                        print(i)
                        st.button('Decline', key=f'delete_job_offer_{i}', on_click=del_job_offer(i), use_container_width=True)
                        st.button('Apply', key=f'accept_job_offer{i}', on_click=accept_job_offer(i), use_container_width=True)

                _, accept_all_col = st.columns([0.85, 0.15])
                with accept_all_col:
                    st.write('')
                    st.write('')
                    st.markdown("""
                    <style>
                    div:nth-child(4) > div > button {
                        background-color: #559955;
                        border-color: #226622;
                        color:#ffffff;
                    }
                    div:nth-child(4) > div > button:hover {
                        background-color: #448844;
                    }
                    </style>""", unsafe_allow_html=True)
                    st.button(
                        'Accept all', key=f'accept_all_job_offers', type='primary',
                        on_click=accept_all_job_offers(min(N_OFFERS_TO_SHOW, len(st.session_state.job_offers))),
                        use_container_width=True)

