import requests
from bs4 import BeautifulSoup

PAGE_URL = "http://www.formula1.com/en/drivers.html"

class Drivers:
    def __init__(self):
        self.__cache_drivers__()

    def __cache_drivers__(self):
        self.page = requests.get(PAGE_URL)
        self.bs = BeautifulSoup(self.page.content, "html.parser")

        # get the container that holds all of the driver information
        div = self.bs.find("div", {"class": "container listing-items--wrapper driver pre-season"})

        # get all the a tags that hold the driver links
        a_tags = div.find_all("a", {"class": "listing-item--link"})

        # create a dictionary to hold the driver data
        driver_list = {}

        # iterate through the a tags
        for a_tag in a_tags:
            # get the driver name
            tag = a_tag.find("div", {"class": "col-xs-8 listing-item--name f1-uppercase"})
            name = [ ]
            if tag is not None:
                for span in tag.find_all("span"):
                    name.append(span.text)

            # get the driver's stats
            driver_page = requests.get(PAGE_URL[0:23] + a_tag["href"])
            ds = BeautifulSoup(driver_page.content, "html.parser")
            stats = ds.find("table", {"class": "stat-list"}).find("tbody").find_all("tr")

            # add the driver and stats to the driver list
            driver_list[' '.join(name)] = {}
            for stat in stats:
                driver_list[' '.join(name)][stat.find("th").text] = stat.find("td").text

        self.drivers = driver_list

    def get_drivers(self):
        return self.drivers
