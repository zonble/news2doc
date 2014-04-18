#!/usr/bin/env python
# encoding: utf-8

import urllib2, datetime, re
import utils
import xml.etree.ElementTree as ET
try:
	import jianfan
except:
	pass

class FinancialTimes:
	'A class for helping fetching news from The Financial Times Chinese. '

	# RSS = ['http://www.ftchinese.com/rss/feed', #每日更新
	# 	   'http://www.ftchinese.com/rss/news', #今日焦點
	# 	   'http://www.ftchinese.com/rss/hotstoryby7day', #十大熱門文章
	# 	   'http://www.ftchinese.com/rss/column/007000005', #每日英語
	# 	   'http://www.ftchinese.com/rss/column/007000004', #第一時間解讀
	# 	   'http://www.ftchinese.com/rss/column/007000007', #遠觀中國
	# 	   'http://www.ftchinese.com/rss/column/007000002', #朝九晚五
	# 	   'http://www.ftchinese.com/rss/lifestyle', #生活時尚
	# 	   'http://www.ftchinese.com/rss/letter', #讀者有話說
	# 	   'http://www.ftchinese.com/rss/column/007000012' #馬丁沃爾夫
	# ]
	RSS = ['http://www.ftchinese.com/rss/feed']

	def _jtof(self, text=''):
		try:
			text = jianfan.jtof(text)
			text = text.replace(u'“', u'「');
			text = text.replace(u'”', u'」');
		except Exception as e:
			pass
		return text

	def _fetch_articles_in_24hours(self, url):
		print url
		yesterday = utils.yesterday()
		articles = []
		response = urllib2.urlopen(url).read()
		parser = ET.XMLParser(encoding='utf-8')
		xml = ET.fromstring(response, parser=parser)
		for child in xml.iter('item'):
			find = lambda x: child.findall(x)[0].text
			publish_date_txt = find('pubDate')
			publish_date = datetime.datetime.\
						   strptime(publish_date_txt, "%a, %d %b %Y %H:%M:%S %Z")
			if publish_date > yesterday:
				title = find('title')
				title = self._jtof(title)
				article = {'link': find('link') + '?full=y',
						   'title': title,
						   'publish_date': publish_date}
				articles.append(article)
		return articles

	def fetch_article(self, url):
		def format_text(text):
			text = text.replace('<div id=story_main_mpu></div>', '')
			text = text.replace('</p>', '\n')
			text = re.sub('<[^<]+?>', '', text)
			return text

		assert url
		response = urllib2.urlopen(url).read().decode('utf-8')
		pattern = r'<!---->\n(.*)\n</div>'
		content = re.findall(pattern, response, re.MULTILINE)
		if len(content) < 1: return
		text = content[0]
		text = self._jtof(text)
		text = format_text(text).split('\n')
		return text

	def fetch_all_articles_in_24hours(self):
		'''
		Fetch all articles within 24 hours from the RSS feed of The
		Financial Times Chinese.
		'''

		all_articles = []
		for url in FinancialTimes.RSS:
			try:
				print('Fetching RSS feed from ' + url)
				articles = self._fetch_articles_in_24hours(url)
				all_articles += articles
				print('...Done.')
			except Exception as e:
				print('...Failed. ' + str(e))

		for article in all_articles:
			link = article['link']
			try:
				print('Fetching article from ' + link)
				text = self.fetch_article(link)
				article['text'] = text
				print('...Done.')
			except Exception as e:
				print('...Failed. ' + str(e))
		return all_articles
