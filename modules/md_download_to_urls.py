## Downloads Markdown from a reddit page and parses links, saves to urls.md

def get(url, lw):
	import http
	import json
	import requests
	import re

	write_file = open("urls.md", "w+")

	headers = {
	    'User-Agent': 'BookOfReddit Markdown Parser'
	}

	## Get data from reddit json files
	if url.endswith('/'):
		url = url[:-1]
	actual_url = url + ".json"
	lw("Starting network connection to: " + actual_url)

	try:
		response = requests.get(actual_url, headers=headers).json()
	except json.decoder.JSONDecodeError as jde:
		lw("JSON decode error! Most likely cause: reddit servers down OR url parse error. ")
		lw(jde)
		print("Sorry, {actual_url} doesn't seem to be parseable.")
		return jde
	except Exception as e:
		lw(f"Other, non JDE exception.")
		lw(e)
		return e

	lw("Got data from specified url! Parsing data as text...")

	try:
		if response[0].get("kind") == "Listing": # Check if it's a post
			content_md = response[0].get("data").get("children")[0].get("data").get("selftext").replace("`","") # Wow this is long
		else:
			content_md = response.get("data").get("content_md").replace("`","")
	except:
		content_md = response.get("data").get("content_md").replace("`","")

	lw("Got Markdown content from reddit JSON file...")

	write_file.write(content_md)
	write_file.close()

	return 0

if __name__ == '__main__':
	get(input("Url: "))