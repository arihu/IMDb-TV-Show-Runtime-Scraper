from flask import Flask, render_template, request
from tvscraper import scrape_imdb
import time

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        imdb_id = request.form["imdb_id"]
        start_time = time.time()
        episode_durations = scrape_imdb(imdb_id)
        end_time = time.time()
        generation_time = end_time - start_time
        return render_template("result.html", episode_durations=episode_durations, generation_time=generation_time)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
