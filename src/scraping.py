import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs

#We will be scraping gamesjobdirect.com


def final_page():
    """
    So that we can iterate through all the pages of a search, we need to find the final page number to use as a condition
    """
    #The initial URL of gamesjobdirect when you search leicester in a 50 mile radius
    URL = "https://www.gamesjobsdirect.com/results?page=1&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    #find the margin where the go to last page tab is
    results = soup.find_all("div", class_="margin-t-1")

    #We need to loop through the divs as there may be multiple margin-t-1
    for x in results:
        links = x.find_all("a")
        for link in links:
            link_url = link["href"]

    #parse the url to find what the final page is
    url = "https://www.gamesjobsdirect.com" + link_url
    parsed_url = urlparse(url)
    last_page = parse_qs(parsed_url.query)['page'][0]

    return last_page
    

def scraping():
    for page in range(1, int(final_page())+1):
        URL = f"https://www.gamesjobsdirect.com/results?page={page}&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        #find the margin where the go to last page tab is
        results = soup.find_all("a", class_="job-title")
        #This will need to be changed later so it gets stored in a database instead of printing
        for x in results:
            print(x["title"])
        
        
