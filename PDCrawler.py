import os

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from datetime import date, timedelta
from dateutil import rrule

class PDCrawler:
	def UrlGen(sdate, edate):
		syear = sdate[:4]
		smonth = sdate[5:7]
		sday = sdate[8:10]
		sdate = date(int(syear), int(smonth), int(sday))

		eyear = edate[:4]
		emonth = edate[5:7]
		eday = edate[8:10]
		edate = date(int(eyear), int(emonth), int(eday))

		Urls = list()

		cdate = sdate
		for dday in range((edate - sdate).days + 1):
			cyear = cdate.year
			cmonth = cdate.month
			cday = cdate.day

			Urls.append("http://paper.people.com.cn/rmrb/html/" + str(cyear) + "-" + str(cmonth).zfill(2) + "/" + str(cday).zfill(2) + "/nbs.D110000renmrb_01.htm")
			cdate = cdate + timedelta(days = 1)
		return(Urls)
		

	def PageUrlExtract(link):
		PUrls = list()
		r = requests.get(link)
		soup = BeautifulSoup(r.text, "html.parser")
		tmp = soup.find_all('a', id = "pageLink")
		for t in tmp:
			if t['href'][:1] == ".":
				PUrls.append(link[:48] + t['href'][2:])
			else:
				PUrls.append(link[:48] + t['href'])
		return(PUrls)

	def NewsExtract(sdate, edate):
		Links = PDCrawler.UrlGen(sdate, edate)

		syear = sdate[:4]
		smonth = sdate[5:7]
		sday = sdate[8:10]
		sdate = date(int(syear), int(smonth), int(sday))

		eyear = edate[:4]
		emonth = edate[5:7]
		eday = edate[8:10]
		edate = date(int(eyear), int(emonth), int(eday))
		
		cdate = sdate

		for link in Links:
			cyear = cdate.year
			cmonth = cdate.month
			cday = cdate.day

			cfile = str(cyear) + "-" + str(cmonth).zfill(2) + "-" + str(cday).zfill(2) + ".txt"
			cdate = cdate + timedelta(days = 1)
			f = open(cfile, "w")
			f = open(cfile, "a")

			PLinks = PDCrawler.PageUrlExtract(link)
			for plink in PLinks:
				r = requests.get(plink)
				r.encoding = 'utf-8'
				soup = BeautifulSoup(r.text, "html.parser")
				tmp = soup.find_all('div', id = "titleList")
				purls = tmp[0].find_all('li')
				
				for pl in purls:
					url = plink[:48] + pl.a["href"]
					p = requests.get(url)
					p.encoding = 'utf-8'
					subsoup = BeautifulSoup(p.text, "html.parser")
					art = subsoup.find_all('div', id = "ozoom")
					for a in art:
						f.write(a.text[150:].strip())
			f.close()

PDCrawler.NewsExtract("2017-01-15", "2018-01-15")
