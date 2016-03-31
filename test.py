# -*- coding: utf-8 -*-

import urllib.request
from socket import timeout
from bs4 import BeautifulSoup
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
			if len(row) < 3:
				if 'не' in row[1]:
					calc.append((0,0,0))
				else:
					tcalc = calc.append((0,1,0))
					print(tcalc)
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

def housedata_final(name):
	print('start housedata_final')
	f = open(name, 'r')
	f2 = open(DIR + 'housedata_final_test.csv', 'w')
	count = 0
	for i in f:
		s = i.split(',')
		try:
			int(s[2])
			f2.write(s[2] + ',' + s[0].strip('"') + ',' + s[1] + '\n')
			count += 1
		except:
			print('nodata')
	f2.close()
	return count

def to_house_final(name):
	time = str(datetime.now())
	print('start to_house_final')
	f = open(name, 'r')
	f2 = open(DIR + 'house_parse_data_errors_' + str(time) +'.csv', 'w')
	f3 = open(DIR + 'house_final_' + str(time) + '_.csv', 'w')
	errors_count = 0
	complete_count = 0
	for i in f:
		s = i.split(',')
		print(s)
		try:
			if (('timeout' in s)or('connection error' in s)or('timeout\n' in s)or('connection error\n' in s)):
				f2.write(s[0].strip('\n') + ',' + s[1].strip('\n') + ',' + s[2].strip('\n') + '\n')
				errors_count += 1
			else:
				if not('nodata' in s):
					f3.write(s[0])
					for i in s[1:]:
						f3.write(',' + str(i))
					f3.write('\n')
					complete_count += 1
		except IndexError:
			print('error')
	f2.close()
	f3.close()
	return errors_count, complete_count

def out(name, total, border):
	try:
		f = open(name, 'r')
		f2 = open(DIR + 'house_parse_data.csv', 'w')
		f2.write('id,lat,lon,gaz, need, date on,heating, need, date on,power, need, date on,cold, need, date on,water_remove, need, date on,hot, need, date on\n')
		count = 0
		for i in f:
			time = datetime.now()
			if count <= border:
				print('operation:', count, '/', border)
				s = i.split(',')
				calc = calc_tools(s[0]) 
				#f2.write( s[0] + ',' + s[1] + ',' + s[2].strip('\n') + ',' + str(d_percent(BASE_URL + s[0])) + '\n')
				f2.write(s[0] + ',' + s[1] + ',' + s[2].strip('\n'))
				for i in calc:
					for j in i:
						f2.write(',' + str(j))
				f2.write('\n')
				count += 1
				speed = datetime.now() - time
				print('speed:', speed, 'wait:', (float(str(speed).split(':')[2])*(border-count))/60/60, 'h')			
	except:
		f.close()
		print('ERROR')
		print('out_total:', count)	
	f.close()
	print('END')
	return count

def main():
	total = housedata_final(DIR + 'housedata.csv')
	out_total = out(DIR + MAIN_DATA, total, 10)
	errors, complete = to_house_final(DIR + 'house_parse_data.csv')
	print()
	print('total:', out_total - 1, '\n', 'errors:', errors, '\n', 'copmlete:', complete, '\n', 'nodata:~', (out_total - complete)*100/out_total, '%')


if __name__ == '__main__':
    main()