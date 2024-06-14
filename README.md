ESA SME scraper and analyzer to find jobs at ESA contractors more easily :) <3

Data Source
-----------

ESA publishes their SME (Small and Medium Enterprises) contractors here: https://esastar-emr.sso.esa.int/PublicEntityDir/PublicEntityDirSme

The large contractors are the well-known enterprises like Airbus, Thales, Terma, Leonardo, Telespazio, RHEA Group, etc.

Installation
------------

First install python requirements from requirements.txt:
`pip install -r requirements.txt`

Create python environment:
`python -m venv ESASMEscraper`

Activating the python environment:
`source ./ESASMEscraper/bin/activate`

And then you gotta install some OpenAI-compatible AI somewhere. I had mine running on a separate desktop using Jan.ai and using the Llama 3 8B Instruct. I don't know which models are good and what they're good at, I just picked what seemed reasonable based on google search.

How this project is supposed to work
------------------------------------

The pipeline used in this project:
- Step 1a: Using Selenium, collect all rows in ESA's SME database (https://esastar-emr.sso.esa.int/PublicEntityDir/PublicEntityDirSme). No processing, simply gathering rows in the HTML documents. Output is an ill-formatted HTML. We don't need proper <head> or <body> tags.
- Step 1b: Take all the rows from Step 1a and collect company details by simply doing a GET request and parsing info. Transform everything into a JSON dictionary. This is the main output, already useful.
Then for each entry in the JSON dict, i.e. for each company, perform steps 2-4:
	- Step 2: if company has a webpage link, download the webpage using Selenium (to deal with Javascript) and extract content and links using Trafilatura
	- Step 3: pass the content to an AI and ask it to provide a list of tags describing what the company does and also whether there's a career page link
		- optionally, if we have the link, we could also follow it and ask AI to check what open positions there are. But we're not going to do this.
	- Step 4: collect all tags into a JSON array and append that to the JSON dict from Step 1b.

- Step 5 (Not yet implemented): After all companies are processed, collect all tags into one big JSON array. Give that array to an AI and ask it to reduce redundancy by removing same and similar tags. Ask the AI to also provide the replacements, i.e. if tag A supersedes (contains, replaces) tag B, then we want to document a transformation like "B -> A".
- Step 6 (Not yet implemented): Go through the big JSON dict with original tags and for each company apply the transformations. Make sure the list of tags is a set, not a multiset.


- Step 7: profit, lmao. You can search for the keywords you're interested in, like "software", or "materials", and find those in the JSON files, thus finding companies that do those things. So far, unfortunately, the quality of the result is not great. I need to use a bigger model, but I don't have the GPU(s) for that.

Usage
-----

Well, you can skip steps 1a and 1b, because those things are unlikely to change much soon. If anything, ESA should remove some of those entries, as some of the URLs just get redirected to stuff that's probably unrelated or they just return an error. Some entries also simply don't have a URL at all. Anyway, those first two scripts (the steps are in the file names) print to stdout, so you should redirect stdout to a file.

I won't provide instructions on how to run the AI, that's up to you to figure out, there are howtos online.

Configuration on accessing the AI are in the `Steps-2-3-4-company_analyzer.py` script. Just have a look there.

Code quality
------------

In this case I really don't care. I care about the quality of output, which is currently quite lacking. I'd welcome suggestions on that part.

Results
-------

Rather poor in a lot of cases, I'd say. It seems that I need a bigger model that's better at outputting just tags and not whole sentences at times. It should also handle bad websites better. But results may also depend on the quality of trafilatura's output.


Other (probably better) places where you can search for jobs in the european space industry are here:
https://spacecrew.com/
https://spaceindividuals.com/
https://www.space-careers.com/


Feel free to suggest more data sources, companies, suggestions, or strategies how to find jobs! :)

