#!/usr/bin/env python
# encoding: utf-8

import urllib2, datetime, re
import utils
import xml.etree.ElementTree as ET

class NewYorkTimes:
	'A class for helping fetching news from The New York Times Chinese. '

	def fetch_all_articles_in_24hours(self):
		'''
		Fetch all articles within 24 hours from the RSS feed of The New York
		Times.
		'''

		url = 'http://cn.nytimes.com/rss/zh-hant/'
		print('Fetching RSS feed from ' + url)
		try:
			response = urllib2.urlopen(url).read()
			parser = ET.XMLParser(encoding='utf-8')
			xml = ET.fromstring(response, parser=parser)
			print('...Done')
		except Exception as e:
			print('...Failed. ' + str(e))
			return []

		yesterday = utils.yesterday()
		articles = []

		def format_text(text):
			text = text.replace('<div id=story_main_mpu></div>', '')
			text = text.replace('</p>', '\n')
			text = re.sub('<[^<]+?>', '', text)
			return text

		for child in xml.iter('item'):
			find = lambda x: child.findall(x)[0].text
			publish_date_txt = find('pubDate').replace(' +0800', '')
			publish_date = datetime.datetime.\
						   strptime(publish_date_txt, "%a, %d %b %Y %H:%M:%S")
			if publish_date > yesterday:
				text = find('description')
				text = format_text(text).split('\n')
				article = {'link': find('link'),
						   'title': find('title'),
						   'text': text,
						   'publish_date': publish_date,
						   'source': 'The New York Times Chinese'}
				articles.append(article)
		return articles
