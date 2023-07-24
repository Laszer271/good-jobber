import streamlit as st
import os, sys

@st.cache_resource
def installff():
  print('installing firefox')
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

if 'OPENAI_API_KEY' not in os.environ:
    with open('./credentials/openai.txt', 'r') as f:
        os.environ["OPENAI_API_KEY"] = f.read()

import pandas as pd
from time import sleep
from tempfile import NamedTemporaryFile
from datetime import datetime

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from html_components import JOB_OFFER, DEFAULT_STYLE
from lib.utils import ChangeButtonColour
from lib.auto_forms import run_selenium
from lib.llm_describe import get_description


N_OFFERS_TO_SHOW = 5
N_OFFERS_TO_STORE = 100


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

    data = pd.read_json('./data/all_offers_with_desc_pruned.json', orient='index').reset_index(drop=True).sample(frac=1)
    data['Url'] = 'https://nofluffjobs.com' + data['Url'] + '?lang=en'

    # db = Chroma.from_texts(data['Description'].tolist(), HuggingFaceEmbeddings())
    search_results = st.session_state.db.similarity_search(candidate_preferences, k=N_OFFERS_TO_STORE)
    search_results = [doc.page_content for doc in search_results]

    data = data.set_index('Description').loc[search_results].reset_index()
    data['ShortDescription'] = None
    # data = data.loc[data['Description'].isin(search_results)].reset_index(drop=True)

    return data


def del_job_offer(i):
    def del_job():
        # del st.session_state.job_offers[i]
        # print('To drop:', i)
        # print(st.session_state.job_offers)
        st.session_state.job_offers.drop(index=i, inplace=True)
        st.session_state.job_offers.reset_index(drop=True, inplace=True)
    return del_job


def accept_job_offer(i, personal_data, fake=False):
    # TODO: add the job to the list of accepted jobs
    def accept_job():
        with NamedTemporaryFile(dir='.', suffix=f'_{personal_data["Surname"]}{personal_data["Name"]}_CV.pdf') as f:
            f.write(personal_data['CV'].getbuffer())
            cv_path = f.name
            personal_data['cv_path'] = cv_path
            url = st.session_state.job_offers.iloc[i]['Url']
            if not fake:
                run_selenium(url, personal_data) # Runs the bot to apply for the job

        del_job_offer(i)()
    return accept_job


def accept_all_job_offers(n_jobs, personal_data, fake=False):
    def accept_all():
        for i in range(n_jobs):
            accept_job_offer(0, personal_data, fake=fake)()
    return accept_all


def populate_offers(person_description, personal_data):
    for i, (_, job_offer) in enumerate(st.session_state.job_offers.iloc[:N_OFFERS_TO_SHOW].iterrows()):
        _, job_col, buttons_col = st.columns([0.05, 0.73, 0.22])

        with job_col:
            with st.spinner('Personalizing the job offers...'):
                job_title = job_offer['JobTitle']
                company = job_offer['Company']
                url = job_offer['Url']
                description = job_offer['Description'] 
                short_description = job_offer['ShortDescription']
                short_description = '' # TODO: erase that

                if short_description is None:
                    short_description = get_description(description, person_description)
                    st.session_state.job_offers.iloc[i]['ShortDescription'] = short_description
                else:
                    sleep(0.0)

                current_div = JOB_OFFER.format(title=job_title, company=company, url=url, description=short_description)

                # Adding the job offer to the list of recommendations
                job_titles.append(st.markdown(f'{current_div}', unsafe_allow_html=True))
                st.write('')
            with buttons_col:
                st.write('')
                print(i)
                st.button('Decline', key=f'delete_job_offer_{i}', on_click=del_job_offer(i), use_container_width=True)
                st.button('Apply', key=f'accept_job_offer{i}', on_click=accept_job_offer(i, personal_data), use_container_width=True)


if __name__ == '__main__':

    st.set_page_config(
        page_title='Streamlit cheat sheet',
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _ = installff()

    # initialize our database
    if 'db' not in st.session_state:
        data = pd.read_json('./data/all_offers_with_desc_pruned.json', orient='index').reset_index(drop=True).sample(frac=1)
        st.session_state.db = Chroma.from_texts(data['Description'].tolist(), HuggingFaceEmbeddings())    

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
            cv = st.file_uploader('Upload your CV', type=['pdf'])
            st.divider()

            st.markdown("<h4 style='text-align: center;'>Your personal information</h4>", unsafe_allow_html=True)
            name_col, surname_col = st.columns(2)
            name = name_col.text_input('Name', placeholder='Oli', value='Oli')
            surname = surname_col.text_input('Surname', placeholder='Ali', value='Ali')
            birthdate = st.date_input('Birthdate', 
                                      value=datetime(2000, 10, 12),
                                      min_value=datetime(1900, 1, 1),
                                      max_value=datetime.now())
            address = st.text_input('Address',
                                    placeholder='123 Main St, New York, NY 10030',
                                    value='123 Main St, New York, NY 10030'
                                    )
            email_col, nr_col = st.columns(2)
            email = email_col.text_input('Email',
                                         placeholder='person@gmail.com',
                                         value='person@gmail.com')
            phone_nr = nr_col.text_input('Phone number',
                                         placeholder='+1 123 456 789',
                                         value='+1 123 456 789')
            st.divider()

            st.markdown("<h4 style='text-align: center;'>Your preferences</h4>", unsafe_allow_html=True)

            for i in st.session_state.jobs:
                del_col, job_col = st.columns([0.1, 0.9])
                with job_col:
                    job_titles.append(st.text_input(f'Job title {i}',
                                                    placeholder='Data Scientist',
                                                    value='Data Scientist'))
                with del_col:
                    st.write(' ')
                    st.button('X', key=f'delete_job_{i}', on_click=del_job_position(i))

            print(st.session_state.jobs)
            add_more = st.button('Add more viable job positions', on_click=add_job_position)

            min_col, max_col = st.columns([1, 1]) 
            min_wage = min_col.number_input('Min Monthly Net $', value=1_000, min_value=0, step=50)
            max_wage = max_col.number_input('Max Monthly Net $', value=2_000, min_value=0, step=50)

            skills = st.text_area('Provide tags for skills and interests delimited by comma',
                                  placeholder='python, data science, machine learning',
                                  value='python, data science, machine learning')
            benefits = st.text_area('Provide benefits you are looking for in a job delimited by comma',
                                    placeholder='remote, flexible hours, health insurance',
                                    value='remote, flexible hours, health insurance')
            experience = st.selectbox('Years of experience',
                                      options=['No experience', '0-1 years', '1-2 years', '2-3 years',
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
            # Values are loaded from all the streamlit fields
            comm_experience = f'With commercial experience of {experience}' if experience != 'No experience' else 'With no commercial experience'
            person_description = f'''
            Interested in following job titles: {', '.join(job_titles)} or similar
            Looking for a job with a salary between {min_wage} and {max_wage} $/month
            Especially interested in following skills and technologies: {skills} or similar
            Looking for a job with following benefits: {benefits}
            {comm_experience}
            '''

            personal_data = {
                'CV': cv,
                'Name': name,
                'Surname': surname,
                'Email': email,
                'Phone': phone_nr,
                'Address': address,
                'Birthdate': str(birthdate),
            }

            if st.session_state.get_jobs:
                st.session_state.job_offers = get_job_recommendations(person_description)
                st.session_state.get_jobs = False

            with output_col:
                st.markdown("<h4 style='text-align: center;'>Job recommendations</h4>", unsafe_allow_html=True)
                # _, apply_all_col, _ = st.columns([0.35, 0.3, 0.35])
                # with apply_all_col:
                #     agree = st.button('Apply to all', type='primary')

                ### ADD THE RECOMMENDATIONS ###
                # if agree:
                #     while len(st.session_state.job_offers) > 0:
                #         populate_offers(person_description, personal_data)
                #         accept_all_job_offers(min(N_OFFERS_TO_SHOW, len(st.session_state.job_offers)), personal_data, fake=True)()
                # else:
                populate_offers(person_description, personal_data)

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
                        on_click=accept_all_job_offers(min(N_OFFERS_TO_SHOW, len(st.session_state.job_offers)), personal_data, fake=True),
                        use_container_width=True)
                    
                    


