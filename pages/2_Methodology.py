import streamlit as st

st.title ("Methodology")
st.html("<p style='padding-top:15px'> </p>")
st.text("""\n
        1.  User enters field of interest in chat box in homepage\n
        2.  Scraper(user_message) is called to search relevant courses\n
            in skillsfuture, ranked by ratings\n
        3.  Scraper function outputs first 3 links to the course details\n
            pages\n
        4.  Another Scraper function is called to extract details from\n
            course details page\n
        5.  Details are provided in prompt to LLM\n
        6.  LLM outputs summary of case details and shows address of \n
            course provider on map\n
        7.  Separately, user can check out the job vacancies trend\n
            and get some info about expected salaries from a link\n
            to Straits Times. 
        """)
