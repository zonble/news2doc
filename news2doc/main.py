#!/usr/bin/env python
# encoding: utf-8

from wsj import *
from docx import *

def make_doc(articles):
	print 'makeing .docx file.'

	document = Document()
	for article in articles:
		document.add_heading(article['title'], 1)
		document.add_paragraph(article['link'])
		document.add_paragraph(str(article['publish_date']))
		document.add_paragraph()
		text = article['text']
		for line in text:
			line = line.strip().decode('utf-8')
			document.add_paragraph(line)
	document.save('news.docx')

def main():
	articles = []
	articles += WSJ().fetch_all_articles_in_24hours()
	# print articles
	make_doc(articles)

if __name__ == '__main__':
	main()
