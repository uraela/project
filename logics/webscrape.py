import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from helper_functions import llm
import ast

import time
import requests
import json

def scraper(user_message):
    # instantiate options for Chrome
    #options = webdriver.ChromeOptions()
    chrome_options = Options()

    # run the browser in headless mode
    chrome_options.add_argument("--headless=new")

    # instantiate Chrome WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
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
    schools = []
    for url in urls:
        html_raw = load_html(url)
        soup = bs4.BeautifulSoup(html_raw, 'html.parser')
        info = {}
        for k, v in CONTENT_KEYS.items():
            elements = soup.find_all(attrs={"data-bind": lambda x: x and f"courseDetail.{v}" in x})
            if len(elements) == 0:
                continue
        
            info[k] = elements[0].get_text()
            if k == 'provider':
                schools.append(info[k])
        infos.append(info) 
    print (schools)
    return infos, schools
        
#url = "https://www.myskillsfuture.gov.sg/content/portal/en/training-exchange/course-directory/course-detail.html?courseReferenceNumber=TGS-2020500290"
#info = get_course_info(url)
#print(info)

def generate_response(info):

    delimiter = "####"

    system_message = f"""
    You are Ms Piggy and very ethusiastic about life. 

    Step 1:{delimiter} All available courses are shown in the dictionary array below:
    {info}

    Step 2:{delimiter} Summarise information about the courses. Label each course as C1, C2, etc\
    You must only rely on the facts or information in the dictionary array.\

    Step 3:{delimiter}: Answer the customer in an encouraging tone. Mention course label.\
    Make sure the statements are factually accurate and concise.\
    Complete with details such as title, provider, price and skills to be learnt.\
    Use Neural Linguistic Programming to construct your response. Use the same font.\

    {delimiter}Step 4:{delimiter}: Provide the map coordinates of all course providers.\
    Be factual, different course providers have different coordinates.\
    Format should be [[a,b],[c,d],[e,f]]. Do not number or label each set of coordinates.
    
    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to customer>
    {delimiter}Step 4:{delimiter} <step 4 extract coordinates>

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
    print ("chatgpt_coord:" + coord)
    coord = ast.literal_eval(coord)  
    return response_to_customer, coord    

def dict_coord_from_json():
    # Load GeoJSON data from a file
    schools = []
    coords = []
    coord_dict = {}
    with open('./data/sch_info.geojson') as f:
        data = json.load(f)
        features = data.get('features')
        for feature in features:
            item = feature.get('properties').get('Description')
            item = item[item.find('NAME_OF_SCHOOL'):]
            item = item[item.find('<td>'):]
            item = item[4:item.find('</td>')]
            schools.append(item)
            item2 = feature.get('geometry').get('coordinates')[:2]
            coords.append(item2)
    coord_dict = dict(zip(schools, coords))     
    return coord_dict

def reply (user_message):
    coords =[]
    links = scraper(user_message)
    info, schools = get_course_info(links)
    coord_dict = dict_coord_from_json()
    reply, chatgpt_coord =  generate_response(info)
    i=0
    for school in schools:
        coord = coord_dict.get(school)
        print (f"json_coord is {coord}")
        if coord:
            coords.append([coord[0],coord[1]])
        else:
            coords.append([chatgpt_coord[i][0], chatgpt_coord[i][1]])              
            i=i+1  
            print (i)
    print(coords)
    return reply, coords