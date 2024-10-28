import streamlit as st

st.title ("Project Scope")
st.html("<p style='padding-top:15px'> </p>")
st.text("""       
        Create a simple chat that summarises course details from Skillsfuture and shows\n
        location of course providers. \n
        Data sources are from Skillsfuture website, data.gov.sg and the internet.\n
          """)
st.html("<p style='padding-top:15px'> </p>")
filepath = './data/piggy.jpg'
st.image(filepath, caption="Ms Piggy is here to help you")