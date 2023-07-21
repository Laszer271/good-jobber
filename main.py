import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO
import base64
from PIL import Image

# from generating.text_generation import TextGenerator
# from generating.image_generation import ImageGenerator
# from generating.text_generation import make_prompt_data_for_gpt

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
    st.session_state.n_jobs += 1


def del_job_position(i):
    def del_job():
        st.session_state.n_jobs -= 1
        del job_titles[i]
    return del_job
    

if __name__ == '__main__':
    # st.set_page_config(layout="wide")
    N_IDEAS_TO_SHOW = 10

    model_gui = st.container()

    if 'n_jobs' not in st.session_state:
        st.session_state.n_jobs = 1
    if 'searching' not in st.session_state:
        st.session_state.searching = True
    job_titles = []

    with model_gui:
        st.header('Good Job Finder')
        st.write('Find a job that matches your skills and interests')
        
        info_col, output_col = st.columns([1, 1])

        with info_col:
            st.subheader('Upload CV')
            st.file_uploader('Upload your CV', type=['pdf', 'docx', 'doc'])

            st.subheader('Your personal information')
            name_col, surname_col = st.columns(2)
            name = name_col.text_input('Name', placeholder='Oli')
            surname = surname_col.text_input('Surname', placeholder='Ali')
            birthdate = st.date_input('Birthdate', value=None, min_value=None, max_value=None)
            address = st.text_input('Address', placeholder='123 Main St, New York, NY 10030')

            st.subheader('Your preferences')

            for i in range(st.session_state.n_jobs):
                del_col, job_col = st.columns([0.2, 0.8])
                with job_col:
                    job_titles.append(st.text_input(f'Job title {i+1}', placeholder='Data Scientist'))
                with del_col:
                    st.button('X', key=f'delete_job_{i+1}', on_click=del_job_position(i))

            print(st.session_state.n_jobs)
            add_more = st.button('Add more viable job positions', on_click=add_job_position)

            min_col, max_col = st.columns([1, 1]) 
            min_wage = min_col.number_input('Min Monthly Net $', value=1_000, min_value=0, step=50)
            max_budget = max_col.number_input('Max Monthly Net $', value=2_000, min_value=0, step=50)

            st.text_area('Provide tags for skills and interests delimited by comma',
                          placeholder='python, data science, machine learning')
            st.text_area('Provide benefits you are looking for in a job delimited by comma',
                          placeholder='remote, flexible hours, health insurance')


        if st.session_state.searching:
            with output_col:
                st.subheader('Job recommendations')

        # min_col, max_col, disp_col = st.columns([0.5, 0.5, 1]) # Then 4 columns for min/max budget
        # sel_col, img_col = st.columns(2) # First 2 columns, 1 for input, 2nd for output
        # sel_col_final, prev_col, next_col = st.columns([1, 0.5, 0.5])  # At the end 3 columns, the first for generate button

        # age = sel_col.number_input('How old is the person the gift is for', min_value=0, max_value=200, value=15    )

        # gender = sel_col.selectbox('What is the gender of the person the gift is for',
        #                       options=['Woman', 'Man', 'Non-binary'], index=0)

        # interests = sel_col.text_input(
        #     'Describe the person interests', placeholder='swimming, car racing', max_chars=2000)

        # min_budget = min_col.number_input('Min $', value=10.0, min_value=0.0)
        # max_budget = max_col.number_input('Max $', value=50.0, min_value=0.0)

        # if 'is_generated' not in st.session_state:
        #     st.session_state.is_generated = False
        # if 'images' not in st.session_state:
        #     st.session_state.images = []
        # if 'count' not in st.session_state:
        #     st.session_state.count = 0

        # should_generate = sel_col_final.button('Generate', key='generate')
        # should_update = next_col.button('Show next idea', key='next_idea')
        # show_previous = prev_col.button('Show previous idea', key='prev_idea')

        # if should_generate:
        #     st.session_state.count = 0
        #     st.session_state.is_generated = True
        #     st.session_state.ideas, output_image = generate_text_and_image(interests, gender, age)
        #     st.session_state.images =[output_image]
        #     populate_column(img_col, disp_col, output_image, 0, min_budget, max_budget)
        #     print('=' * 50)
        #     print(type(output_image))
        #     print('=' * 50)

        # if show_previous:
        #     if st.session_state.is_generated:
        #         if st.session_state.count == 0:
        #             output_image = st.session_state.images[st.session_state.count]
        #             populate_column(img_col, disp_col, output_image, st.session_state.count, min_budget, max_budget)
        #             disp_col.write(f'There are no previous ideas, the current one is the first one :)')
        #         else:
        #             st.session_state.count -= 1
        #             output_image = st.session_state.images[st.session_state.count]
        #             populate_column(img_col, disp_col, output_image, st.session_state.count, min_budget, max_budget)
        #     else:
        #         disp_col.write(f'Consider generating some ideas first :)')

        # if should_update:
        #     if st.session_state.is_generated:
        #         st.session_state.count += 1
        #         if st.session_state.count < len(st.session_state.images):
        #             output_image = st.session_state.images[st.session_state.count]
        #             populate_column(img_col, disp_col, output_image, st.session_state.count, min_budget, max_budget)
        #         elif st.session_state.count < N_IDEAS_TO_SHOW:
        #             output_image = update_image(interests, gender, age, st.session_state.ideas, st.session_state.count)
        #             st.session_state.images.append(output_image)
        #             populate_column(img_col, disp_col, output_image, st.session_state.count, min_budget, max_budget)
        #         else: 
        #             output_image = update_image(interests, gender, age, 'sad face', st.session_state.count)
        #             populate_column(img_col, disp_col, output_image, st.session_state.count, min_budget, max_budget)
        #     else:
        #         disp_col.write(f'Consider generating some ideas first :)')
        #     st.session_state.count = min(st.session_state.count, N_IDEAS_TO_SHOW)
                    
