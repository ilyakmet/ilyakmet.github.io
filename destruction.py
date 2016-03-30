# -*- coding: utf-8 -*-

import urllib.request
from socket import timeout
from bs4 import BeautifulSoup
import random




BASE_URL = 'https://www.reformagkh.ru/myhouse/profile/archive/'
DIR = '/Users/ilya/Desktop/maps/'
MAIN_DATA = 'housedata_final.csv'




def get_html(url):
    response = urllib.request.urlopen(url, timeout=10)
    return response.read()

def archive_url(url):
	soup = BeautifulSoup(get_html(url), 'html.parser')
	archive = soup.find('a', class_='label block_label label_archive_profile')['href']
	return archive

def d_percent(url):
	try:
		soup = BeautifulSoup(get_html('https://www.reformagkh.ru' + archive_url(url)), 'html.parser')
		percent = soup.find_all('table', class_='col_list')[2].find_all('span')[1].text.strip().strip('%')
		final_percent = float(percent)
		if final_percent > 100:
			final_percent = 'year'
	except(urllib.error.HTTPError, urllib.error.URLError):
		print('connection error')
		final_percent = 'connection error'
	except timeout:
		print('timeout')
		final_percent = 'timeout'
	except:
		final_percent = 'nodata'
	return final_percent

def out(name):
	try:
		f = open(name, 'r')
		f2 = open(DIR + 'house_percent.csv', 'w')
		f2.write('id,lat,lon,percent\n')
		count = 0
		for i in f:
			print('operation:', count)
			s = i.split(',')
			f2.write( s[0] + ',' + s[1] + ',' + s[2].strip('\n') + ',' + str(d_percent(BASE_URL+s[0])) + '\n')
			count += 1
	except:
		f.close()
		print('END')
	f.close()

def to_final_csv(name):
	print('start to_final_csv')
	f = open(name, 'r')
	f2 = open('housedata_final.csv', 'w')
	count = 0
	for i in f:
		s = i.split(',')
		print(s)
		try:
			f2.write(s[2] + ',' + s[0].strip('"') + ',' + s[1] + '\n')
			count += 1
		except IndexError:
			print('error')
	f2.close()
	print('total: ',count)

def to_final_csv_errors(name):
	print('start to_final_csv_errors')
	f = open(name, 'r')
	f2 = open('housedata_final_errors.csv', 'w')
	count = 0
	for i in f:
		s = i.split(',')
		print(s)
		if ('connection error\n' in s)or('timeout\n' in s):
			try:
				f2.write(s[0].strip('\n') + ',' + s[1].strip('\n') + ',' + s[2].strip('\n') + '\n')
				count += 1
			except IndexError:
				print('error')
	f2.close()
	print('total errors: ',count)

def remove_nodata(name):
	print('start remove_nodata')
	f = open(name, 'r')
	f2 = open('house_percent_final_' + str(random.randint(1000,1000000)) + '.csv', 'w')
	count = 0
	for i in f:
		s = i.split(',')
		print(s)
		if (('nodata\n' in s)or('timeout\n' in s)or('connection error\n' in s)or('year\n' in s)) == False:
			try:
				f2.write(s[0] + ',' + s[1] + ',' + s[2] + ',' + s[3])
				count += 1
			except IndexError:
				print('error')
	f2.close()
	print('total nodata: ',count)

def main():
	#to_final_csv('housedata.csv')
	out(DIR + MAIN_DATA)
	to_final_csv_errors(DIR + 'house_percent.csv')
	remove_nodata(DIR + 'house_percent.csv')




if __name__ == '__main__':
    main()