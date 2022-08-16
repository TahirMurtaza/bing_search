
from flask import request, jsonify,Flask
import json
import requests
from bs4 import BeautifulSoup
import urllib.parse
from utils import parse,bingSearch
import re




app = Flask(__name__)


@app.route('/api/v1/customsearch', methods=('POST',))
async def customsearch():
    try:
       
        searchquery = request.get_json()
        result = {'people':[]}
        result['people'] = []
        res = await bingSearch.customsearch(searchquery)
        # print("response",res)
        # get total API results
        total_results = res['totalResults']
        title = searchquery['title']
        company = searchquery['company']
        
        # check if results are found
        if int(total_results) > 0:
            for item in res['items']:
                person = {}
                
                h2_tag=item.find('h2')
                link_tag=h2_tag.find('a')
                
                extract_title = h2_tag.getText()
                print(extract_title)
                # if title and company has exact match
                if re.search(title,extract_title) and re.search(company,extract_title):
                    
                    description = item.find('p').getText()
                    
                    person["month_started"],person['year_started'] = parse.extract_date_started(description)
                    # compare present date and after date
                    if parse.compare_dates(searchquery['after_date'], person["month_started"],person['year_started']):
                        full_name = parse.extract_human_names(extract_title)
                        person['full_name'] = full_name
                        person['linkedin_url'] = link_tag.get('href')
                        person['title'],person['company_name'] = parse.extract_title_company(extract_title)
                        result['people'].append(person)
        
        return jsonify(result),201
    except Exception as e:
        return jsonify({'error':str(e)}),401


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}


def job_list_url(company_name,title,company_website):
    
    proxy = {'https': 'http://user-lyneadmin:lyneadmin@gate.dc.smartproxy.com:20000'}
    safe_querystring = urllib.parse.quote_plus(f'"${title}" "${company_name}" site:linkedin.com')
    
    url = 'https://www.bing.com/search?q='+safe_querystring
    headers = {'User-Agent': get_fake_user_agent()}
    response = requests.get(url, proxies=proxy, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')
    search_results=soup.find_all('li', class_='b_algo')
    result_url=[]
    # result_title=[]
    for result in search_results:
                h2_tag=result.find('h2')
                link_tag=h2_tag.find('a')
                extract_title = h2_tag.getText()
                description = result.find('p').getText()
                # title=link_tag.text
                # if("Indeed" in title or "Glassdoor" in title):
                #     continue
                url=link_tag.get('href')
                # caption = result.find('div', class_='b_caption')
                # description = caption.find('p')
                result_url.append(url)
    return(result_url)




#job_list_url("Account Executive","Fivetran","fivetran.com")