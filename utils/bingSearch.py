from bs4 import BeautifulSoup
import requests_async as requests
from utils.fake_user import get_fake_user_agent
import urllib.parse

async def customsearch(searchquery):
    proxy = {'https': 'http://user-lyneadmin:lyneadmin@gate.dc.smartproxy.com:20000'}
    query='"%s" "%s" site:linkedin.com' % (searchquery['title'], searchquery['company'])
    safe_querystring = urllib.parse.quote_plus(query)
    url = 'https://www.bing.com/search?q='+safe_querystring
    print(url)
    headers = {'User-Agent': get_fake_user_agent()}
    response = await requests.get(url, proxies=proxy, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    search_results= soup.find_all('li', {'class': 'b_algo'})
    res = {}
    res["totalResults"] = len(search_results)
    res["items"] = search_results
    return res