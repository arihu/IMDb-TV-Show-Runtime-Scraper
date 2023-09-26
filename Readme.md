# IMDb TV Show Runtime Scraper

A webpage that will take IMDb TV Show id and return the total runtime in minutes.
The scraper works by using BeautifulSoup to gather all links relating to the show
by inserting the imdb id to a link of an episode list. The scraper will then use
Selenium to scroll down the episode page to let it load and gather the runtime
using scripts.
