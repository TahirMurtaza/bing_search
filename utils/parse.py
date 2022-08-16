from calendar import month
from datetime import datetime
import re


# parse date format eg. 03 May 2022 1:40:14 AM
def parse_date(date):
    datetime_object = datetime.strptime(date, '%d %b %Y  %I:%M:%S %p')
    return datetime_object


def extract_human_names(title):
    if title:
        full_name = title.split(' - ')[0]
    return full_name

def extract_date_started(str):
    months = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ', 'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
    month_started = None
    year_started = None
    for mon in months:
        if str.find(mon) != -1:
            month_started = months.index(mon) + 1
            start = str.find(mon) + 4
            end = start + 4
            year = str[start:end]
            if IsInt(year):
                year_started = int(year)
                break;
            
    return month_started, year_started        

def IsInt(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def compare_dates(d1, month_started, year_started):
    if month_started and year_started:
        # format (03 May 2022 1:40:14 AM)
        d1_object = parse_date(d1)
        # format (Mar 2022)
        d2_object = datetime(month=month_started,year=year_started,day=1)
        # compare if present date is greater than after date
        if d2_object > d1_object:
            return True
    return False

def extract_title_company(text):
    title = None
    company = None
    chars = ["-","–"]
    for char in chars:
        if re.search(char,text):
            arr = text.split(char)
            if len(arr) == 3:
                title = text.split(char)[1]
                company = text.split(char)[2]
            elif len(arr) == 2:
                title = text.split(char)[1]
    
    title = title.replace('...','').lstrip().rstrip()    
    company = company.replace('...','').replace("| LinkedIn","").lstrip().rstrip()    
    return title ,company
            

