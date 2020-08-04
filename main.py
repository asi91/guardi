import time
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from web_crawler import Crawler, CORRUPT_LINKS, LINKS_DEPTH
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", corrupt_links=CORRUPT_LINKS, links_depth=LINKS_DEPTH)


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    crawler = Crawler()
    scheduler.add_job(func=crawler.start, trigger="date", run_date=datetime.datetime.now())
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    # Start the Flask app
    app.run(host="0.0.0.0")
