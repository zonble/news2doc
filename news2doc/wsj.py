#!/usr/bin/env python
# encoding: utf-8

import urllib
import urllib2
import datetime
import xml.etree.ElementTree as ET
import re

class WSJ:
	# RSS = [
	# 	'http://cn.wsj.com/big5/rss02.xml', # 特寫
	# 	'http://cn.wsj.com/big5/rssbch.xml', # 中港台
	# 	'http://cn.wsj.com/big5/rssglobal.xml', # 國際財經
	# 	'http://cn.wsj.com/big5/RSSFeedLuxury.xml', # 奢華人生
	# 	'http://cn.wsj.com/big5/rsschinastock.xml', # 中國股市
	# 	'http://cn.wsj.com/big5/rssHKstock.xml', # 香港股市
	# 	'http://cn.wsj.com/big5/rssmarkets.xml', # 全球金融市場
	# 	'http://cn.wsj.com/big5/rsstech.xml', # 科技
	# 	'http://cn.wsj.com/big5/rssautoene.xml', # 能源與汽車
	# ]

	RSS = ['http://cn.wsj.com/big5/rss02.xml']

	def _fetch_articles_in_24hours(self, url):
		print url
		now = datetime.datetime.now()
		yesterday = now - datetime.timedelta(days=1)
		articles = []
		response = urllib2.urlopen(url).read()
		response = response.decode('big5').encode('utf-8')
		parser = ET.XMLParser(encoding='utf-8')
		xml = ET.fromstring(response, parser=parser)

		for child in xml.iter('{http://purl.org/rss/1.0/}item'):
			find = lambda x: child.\
				   findall('{http://purl.org/rss/1.0/}' + x)[0].text
			publish_date_txt = find('pubDate').replace(' +0800', '')
			publish_date = datetime.datetime.\
						   strptime(publish_date_txt, "%Y/%m/%d %H:%M:%S")
			if publish_date > yesterday:
				article = {'link':find('link'),
						   'title':find('title'),
						   'publish_date':publish_date}
				articles.append(article)
		return articles

	def fetch_article(self, url):
		def format_text(text):
			text = text.replace('<br>', '\n')
			text = re.sub('<[^<]+?>', '', text)
			return text

		assert url
		response = urllib2.urlopen(url).read()
		response = response.decode('big5', 'ignore').encode('utf-8')
		pattern = r'<!content_tag txt>(.*)<!/content_tag txt>'
		content = re.findall(pattern, response, re.MULTILINE)
		if len(content) < 0:
			return
		text = content[0]
		text = format_text(text).split('\n')
		return text

	def fetch_all_articles_in_24hours(self):
		all_articles = []
		for url in WSJ.RSS:
			articles = self._fetch_articles_in_24hours(url)
			all_articles += articles
		for article in all_articles:
			link = article['link']
			print link
			text = self.fetch_article(link)
			article['text'] = text
		return all_articles
