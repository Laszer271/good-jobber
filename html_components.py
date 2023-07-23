# JOB_OFFER = '''
# <div onclick="window.open('{url}','mywindow');" onmouseover="this.style.backgroundColor='#f7f7f7'"
# style="position: relative;
#               padding: 20px;
#               border: 2px solid #ddd;
#               border-radius: 10px;
#               background-color: #fff;
#               transition: background-color 0.3s ease;
#               cursor: pointer;
#               font-family: Arial, sans-serif;
#               width: 300px; /* Set width as per your requirement */" 
#        onmouseout="this.style.backgroundColor='#fff'">
#     <h2 style="font-size: 18px; font-weight: bold; margin: 0;">{title}</h2>
#     <p style="font-size: 14px; margin: 5px 0 0 0;">{company}</p>
#     <!-- Hidden URL for the offer -->
#   </div>
# '''


# div_style = "padding: 20px; border: 2px solid #ddd; border-radius: 10px; background-color: #fff; font-family: Arial, sans-serif; width: 300px;"
# title_style = "font-size: 18px; font-weight: bold; margin: 0;"
# company_style = "font-size: 14px; margin: 5px 0 0 0;"

# # Generate the div HTML code with embedded CSS
# div_html = """
# <div style="{div_style}">
#     <h2 style="{title_style}">{title}</h2>
#     <p style="{company_style}">{company}</p>
# </div>
# """.format(
#     div_style=div_style, title_style=title_style, company_style=company_style,
#     title="{title}", company="{company}"
#     )
    

# JOB_OFFER = """
# <a href="{url}" target="_blank">{div_html}</a>
# """.format(url="{url}", div_html=div_html)

link_style = "text-decoration: none; color: inherit; cursor: pointer;"
div_style = "padding: 20px; border: 2px solid #ddd; border-radius: 10px; background-color: #fff; font-family: Arial, sans-serif; width: calc(100% - 40px);"
# title_style = "font-size: 18px; font-weight: bold; margin: 0;"
# company_style = "font-size: 14px; margin: 5px 0 0 0;"
title_style = "font-size: 18px; font-weight: bold; margin: 0; color: #333; text-decoration: none;"
company_style = "font-size: 14px; margin: 5px 0 0 0; color: #666; text-decoration: none;"

# Define CSS styles for the default and hover state
DEFAULT_STYLE = f"""
<style>
    .job-offer-link {{
        {link_style}
    }}
    .job-offer-link:hover {{
        text-decoration: none; /* Remove underline on hover */
    }}
    .job-offer-div {{
        {div_style}
    }}
    .job-offer-title {{
        {title_style}
    }}
    .job-offer-company {{
        {company_style}
    }}
    .job-offer-div:hover {{
        background-color: #f7f7f7;
    }}
    .job-offer-div a {{
        text-decoration: none;
    }}
</style>
"""

# Generate the div HTML code with embedded CSS and URL
div_html = """
<div class="job-offer-div">
    <h2 class="job-offer-title">{title}</h2>
    <p class="job-offer-company">{company}</p>
    <p class="job-offer-company">{description}</p>
</div>
"""

# Create a hyperlink around the job offer div to open the URL in a new window
hyperlink_html = '<a href="{url}" target="_blank" class="job-offer-link">{div_html}</a>'.format(url="{url}", div_html=div_html)

JOB_OFFER = hyperlink_html
# Display the CSS and HTML code using st.markdown
# st.markdown(default_style + hyperlink_html, unsafe_allow_html=True)
# st.write(hyperlink_html, unsafe_allow_html=True)

