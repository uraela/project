import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from helper_functions import llm

import time
import requests
    
def scraper(user_message):
    # instantiate options for Chrome
    options = webdriver.ChromeOptions()

    # run the browser in headless mode
    #options.add_argument("--headless=new")

    # instantiate Chrome WebDriver with options
    driver = webdriver.Chrome(options=options)

    # open the specified URL in the browser
    url = 'https://www.myskillsfuture.gov.sg/content/portal/en/portal-search/portal-search.html'
    driver.get(url)
    #assert 'Skillsfuture' in driver.title
    
    #elem = driver.find_element(By.XPATH("//input[@id='global-search-page-searchbar']"))# Find the search box
    elem = driver.find_element(By.ID,'global-search-page-searchbar')  
    elem.send_keys(user_message + Keys.RETURN)

    url = driver.current_url+"&sort=Course_Quality_Stars_Rating%20desc%2CCourse_SEO_Name%20asc" 
    driver.get(url)
    delay = 3 # seconds
    #print (driver.current_url)
    try:
         myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME,('card-title'))))
         print ("Page is ready!")
    except TimeoutException:
         print ("Loading took too much time!")
    
    links = []
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    for elem in elems:
        if "https://www.myskillsfuture.gov.sg/content/portal/en/training-exchange/course-directory/course-detail.html?" in elem.get_attribute("href"):
            links.append(elem.get_attribute("href"))
    #print (links)
    return links[:3]
    #close the browser
    driver.quit()


def load_html(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if you don't need to see the browser
    driver = webdriver.Chrome(options=chrome_options)

    html_raw = None
    
    try:
        driver.get(url)
        time.sleep(5)
        html_raw = driver.page_source
    finally:
        driver.quit()
    
    return html_raw


CONTENT_KEYS = {
    "title": "courseTitle",
    "price": "totalCostOfTraining",
    "provider": "trainingProvider",
    "attendee_count": "courseAttendeeCount",
    "objective": "courseObjective",
    "content": "courseContent",
    "job_roles": "relevantJobRoles",
    "training_duration": "totalTrainingDurationHour",
}

def get_course_info(urls):
    infos = []
    for url in urls:
        html_raw = load_html(url)

        soup = bs4.BeautifulSoup(html_raw, 'html.parser')
        info = {}
        for k, v in CONTENT_KEYS.items():
            elements = soup.find_all(attrs={"data-bind": lambda x: x and f"courseDetail.{v}" in x})
            if len(elements) == 0:
                continue
            
            info[k] = elements[0].get_text()
        infos.append(info) 

    return infos
        
#url = "https://www.myskillsfuture.gov.sg/content/portal/en/training-exchange/course-directory/course-detail.html?courseReferenceNumber=TGS-2020500290"
#info = get_course_info(url)
#print(info)

def generate_response(info):

    delimiter = "####"

    system_message = f"""
    You are Ms Piggy and very ethusiastic about life. Say something uplifting in 5 words.

    Step 1:{delimiter} All available courses are shown in the dictionary array below:
    {info}

    Step 2:{delimiter} Summarise information about the courses. \
    You must only rely on the facts or information in the dictionary array.\

    Step 3:{delimiter}: Answer the customer in a encouraging tone.\
    Make sure the statements are factually accurate and concise.\
    Complete with details such as title, provider, price and skills to be learnt.\
    Use Neural Linguistic Programming to construct your response.

    {delimiter}Step 4:{delimiter}: Provide the map coordinates of all the different course providers.\
    Coordinates should all be different. Coordinates elements should be separated by comma only like this: a, b, c, d, e, f, g \

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to customer>
    {delimiter}Step 4:{delimiter} <step 4 rxtract coordinates>

    Make sure to include {delimiter} to separate every step.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        # {'role':'user',
        #  'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_by_messages(messages)  
    coord = response_to_customer.split(delimiter)[-1] 
    response_to_customer= response_to_customer.split(delimiter)[-3]  
    print ("coord:" + coord)
    return response_to_customer, coord   

def reply (user_message):
    links = scraper(user_message)
    info = get_course_info(links)
    reply =  generate_response(info)
    return reply