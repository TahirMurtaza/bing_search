from bs4 import BeautifulSoup
import requests_async as requests
from utils.fake_user import get_fake_user_agent
import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv()

async def customsearch(searchquery):
    username = os.getenv('username')
    password = os.getenv('password')
    PROXY_RACK_DNS = os.getenv('PROXY_RACK_DNS')
    proxy = {"https":"http://{}:{}@{}".format(username, password, PROXY_RACK_DNS)}
    query='"%s" "%s" site:linkedin.com' % (searchquery['title'], searchquery['company'])
    safe_querystring = urllib.parse.quote_plus(query)
    url = 'https://www.bing.com/search?q='+safe_querystring
    headers = {'User-Agent': get_fake_user_agent()}
    response = await requests.get(url, proxies=proxy, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    search_results= soup.find_all('li', {'class': 'b_algo'})
    res = {}
    res["totalResults"] = len(search_results)
    res["items"] = search_results
    return res