import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
import matplotlib.pyplot as plt

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
    

def titles():
    title_list = []
    for page in range(1, int(final_page())+1):
        URL = f"https://www.gamesjobsdirect.com/results?page={page}&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        #find the margin where the go to last page tab is
        results = soup.find_all("a", class_="job-title")
        #This will need to be changed later so it gets stored in a database instead of printing
        for x in results:
            title_list.append(x["title"])
    return(title_list)

def job_types():
    soft_engineer = 0
    data_analyst = 0
    ui_design = 0
    video_editor = 0
    backend_dev = 0
    producer = 0
    title_list = titles()
    for x in title_list:
        if "data" in x.lower():
            data_analyst += 1
        elif "ui" in x.lower():
            ui_design += 1
    print(data_analyst)
    print(ui_design)

def programming_langs():
    import re
    python = 0
    csharp = 0
    cplus = 0
    java = 0
    sql = 0
    unity = 0
    for page in range(1, int(final_page())+1):
        URL = f"https://www.gamesjobsdirect.com/results?page={page}&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("a", class_="job-title")
        for x in results:
            URL = "https://www.gamesjobsdirect.com" + x["href"]
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            result = soup.find("div", class_="post-description")
            is_python = result.find(string=re.compile('.*{0}.*'.format("Python")))
            is_csharp = result.find(string=re.compile('.*{0}.*'.format("C#")))
            is_cplus = result.find(string=re.compile('.*{0}.*'.format("C\+\+")))
            is_java = result.find(string=re.compile('.*{0}.*'.format("Java")))
            is_sql = result.find(string=re.compile('.*{0}.*'.format("SQL")))
            is_unity = result.find(string=re.compile('.*{0}.*'.format("Unity")))
            if is_python != None:
                python += 1
            if is_csharp != None:
                csharp += 1
            if is_cplus != None:
                cplus += 1
            if is_java != None:
                java += 1
            if is_sql != None:
                sql += 1
            if is_unity != None:
                unity += 1
            
            continue
    return [python, csharp, cplus, java, sql, unity]
             
def graph():
    labels = 'Python', 'C#', "C++", "Java", "SQL", "Unity"
    sizes = programming_langs()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
            
def job_desc():
    for page in range(1, int(final_page())+1):
        URL = f"https://www.gamesjobsdirect.com/results?page={page}&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("a", class_="job-title")
        for x in results:
            URL = "https://www.gamesjobsdirect.com" + x["href"]
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")

            job_info = soup.find("div", class_="job-info-container")

            location = job_info.find("label", string="Location").parent.find("p")
            experience = job_info.find("label", string="Experience Level").parent.find("p")
            company_name = job_info.find("label", string="Company Name").parent.find("p")
            job_title = soup.find("h3", class_="margin-b-4")
            unwanted = job_title.find("span")
            if unwanted is not None:
                unwanted.extract()
            print(job_title.text.strip())

job_desc()

