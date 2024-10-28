import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time
import requests
    
def scraper(user_message):
    # instantiate options for Chrome
    options = webdriver.ChromeOptions()

    # run the browser in headless mode
    options.add_argument("--headless=new")

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
    return links[:2]
    #close the browser
    driver.quit()

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

def get_course_info(links):
    for link in links:
        url = link
        response = requests.get(url)
        html = response.text
        #print(html)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        info = {}
        
        for k, v in CONTENT_KEYS.items():
            elements = soup.find_all(attrs={"data-bind": lambda x: x and f"courseDetail.{v}" in x})
            if len(elements) == 0:
                continue
            
            info[k] = elements[0].get_text()

        return info
    print("test")
    print(get_course_info(links))

def reply (user_message):
    links = scraper(user_message)
    get_course_info(links)