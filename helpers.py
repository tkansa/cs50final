import feedparser
import urllib.parse

from flask import redirect, render_template, request, session, url_for
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def lookup(category):
    """Looks up articles for category."""

    # check cache for category
    #if category in lookup.cache:
    #    return lookup.cache[category]

    # get feed from NYTimes
    feed = feedparser.parse("http://rss.nytimes.com/services/xml/rss/nyt/{}.xml".format(urllib.parse.quote(category, safe="")))

    # if no items in feed, get feed from Onion
    if not feed["items"]:
        feed = feedparser.parse("http://www.theonion.com/feeds/rss")

    # cache results
    lookup.cache[category] = [{"link": item["link"], "title": item["title"], "description": item["description"]} for item in feed["items"]]

    # return results
    return lookup.cache[category]

# initialize cache
lookup.cache = {}
