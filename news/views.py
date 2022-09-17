from pprint import pprint

from django.shortcuts import render
from newsapi import NewsApiClient
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os

load_dotenv()

# Init
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


# Create your views here.
def index(request):
    topnews = newsapi.get_everything(q="sports")

    latest = topnews['articles']
    #pprint(topnews)
    title = []
    desc = []
    url = []
    author = []
    date = []
    content = []

    for i in range(int(len(latest)/4)):

        news = latest[i]

        title.append(news['title'])
        desc.append(news['description'])
        content.append(scrape_all_content(news['url']))
        url.append(news['url'])
        author.append(news['author'])
        date.append(news['publishedAt'])

    all_news = zip(title, desc, content, url, author, date)

    context = {
        'all_news': all_news
    }

    return render(request, "news/index.html", context)


def scrape_all_content(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    return soup.get_text()