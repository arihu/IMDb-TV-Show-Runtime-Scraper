import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def scrape_imdb(imdb_id):
    # Get list of episodes given imdb id
    url = f"https://m.imdb.com/search/title/?series={imdb_id}&view=simple&count=250&sort=user_rating,desc&ref_=tt_eps_rhs_sm"
    episodelist = requests.get(url)
    episodelist_soup = BeautifulSoup(episodelist.text, "html.parser")
    ###Headless mode
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    ##Debug
    print("\nurl: " + url)

    # Each episode block is inside div of class lister-item mode-simple
    episode_durations = []
    episodes = episodelist_soup.find_all("div", class_="lister-item mode-simple")
    if len(episodes) == 0:
        print("Not a TV show or Invalid ID")
        return []

    for episode in episodes:
        link_elements = episode.find_all("a")
        # Each episode block has ~14 links, Episode page is the 1st link(0th index)
        if len(link_elements) != 0:
            episode_link = link_elements[0]
            episode_url_path = episode_link["href"]
            episode_url = f"https://m.imdb.com{episode_url_path}"

            ##Debug
            print("\nepisode url: " + episode_url)

            driver.get(episode_url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # runtime is found in li tag of data-testid="title-techspec-runtime", in the child div element
            # in form x minutes or x minutes y hours
            # ex:
            # <li role="presentation" class="ipc-metadata-list__item" data-testid="title-techspec_runtime">
            #   <span class="ipc-metadata-list-item__label" aria-disabled="false">Runtime</span>
            #   <div class="ipc-metadata-list-item__content-container">1<!-- --> <!-- -->hour<!-- --> <!-- -->28<!-- --> <!-- -->minutes</div>
            # </li>
            try:
                runtime_text = driver.execute_script(
                    "return document.querySelector('li[data-testid=\"title-techspec_runtime\"] div').textContent;"
                )
                print("runtime text: " + runtime_text)
                duration_minutes = parse_duration(runtime_text)
                print("runtime in minutes: " + str(duration_minutes))
                episode_durations.append(duration_minutes)
            except Exception as e:
                print(
                    "episode url has no runtime, episode not released, or misc. error"
                )
                print("Error:", str(e))
                continue

    driver.quit()
    return episode_durations


def parse_duration(duration_str):
    words = duration_str.split()
    hours = 0
    minutes = 0
    i = 0
    while i < len(words):
        word = words[i].lower()
        if word.isdigit():
            if i + 1 < len(words) and words[i + 1].lower() in ["hour", "hours"]:
                hours = int(word)
                i += 1
            elif i + 1 < len(words) and words[i + 1].lower() in ["minute", "minutes"]:
                minutes = int(word)
                i += 1
            else:
                minutes = int(word)
        elif word == "hour" or word == "hours":
            hours = 1
        elif word == "minute" or word == "minutes":
            minutes = 1
        i += 1
    # Calculate the total duration in minutes
    total_minutes = hours * 60 + minutes
    return total_minutes
