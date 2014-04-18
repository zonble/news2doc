#!/usr/bin/env python
# encoding: utf-8

from wsj import *
from ft import *
from nyt import *
from docx import *

def make_doc(articles):
	print 'makeing .docx file.'

	document = Document()
	for article in articles:
		document.add_heading(article['title'], 1)
		document.add_paragraph(article['link'])
		document.add_paragraph(str(article['publish_date']))
		document.add_paragraph()
		if 'text' not in article: return
		text = article['text']
		if not text: return
		for line in text:
			# line = line.strip().decode('utf-8', 'ignore')
			line = line.strip()
			if len(line):
				document.add_paragraph(line)
	document.save('news.docx')

def main():
	articles = []
	# try: articles += WSJ().fetch_all_articles_in_24hours()
	# except: pass
	try: articles += FinancialTimes().fetch_all_articles_in_24hours()
	except: pass
	try: articles += NewYorkTimes().fetch_all_articles_in_24hours()
	except: pass
	make_doc(articles)

if __name__ == '__main__':
	main()
