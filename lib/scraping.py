import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
from concurrent.futures import ProcessPoolExecutor

import time


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
        self.url = 'https://www.gamesjobsdirect.com/results?page={}&stack=0&mt=2&ic=False&l=Leicester&lid=2644668&lat=52.638599395752&lon=-1.13169002532959&r=50&age=0&sper=4'

    def main(self):
        """ Creates threads and gives them a different page to scrape through.
        """
        # print('GamesJobDirectScraper.main()')
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
        self.url = 'https://jobs.gamesindustry.biz/jobs?search=&job_geo_location=Leicester%2C%20UK&radius=50&Find_Jobs=Find%20Jobs&lat=52.6368778&lon=-1.1397592&country=United%20Kingdom&administrative_area_level_1=England'

    def main(self):
        """ Creates threads and gives them a different page to scrape through.
        """
        # print('GameindustryBizScraper.main()')
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
            experience = 'Not specified'
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


class AardvarkSwiftScraper(Scraper):
    """ Class for scraping aswift.com
    """
    def __init__(self):
        self.url = 'https://aswift.com/job-search/?page_job={}&industry=&location=united-kingdom&job_title=&cs_=Search&parent=&industry=&job_title='

    def main(self):
        """ Creates threads and gives them a different page to scrape through.
        """
        # print('AardvarkSwiftScraper.main()')
        with ProcessPoolExecutor(max_workers=10) as executor:
            for page_number in range(1, self.last_page_number() + 1):
                url = self.url.format(page_number)
                future = executor.submit(self.scrape, url)

    def last_page_number(self):
        """ Finds the number of the last page to facilitate iteration through the pages.
        """
        page = requests.get(self.url.format(1))
        soup = BeautifulSoup(page.content, "html.parser")
        return int(soup.find('ul', class_='pagination').find_all('li')[-2].getText())

    def scrape(self, url):
        """ Given the url of a page, iterates over the job offers on that page and scrapes the data.
        """
        current_offers = list()
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        offers_list = soup.find('ul', class_='jobs-listing')
        results = offers_list.find_all('li')
        for result in results:
            link = result.find('a')
            offer_page = requests.get(link['href'])
            soup = BeautifulSoup(offer_page.content, 'html.parser')

            job_title = soup.find('div', class_='rich-editor-text').find('h1').text.strip()
            employer = 'Not specified'
            employer_h2 = soup.find('div', class_='rich-editor-text').find('h2')
            if employer_h2 is not None and employer_h2.text.strip():
                employer = employer_h2.text.split('–')[0].strip()
            location = soup.find('ul', class_='post-options').find('i', class_='icon-location6').parent.find('a').text.strip()
            experience = 'Not specified'
            job_description = soup.find('div', class_='rich-editor-text')
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


class AmiqusScraper(Scraper):
    """ Class for scraping www.amiqus.com
    """
    def __init__(self):
        self.url = 'https://www.amiqus.com/jobs?q=&options=,20878,20877&page={}&size=12'
        self.offer_url = 'https://www.amiqus.com{}'
        self.headers = {  # if we don't include headers the website detects that we are not a human
            'Host': 'www.amiqus.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1'
        }

    def main(self):
        """ Creates threads and gives them a different page to scrape through.
        """
        # print('AmiqusScraper.main()')
        with ProcessPoolExecutor(max_workers=10) as executor:
            for page_number in range(1, self.last_page_number()+1):
                url = self.url.format(page_number)
                future = executor.submit(self.scrape, url)

    def last_page_number(self):
        """ Finds the number of the last page to facilitate iteration through the pages.
        """
        url = self.url.format(1)
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.content, "html.parser")
        return int(soup.find('div', class_='attrax-pagination__pagination').find_all('li')[-3].getText())

    def scrape(self, url):
        """ Given the url of a page, iterates over the job offers on that page and scrapes the data.
        """
        current_offers = list()
        page = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', class_='attrax-vacancy-tile')
        for result in results:
            link = result.find('a', class_='attrax-vacancy-tile__title')
            offer_page = requests.get(self.offer_url.format(link['href']), headers=self.headers)
            soup = BeautifulSoup(offer_page.content, 'html.parser')

            job_title = soup.find('span', class_='header__text').text.split('-')[0].strip()
            employer = 'Not specified'
            location = soup.find('li', class_='Location-wrapper')
            unwanted_label = location.find("label")
            if unwanted_label is not None:
                unwanted_label.extract()
            experience = 'Not specified'
            job_description = soup.find('div', class_='description-widget')
            requirements = self.parse_requirements(job_description)
            offer = Offer(
                title=job_title,
                employer=employer,
                location=location.text.strip(),
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

