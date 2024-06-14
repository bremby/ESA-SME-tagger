#!/usr/bin/env python3

from trafilatura import extract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import sys
import signal

company = ""
def signal_handler(sig, frame):
    print('\nLast company to start processing: ' + company)
    json.dump(tagged_companies, out_file, indent=4)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if len(sys.argv) < 2:
    print("source file argument is missing")
    exit(1)

with open(sys.argv[1]) as f:
    companies = json.load(f)

jan_server = "http://192.168.1.134:1337/v1/chat/completions"
header = "Content-Type: application/json"
model = "llama3-8b-instruct"
# model = "mistral-ins-7b-q4"
instructions = "You receive text content from a company website in any language. Respond with strictly only a list of tags in English, " \
"that would describe the company, as comma-separated values. No special characters, no prefix, no intro, no duplicates, no quotes. "
# I found that shorter instructions work better. The original extensions are here:
# "Do not return anything else. Remove duplicates. Do not prefix the list of tags with anything, not even a sentence. " \
# "Do not quote the tags."
system_role = {"role" : "system", "content": instructions}
user_role = {"role": "user"}
stop = "<|eot_id|>"

pagination = 100

driver = webdriver.Firefox()

page = 0
i = 0
tagged_companies = {}
for company in companies:
	print('Processing company: ' + company, file=sys.stderr)
	if companies[company]["EntityWebSite"] == "":
		print("Company is missing URL:" + companies[company]["Name"])
		continue
	
	url = companies[company]["EntityWebSite"]

	# Use selenium to fetch the company website; We use selenium to handle javascript-based webpages
	try:
		driver.get(url)
		wait = WebDriverWait(driver, timeout=1)
		wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
	except Exception as e:
		print(e)
		continue
	
	
	# print("page ready")

	# Use trafilatura to extract useful content
	content = extract(driver.page_source, include_links=True, url=url)

	# content = "At SBQuantum we aim to “Reveal the Invisible”, be that underground, underwater or concealed by the environment. Our team is using magnetic intelligence to build a precise, localised magnetic model of the earth that will allow us to better understand and navigate through our environment. To do so, we are introducing a novel quantum magnetometer that unlocks greater specificity in its measurement of magnetic resonance lines. This powers a custom dashboard that allows our clients to inspect, explore and navigate based on information that is currently hidden fluctuations of the Earth’s magnetic field."
	# content += stop
	json_request_payload = {"model": model}
	user_role["content"] = content
	json_request_payload["messages"] = [system_role, user_role]
	json_request_payload["temperature"] = 0.7
	json_request_payload["max_tokens"] = 65536
	# json_request_payload["stop"] = stop

	# print("Request:")
	# print(json.dumps(json_request_payload))

	try:
		resp = requests.post(jan_server, json=json_request_payload)
	except Exception as e:
		print(e)
		continue

	# print("\nResponse:")
	resp_data_str = json.loads(resp.text)["choices"][0]["message"]["content"].strip("<|eot_id|>").replace(", ", ",")
	# print(resp_data_str)
	tags = resp_data_str.lower().split(",")
	# print(tags)

	tagged_companies[company] = companies[company]
	tagged_companies[company]["tags"] = list(set(tags)) # remove duplicates

	i += 1
	if i == pagination:
		with open("SMEs-tagged-page" + str(page) + ".json", 'w') as out_file:
			print("dumping to " + str(out_file.name))
			json.dump(tagged_companies, out_file, indent=4)
		page += 1
		i = 0
		tagged_companies = {}

with open("SMEs-tagged-page" + str(page) + ".json", 'w') as out_file:
	json.dump(tagged_companies, out_file, indent=4)

print("Script is done.")

