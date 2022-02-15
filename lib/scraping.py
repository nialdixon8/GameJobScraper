import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
from concurrent.futures import ProcessPoolExecutor

TECHNOLOGIES = ('Python', 'C#', 'C\+\+', 'Java', 'SQL', 'Unity')


def django_setup():
    """ Setup django - see https://stackoverflow.com/questions/34114427.
    """
    import os
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'group15.settings'
    django.setup()


django_setup()
from gameindustry.models import Offer


class Scraper(object):
    """ Parent class of all the scrapers to provide universal functions they can inherit.
    """
    def parse_requirements(self, job_description):
        """ Parses a job offer's description to determine what technologies are required by it.
        """
        requirements = ""
        for tech in TECHNOLOGIES:
            present = job_description.find(string=re.compile('.*{0}.*'.format(tech)))
            if present:
                tech = tech.replace('\\', '')
                requirements += f"{tech} "
        return requirements

    # this one is a bit sketchy because of no pages
    # https://hitmarker.net/jobs?location=uk&sector=technology+quality-assurance+game-production+game-design+game-development+devops+software-engineering


class GamesJobDirectScraper(Scraper):
    """ Class for scraping www.gamesjobsdirect.com
    """
    def __init__(self):
        self.url = "https://www.gamesjobsdirect.com/results?page={}&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4"

    def main(self):
        """ Creates threads and gives them a different page to scrape through.
        """
        print('GamesJobDirectScraper.main()')
        with ProcessPoolExecutor(max_workers=10) as executor:
            for page_number in range(1, self.last_page_number() + 1):
                url = self.url.format(page_number)
                future = executor.submit(self.scrape, url)

    def last_page_number(self):
        """ Finds the number of the last page to facilitate iteration through the pages.
        """
        page = requests.get(self.url.format(1))
        soup = BeautifulSoup(page.content, "html.parser")
        # find the margin where the "go to last page" tab is
        results = soup.find_all("div", class_="margin-t-1")
        # loop through the divs as there may be multiple margin-t-1
        link_url = None
        for result in results:
            links = result.find_all("a")
            for link in links:
                link_url = link["href"]
        # parse the url to find what the final page is
        if link_url is None:
            print("GamesJobDirectScraper(): COULD NOT FIND LAST PAGE URL")
            raise(RuntimeError('no last page url; results: {}'.format(results)))
        parsed_url = urlparse("https://www.gamesjobsdirect.com" + link_url)
        return int(parse_qs(parsed_url.query)['page'][0])

    def scrape(self, url):
        """ Given the url of a page, iterates over the job offers on that page and scrapes the data.
        """
        current_offers = list()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("a", class_="job-title")
        for result in results:
            offer_page = requests.get("https://www.gamesjobsdirect.com" + result["href"])
            soup = BeautifulSoup(offer_page.content, "html.parser")

            job_info = soup.find("div", class_="job-info-container")
            job_title = soup.find("h3", class_="margin-b-4")
            unwanted_span = job_title.find("span")
            if unwanted_span is not None:
                unwanted_span.extract()
            employer = job_info.find("label", string="Company Name").parent.find("p").text.strip()
            location = job_info.find("label", string="Location").parent.find("p").text.strip()
            experience = job_info.find("label", string="Experience Level").parent.find("p").text.strip()
            job_description = soup.find("div", class_="post-description")
            requirements = self.parse_requirements(job_description)
            offer = Offer(
                title=job_title.text.strip(),
                employer=employer,
                location=location,
                experience=experience,
                requirements=requirements
            )
            current_offers.append(offer)
        Offer.objects.bulk_create(current_offers)


class GameindustryBizScraper(Scraper):
    """ Class for scraping jobs.gamesindustry.biz
    """
    def __init__(self):
        self.url = "https://jobs.gamesindustry.biz/jobs?search=&job_geo_location=Leicester%2C%20UK&radius=50&Find_Jobs=Find%20Jobs&lat=52.6368778&lon=-1.1397592&country=United%20Kingdom&administrative_area_level_1=England"

    def main(self):
        """ Creates threads and gives them a different page to scrape through.
        """
        print('GameindustryBizScraper.main()')
        with ProcessPoolExecutor(max_workers=10) as executor:
            for page_number in range(1, self.last_page_number()):
                url = self.url
                if page_number > 1:
                    url = self.url + "&page={}".format(page_number)
                future = executor.submit(self.scrape, url)

    def last_page_number(self):
        """ Finds the number of the last page to facilitate iteration through the pages.
        """
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        return int(soup.find('ul', class_='pager').find_all('li')[-2].getText())

    def scrape(self, url):
        """ Given the url of a page, iterates over the job offers on that page and scrapes the data.
        """
        current_offers = list()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', class_='job__logo')
        for result in results:
            link = result.find('a', class_='recruiter-job-link')
            offer_page = requests.get(link['href'])
            soup = BeautifulSoup(offer_page.content, 'html.parser')

            job_title = soup.find('div', class_='panel-col').find('div', class_='pane-node-title').find('h2').text.strip()
            employer = soup.find('div', class_='pane-node-recruiter-company-profile-job-organization').find('a').text.strip()
            location = soup.find('div', class_='field--name-field-job-region').find('div', class_='field__items').find_all('div')[0].text.strip()
            experince_div = soup.find('div', class_='field--name-field-job-experience-term')
            experience = 'Unknown'
            if experince_div is not None:
                experience = experince_div.find('div', class_='field__items').find_all('div')[0].text.strip()
            job_description = soup.find('div', class_='field--type-text-with-summary')
            requirements = self.parse_requirements(job_description)
            offer = Offer(
                title=job_title,
                employer=employer,
                location=location,
                experience=experience,
                requirements=requirements
            )
            current_offers.append(offer)
        Offer.objects.bulk_create(current_offers)


# TODO: clean this up before merge!
# def threads():
#     URLs = []
#     for page in range(1, int(final_page()) + 1):
#         URLs.append(f"https://www.gamesjobsdirect.com/results?page={page}&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4")
#
#     with ProcessPoolExecutor(max_workers=10) as executor:
#         futures = [executor.submit(parse, url) for url in URLs]
#         print(futures)

