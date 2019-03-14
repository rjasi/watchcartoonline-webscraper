"""
    A tool to scrape links of video urls of all tv show episodes from
    thewatchcartoononline host for a given tv show name... i.e simpsons

    *** DOES NOT DOWNLOAD ANY VIDEO ***

    Notes:
        Performance leaves to be desired due to selenium needing to load every single page.
        Might not have a way around it.

    Tested on chrome driver: Version 69.0.3497.100 (Official Build) (64-bit)

"""

from WatchCartoonOnlineScraper import WatchCartoonOnlineScraper


def log_error(e):
    """
    Print error, in future write to some log
    """
    print ("ERROR: \n")
    print (e)
    print ("*********\n")




if __name__ == "__main__":

    scraper = WatchCartoonOnlineScraper();

    try:
        links = scraper.get_episode_links("simpsons")
    except Exception as e:
        log_error(e)
        print ("Program terminated")


    with open('links.txt', "w") as file:
        for link in links:
            file.write(link + "\n")

    scraper.kill_browser()

    print("FINISHED!")






#smydivs = soup.findAll("div", {"class": "stylelistrow"})
