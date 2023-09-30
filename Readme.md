# IMDb TV Show Runtime Scraper

A webpage that will take a given IMDb TV Show id and return the total runtime in minutes as given in each episode's runtime description with BeautifulSoup and Selenium.

## Why?

Almost all online sites that calculate the runtime of a show uses the formula `# of episodes * Average runtime of all episodes`. This can lead to inaccurate results especially for shows with varying runtimes for each episode(more common because of streaming).

## How does it work?

Submitting the form with an IMDb TV id calls the scrape_imdb function. This will open a new chrome tab that will traverse each episode one by one, keeping track of the duration. After scraping, a result page will be rendered with duration data.

Here is how the scrape_imdb work:

**1) Retrieve the HTML of the Episode List**

We first post the IMDb id to this episode list template:

```python
url = f"https://m.imdb.com/search/title/?series={imdb_id}&view=simple&count=250&sort=user_rating,desc&ref_=tt_eps_rhs_sm"
```

This episode list shows the 250 of the most top rated episodes of the given TV show ID. This episode list is also queried using advanced search, features no ads, and is loaded statically, which allows the HTML to be parsed with BeautifulSoap.

```python
episodelist = requests.get(url)
episodelist_soup = BeautifulSoup(episodelist.text, "html.parser")
```

We can now access the episode list and access every episode on the list by using BeautifulSoup's find_all method

**2) Add Selenium Drivers to load webpage Dynamically**

Contrast to the episode list that is loaded statically, each episode page is loaded dynamically. This requires the scraper to use Selenium to manually scroll down the webpage to load everything. The driver also adds the extension [uBlock Origins](https://ublockorigin.com/) (v1.52.2) in the static folder to help load the webpage faster

Initializing the Scraper:

```python
options = Options()
options.add_extension("./static/uBlockOrigin.crx")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
```

**3) Traverse each episode and gather data**

The episode link gathered in each episode block in the episode list is surrounded by a div of class "lister-item mode-simple." Each episode url is then iterated to the Selenium driver. The Selenium driver scrolls down the webpage to dynamically load the webpage and another BeautifulSoup soup is used to find the running time.

The runtime data of each episode page is found in a div element within a li of data-testid "title-techspec-runtime." The runtime gathered is either in form x minute(s), x hour(s), or x hour(s) y minute(s). The runtime text is parsed into an integer representation of the number and added to a list episode_durations.

After all episodes are iterated, the webpage updates with the episode_duration list, the episode_duration length(episodes processed), and episode_duration sum(total duration).

## Problems

- Selenium "--headless=new" mode does not work
- TV shows with more than 250 episodes only show runtime for 250 episodes

## How to Run

You will need flask, beautifulsoup4, and selenium. After running app.py, go to any address that the Flask project is running.
