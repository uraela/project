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
        6.  LLM outputs summary of case details and course provider\n
        7.  Map coordinates of course provider is retrieved from json file\n
            from skillsfuture @ https://data.gov.sg/datasets?agencies=SkillsFuture+Singapore+(SSG)&page=1&resultId=d_563451336616abdf5b2c36472c2afd8b
        8.  Separately, user can check out the job vacancies trend\n
            and get some info about expected salaries from a link\n
            to Straits Times. 
        """)
