import streamlit as st
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Job Vacancies over the years", page_icon="📈")

st.markdown("# Job vacancies")
#st.sidebar.header("Job vacancies")
st.write("""Data is extracted from https://data.gov.sg/datasets/d_a867a20fe017b3b17f61758cfbfd5767/view""")
st.write("""For info on salaries, see this Straits Times article at https://www.straitstimes.com/singapore/fresh-university-grads-get-higher-salaries-though-fewer-find-full-or-part-time-work-survey""")

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
df = pd.read_csv('./data/jobvacancies.csv')
#last_rows = np.random.randn(1, 1)
print (df)
chart= st.line_chart(df, x = "Quarter", x_label = "Quarter/Yr", y_label = "Job Vancancy Rate")

# plt.plot(x, y, label = "line 1")
# plt.plot(y, x, label = "line 2")
# plt.legend()
# plt.show()
# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")
