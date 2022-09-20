from pprint import pprint

from django.shortcuts import render
from newsapi import NewsApiClient
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os
import re

load_dotenv()

# Init
# newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
newsapi = NewsApiClient(api_key="37d8d403a48442a980e7daf82aaab00c")


# Create your views here.
def list_of_articles(request, source):
    topnews = newsapi.get_everything(sources=source)

    latest = topnews['articles']
    title = []
    desc = []
    url = []
    author = []
    date = []
    content = []

    for i in range(int(len(latest))):
        news = latest[i]

        title.append(news['title'])
        desc.append(news['description'])
        content.append(scrape_all_content(news['url']))
        url.append(news['url'])
        author.append(news['author'])
        date.append(news['publishedAt'])

    all_news = zip(title, desc, content, url, author, date)

    context = {
        'all_news': all_news,
        'source': source
    }

    return render(request, "news/list_of_articles.html", context)


def scrape_all_content(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "lxml")

    try:
        body_text = soup.find("article")
        return body_text.get_text()
    except AttributeError:
        body_text = soup.find("body")
        return body_text.get_text()


def news_source_index(request):
    list_of_sources = []
    sources = newsapi.get_sources()
    for i in sources['sources']:
        list_of_sources.append(i['id'])

    context = {
        'list_of_sources': list_of_sources
    }

    return render(request, 'news/news_index.html', context)