import openai as ai

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def run(name):
    realPreferencesAndExperience = """
    earnings: salary from 1k usd to 3k usd,
    technology: data science, python and pytorch,
    experience: works with  mentioned technologies for over two years,
    location: Warsaw"""

    realJobOffer = """
    earnings: 1200$, 
    technology: data science, python, pytorch would be nice,
    experience: at least one year experience in one of required fields, 
    location: Warsaw or fully remote"""


    preferencesAndExperience = """
    earnings: salary more than 2000 usd,
    technology: working with .net and angular,
    experience: maximum 1 year experience required,
    location: remote or London"""

    jobOffer = """
    earnings: 2500$, 
    technology: aspNetCore, entityframework, .net,
    experience: no experience required, 
    location: Warsaw or fully remote"""
    result = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are assisting clients to 
            find out if they meet job requirements and a job will suit client's preferences. 
            You give verdicts: Ok, not ideal <- client doesn't meet all requirements but more than less and
            job meets job preferences;
             Perfect <- client meets every job requirement and meets client job preferences in general; 
             Maybe <- client meets requirements partially or preferences are met partially; 
             Pass <- client would not get a job or doesn't meet client preferences"""},
            {"role": "user", "content": f"""Hello assistant, 
            please look at my job preferences and experience: 
            {preferencesAndExperience}.
            
            Now look at that job requirements and specification:
            {jobOffer}
            
            tell me if I meet those job requirements"""},
            {"role": "assistant", "content": """
            preferences met: [requires .net, earnings more than 2000 usd, remote location],
            requirements met: [enough experience, main technology (.net) is known for you]
            
            Verdict: Ok, not ideal"""},
            {"role": "user", "content": f"""Now look at those preferences:
            {realPreferencesAndExperience}. 
            
            Now look at that job requirements and specification:
            {realJobOffer}
            
            tell me if I meet those job requirements, please answer in the same manner as before"""}
        ]
    )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
