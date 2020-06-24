# [AUTHOR: RAHUL MEHTA]
# [ALPHA VERSION: JUNE 23, 2020]
# [NAME: library.py]

# [IMPORTS]
from __future__ import print_function
import csv
import time
import json
import pickle
import intrinio_sdk
from pprint import pprint
from urllib.request import urlopen
from finviz.screener import Screener
from intrinio_sdk.rest import ApiException

# [PRESCRIPTING DIRECTIVES & CONSTANT CREATION]
intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'Ojg1Y2IzMzFlNjcxY2U3YmYwNzc5MjgyNTgwMjEyM2Jh'
company_api = intrinio_sdk.CompanyApi()
tag = 'ebit'

# [LOOK AT COMPANIES WITH MCAPS OVER 3B]
def compilepimary():
	dictionary_ticker_mc = {}
	filters = ['cap_midover','geo_usa']
	print (filters)
	stock_list = Screener(filters=filters, table='Valuation', order='market cap')  # Get the performance table and sort it by price ascending
	for stock in stock_list:
		dictionary_ticker_mc[stock['Ticker']] = stock['Market Cap']
	remove = [k for k,v in dictionary_ticker_mc.items() if v == '-']
	for k in remove: 
		del dictionary_ticker_mc[k]
	return dictionary_ticker_mc

def first_rank(mydict):
	ebitev_dict = {}
	for k,v in mydict.items():
		#[OPEN UP INCOME STATEMENT]
		response = urlopen("https://financialmodelingprep.com/api/v3/income-statement/" + k + "?apikey=81ff40df1c59cd9cfc42b91bafe21a9a")
		data = response.read().decode("utf-8")
		incomedict = json.loads(data)

		#[OPEN UP VALUATION MULTIPLES]
		ev_response = urlopen("https://financialmodelingprep.com/api/v3/enterprise-values/" + k + "?apikey=81ff40df1c59cd9cfc42b91bafe21a9a")
		dataev = ev_response.read().decode("utf-8")
		evdict = json.loads(dataev)

		#[CALCULATIONS]
		if (len(incomedict) > 0 and len(evdict) > 0):
			try: 
				if (incomedict[0]['date'] == evdict[0]['date']):
					ebit = incomedict[0]['ebitda'] - incomedict[0]['depreciationAndAmortization']
					ev = evdict[0]['enterpriseValue']
					ebitev_dict[k] = ebit/ev
				else:
					print ("DATES ARE NOT THE SAME")
			except:
				print (incomedict)
				print ("")
				print (evdict)
		else:
			print (k)
	with open('ebitev.pickle', 'wb') as f:
		pickle.dump(ebitev_dict, f, pickle.HIGHEST_PROTOCOL)

def testmain():
	primary_dict = compilepimary()
	first_rank(primary_dict)

testmain()
