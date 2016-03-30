# -*- coding: utf-8 -*-

import urllib.request
from socket import timeout
from bs4 import BeautifulSoup
import random
from datetime import datetime




BASE_URL = 'https://www.reformagkh.ru/myhouse/profile/archive/'
DIR = '/Users/ilya/Documents/ilyakmet.github.io/'
MAIN_DATA = 'housedata_final.csv'




def get_html(url):
    response = urllib.request.urlopen(url, timeout=8)
    return response.read()

def archive_url(url):
	soup = BeautifulSoup(get_html(url), 'html.parser')
	url = soup.find_all('a', class_='label block_label label_archive_profile')
	archive = 0
	for i in url:
		if (not('882' in i.text))and(archive == 0):
			archive = i['href']
	if archive == 0:
		archive = 'nodata'
	return archive

def d_percent(url):
	try:
		archive = archive_url(url)
		if archive != 'nodata':
			soup = BeautifulSoup(get_html('https://www.reformagkh.ru' + archive), 'html.parser')
			percent = soup.find_all('table', class_='col_list')[2].find_all('span')[1].text.strip().strip('%')
			final_percent = float(percent)
			if final_percent > 100:
				final_percent = 'nodata'
		else:
			final_percent = 'nodata'
	except(urllib.error.HTTPError, urllib.error.URLError):
		print('d_percent connection error')
		final_percent = 'connection error'
	except timeout:
		print('d_percent timeout')
		final_percent = 'timeout'
	except:
		final_percent = 'nodata'
	return final_percent

def finance(url):
	try:
		archive = archive_url(url)
		if archive != 'nodata':
			soup = BeautifulSoup(get_html('https://www.reformagkh.ru' + archive_url(url).replace('view', 'finance')), 'html.parser')
			finance_web = soup.find_all('div', class_='w520')[1].find('div', class_='numbered').find_all(class_='nowrap')
			finance = {}
			float(finance_web[0].text.replace(' ','').strip('\n'))
			finance['income'] = finance_web[0].text.replace(' ','').strip('\n')
			finance['expenditures'] = finance_web[2].text.replace(' ','').strip('\n')
			finance['external'] = finance_web[13].text.replace(' ','').strip('\n')
		else:
			finance = {}
			finance['income'] = 'nodata'
			finance['expenditures'] = 'nodata'
			finance['external'] = 'nodata'
	except(urllib.error.HTTPError, urllib.error.URLError):
		print('finance connection error')
		finance = {}
		finance['income'] = 'connection error'
		finance['expenditures'] = 'connection error'
		finance['external'] = 'connection error'
	except timeout:
		print('finance timeout')
		finance = {}
		finance['income'] = 'timeout'
		finance['expenditures'] = 'timeout'
		finance['external'] = 'timeout'
	except:
		finance = {}
		finance['income'] = 'nodata'
		finance['expenditures'] = 'nodata'
		finance['external'] = 'nodata'
	return finance

#[gaz, heating, power, cold, water_remove, hot], (on/off, need, date on)
def calc_tools(id):
	try:
		soup = BeautifulSoup(get_html('https://www.reformagkh.ru/myhouse/profile/view/' + id), 'html.parser')
		calc_web = soup.find('div', id='tab1-subtab5').find_all('tbody')
		calc= []
		for i in calc_web[0:len(calc_web):2]:
			row = i.find('tr').text.strip('\n').split('\n') 
			print(row)
			if len(row) < 3:
				if 'не' in row[1]:
					calc.append((0,0,0))
				else:
					calc.append((0,1,0))
			else:
				calc.append((1,1,row[3]))
	except(urllib.error.HTTPError, urllib.error.URLError):
		print('connection error')
		calc = [('connection error', 0, 0), ('connection error', 0, 0), ('connection error', 0, 0), ('connection error', 0, 0), ('connection error', 0, 0), ('connection error', 0, 0), ('connection error', 0, 0)]
	except timeout:
		print('timeout')
		calc = [('timeout', 0, 0), ('timeout', 0, 0), ('timeout', 0, 0), ('timeout', 0, 0), ('timeout', 0, 0), ('timeout', 0, 0), ('timeout', 0, 0)]
	except:
		calc = [('nodata', 0, 0), ('nodata', 0, 0), ('nodata', 0, 0), ('nodata', 0, 0), ('nodata', 0, 0), ('nodata', 0, 0), ('nodata', 0, 0)]
	return calc

'''
def out(name, total, border):
	try:
		f = open(name, 'r')
		f2 = open(DIR + 'house_percent.csv', 'w')
		f2.write('id,lat,lon,percent,income,expenditures,external\n')
		count = 0
		for i in f:
			time = datetime.now()
			print('operation:', count, '/', total)
			if count < border:
				s = i.split(',')
				#print(s)
				percent_row = d_percent(BASE_URL + s[0])
				#print('percent:', percent_row)
				if type(percent_row) == type(float()):
					finance_row = finance(BASE_URL + s[0])
					f2.write( s[0] + ',' + s[1] + ',' + s[2].strip('\n') + ',' + str(percent_row) + ',' + finance_row['income'] + ',' + finance_row['expenditures'] + ',' + finance_row['external'] + '\n')
				else:
					#print('not float')
					f2.write( s[0] + ',' + s[1] + ',' + s[2].strip('\n') + ',' + str(percent_row) + ',' + 'nodata' + ',' + 'nodata' + ',' + 'nodata' + '\n')
				count += 1
				print('speed:', datetime.now() - time)
	except:
		f.close()
		print('ERROR')
		print('out_total:', count)
	f.close()
	print('END')
	print('out_total:', count)
'''
def out(name, total, border):
	try:
		f = open(name, 'r')
		f2 = open(DIR + 'house_percent.csv', 'w')
		f2.write('id,lat,lon,percent,income,expenditures,external,gaz,on/off, need, date on,heating,on/off, need, date on,power,on/off, need, date on,cold,on/off, need, date on,water_remove,on/off, need, date on,hot,on/off, need, date on\n')
		count = 0
		for i in f:
			time = datetime.now()
			print('operation:', count, '/', total)
			if count < border:
				s = i.split(',')
				#print(s)
				calc_tools(s[0])
				finance_row = finance(BASE_URL + s[0])
				f2.write( s[0] + ',' + s[1] + ',' + s[2].strip('\n') + ',' + str(d_percent(BASE_URL + s[0])) + ',' + finance_row['income'] + ',' + finance_row['expenditures'] + ',' + finance_row['external'] + '\n')
				count += 1
				speed = datetime.now() - time
				print('speed:', speed, 'wait:', (float(str(speed).split(':')[2])*(total-count))/60/60)
	except:
		f.close()
		print('ERROR')
		print('out_total:', count)
	f.close()
	print('END')
	print('out_total:', count)


def to_final_csv(name):
	print('start to_final_csv')
	f = open(name, 'r')
	f2 = open(DIR + 'housedata_final.csv', 'w')
	count = 0
	for i in f:
		s = i.split(',')
		try:
			f2.write(s[2] + ',' + s[0].strip('"') + ',' + s[1] + '\n')
			count += 1
		except IndexError:
			print('nodata')
	f2.close()
	#print('total: ',count)
	return count

def to_final_csv_errors(name):
	print('start to_final_csv_errors')
	f = open(name, 'r')
	f2 = open(DIR + 'housedata_final_errors.csv', 'w')
	count = 0
	for i in f:
		s = i.split(',')
		print(s)
		if ('connection error' in s)or('timeout' in s):
			try:
				f2.write(s[0].strip('\n') + ',' + s[1].strip('\n') + ',' + s[2].strip('\n') + '\n')
				count += 1
			except IndexError:
				print('error')
	f2.close()
	#print('total errors: ',count)
	return count

def remove_nodata(name):
	print('start remove_nodata')
	f = open(name, 'r')
	f2 = open(DIR + 'house_percent_final_' + str(random.randint(1000,1000000)) + '.csv', 'w')
	count = 0
	for i in f:
		s = i.split(',')
		print(s)
		if (('timeout' in s)or('connection error' in s)or('timeout\n' in s)or('connection error\n' in s)) == False:
			try:
				f2.write(s[0] + ',' + s[1] + ',' + s[2] + ',' + s[3]  + ',' + s[4] + ',' + s[5] + ',' + s[6])
				count += 1
			except IndexError:
				print('error')
	f2.close()
	#print('total nodata: ',count)
	return count

def main():
	total = to_final_csv(DIR + 'housedata.csv')
	out(DIR + MAIN_DATA, total, 10)
	errors = to_final_csv_errors(DIR + 'house_percent.csv')
	nodata = remove_nodata(DIR + 'house_percent.csv')
	print('total:', total, '\n', 'errors:', errors, '\n', 'nodata:', total-nodata, '\n', 'copmlete:', total - errors - nodata, '\n')


if __name__ == '__main__':
    main()