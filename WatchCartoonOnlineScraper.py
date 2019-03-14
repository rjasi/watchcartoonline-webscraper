"""
    Class that contains the selenium interface to thewatchcartoononline.tv


"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Give the url for the search page
SEARCH_PAGE_URL = "https://www.thewatchcartoononline.tv/search"
SEASON_URL_PREFIX = "https://www.thewatchcartoononline.tv/anime/"


class WatchCartoonOnlineScraper:

    def __init__(self):
        print ("Initializing scaper...", end ="")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.browser = webdriver.Chrome("./chromedriver", chrome_options=self.options)
        print ("DONE")

    def open_search_page(self):
        print ("Opening search page...", end ="")
        self.browser.get(SEARCH_PAGE_URL)
        print ("DONE")

    def search_function(self, show_name):
        """
        Tells the website to search for someting

        """


        self.open_search_page()
        #catara is the search form
        search_input = self.browser.find_element_by_xpath("//input[@name='catara']")
        submit_button = self.browser.find_element_by_xpath("//input[@class='aramabutonu2 button1' and @type='submit']")

        search_input.send_keys(show_name)

        print ("Submitting search...", end ="")
        submit_button.click()
        print ("DONE")


    def get_season_list(self):
        """
        At the page with all seasons of the show, pull all links to each season

        returns a set of tuple of (title, season_link) of all links to each season
        """

        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        elem_list = soup.find_all("a", href=lambda value: value and value.startswith(SEASON_URL_PREFIX), rel="bookmark")
        season_links = {(elem.getText(), elem['href']) for elem in elem_list}

        return season_links

    def get_episode_links_from_season_link(self, season_link):
        """
        returns list of tuple (title, link) of episode from a season link
        """

        self.browser.get(season_link)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")

        elem_list = soup.find_all("a", {"class": "sonra"})

        episode_links = {(link.getText(), link['href']) for link in elem_list}

        return episode_links

    def get_episode_links(self, show_name):
        """
        Takes in a show_name i.e "simpsons" then
        returns the links to all episodes

        """

        self.search_function(show_name)

        print ("Obtaining all season links...", end ="")
        season_links = self.get_season_list()
        print ("DONE")

        links = []

        for title, season in season_links:

            print ("Obtaining episode links for season: " + title, end ="...")
            episode_links = self.get_episode_links_from_season_link(season)
            #for now ignore the link title
            links = links + [link for episode_title, link in episode_links]

            print ("DONE")

        return links

    def kill_browser(self):
        if (self.browser):
            self.browser.quit()

        self.browser = None