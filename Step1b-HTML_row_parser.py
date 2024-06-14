#!/usr/bin/python3

import pdb
import sys
import json
import requests
import html
from bs4 import BeautifulSoup

# Path to the local HTML file
if len(sys.argv) < 2:
    print("source file argument is missing")
    exit(1)

source_html = sys.argv[1]
# source_html = 'SMEs.html'
# source_html = 'SMEs-sample.html'
# destination_file = 'SMEs.json'

# Read the content of the file
with open(source_html, 'r', encoding='utf-8') as file:
    html_content = file.read()


def get_details(details_linkm, dict_of_attributes):
    # pdb.set_trace()
    response = requests.get("https://esastar-emr.sso.esa.int/" + details_link)
    unescaped = response.text.encode().decode('unicode-escape')
    linked_soup = BeautifulSoup(unescaped, 'html.parser')
    details_list = linked_soup.find_all('input')
    for detail in details_list:
        detail_name = detail['name']
        detail_value = detail['value']
        dict_of_attributes[detail_name] = detail_value

    return dict_of_attributes


# Parse the page content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
list_items = soup.find_all('tr', class_='grid-row')  # Adjust selector as needed

# print(list_items)

dict_of_companies = {}

for item in list_items:
    # pdb.set_trace()
    attributes = item.find_all('td', class_='grid-cell')
    dict_of_attributes = {}
    for attr in attributes:
        data_name = attr['data-name']
        if data_name == 'EntityId':
            details_link = attr.find("a")['href']
            dict_of_attributes = get_details(details_link, dict_of_attributes)
            continue
        value = attr.text.strip()
        dict_of_attributes[data_name] = value

    dict_of_companies[dict_of_attributes["Name"]] = dict_of_attributes

    
print(json.dumps(dict_of_companies, sort_keys=True, indent=4))


