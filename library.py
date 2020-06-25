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

# [PRE-SCRIPTING DIRECTIVES & CONSTANT CREATION]
intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'Ojg1Y2IzMzFlNjcxY2U3YmYwNzc5MjgyNTgwMjEyM2Jh'
company_api = intrinio_sdk.CompanyApi()

# [PRIMARY SCREEN FOR COMPANIES WITH M_CAPS GREATER THAN 3B.]
def compilepimary():
	dictionary_ticker_mc = {}
	filters = ['cap_midover','geo_usa']
	stock_list = Screener(filters=filters, table='Valuation', order='market cap')  # Get the performance table and sort it by price ascending
	for stock in stock_list:
		dictionary_ticker_mc[stock['Ticker']] = stock['Market Cap']
	remove = [k for k,v in dictionary_ticker_mc.items() if v == '-']
	for k in remove: 
		del dictionary_ticker_mc[k]
	return dictionary_ticker_mc

# [PULLS INFORMATION ABOUT EBIT AND ENTERPROSE VALUE. CALCULATE RATIO AND SAVES TO PICKLE FILE]
def first_rank(mydict):
	ebitev_dict = {}
	for k,v in mydict.items():
		#[OPENS UP INCOME STATEMENT]
		response = urlopen("https://financialmodelingprep.com/api/v3/income-statement/" + k + "?apikey=81ff40df1c59cd9cfc42b91bafe21a9a")
		data = response.read().decode("utf-8")
		incomedict = json.loads(data)

		#[OPEN SUP VALUATION MULTIPLES]
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
					print ("DATES ARE NOT THE SAME IN REPORTS.")
			except:
				print (incomedict, " ", evdict)
		else:
			print ("COULDN'T FIND A REPORT FOR: " + k)

	# [DUMPS FILE]
	with open('ebitev.pickle', 'wb') as f:
		pickle.dump(ebitev_dict, f, pickle.HIGHEST_PROTOCOL)

# [OPENS PICKLED FILE AND RANKS. RETURNS THE ARRAY OF TUPLES]
def first_numbering():
	rank_tupled = []
	with open ('ebitev.pickle', 'rb') as f:
		data = pickle.load(f)
	counter = 1;
	for k,v in sorted(data.items(), key = lambda item: item[1]):
		rank_tupled.append(((k,v), counter))
		counter+=1

	with open('rankedonebitev.pickle', 'wb') as f:
		pickle.dump(rank_tupled, f, pickle.HIGHEST_PROTOCOL)

# [TAKES IN RANKED ARRAY AND PARSES THE REMAINING RESULTS FOR ROCE. SAVES ROCE RESULTS TO PICKLED FILE]
def second_rank():
	# [OPENING UP PICKLED FILE]
	ebitroce_dict = {}
	with open ('rankedonebitev.pickle', 'rb') as f:
		arr = pickle.load(f)

	for item in arr:
		#[OPEN UP VALUATION MULTIPLES]
		roce_response = urlopen("https://financialmodelingprep.com/api/v3/ratios/" + item[0][0] + "?apikey=81ff40df1c59cd9cfc42b91bafe21a9a")
		dataroce = roce_response.read().decode("utf-8")
		rocedict = json.loads(dataroce)

		#[CALCULATIONS]
		if (len(rocedict) > 0):
			try: 
				if rocedict[0]['returnOnCapitalEmployed'] != None:
					ebitroce_dict[item[0][0]] = rocedict[0]['returnOnCapitalEmployed']
			except:
				print ("AN EXCEPTION OCCURRED")
		else: 
			print ("COULDNT FIND A ROCE MULTIPLE")

	#[DUMPS IT INTO PICKLE FILE]
	with open('ebitroce.pickle', 'wb') as file:
		pickle.dump(ebitroce_dict, file, pickle.HIGHEST_PROTOCOL)

# [OPENS PICKLED FILE AND RANKS. RETURNS THE ARRAY OF TUPLES]
def second_numbering():
	rank_tupled = []
	with open ('ebitroce.pickle', 'rb') as f:
		data = pickle.load(f)

	counter = 1
	for k,v in sorted(data.items(), key = lambda item: item[1]):
		rank_tupled.append(((k,v), counter))
		counter += 1

	with open('rankedonebitroce.pickle', 'wb') as file:
		pickle.dump(rank_tupled, file, pickle.HIGHEST_PROTOCOL)

# [OPENS UP THE TWO RANKED PICKLED FILES AND COMBINES THE RANKING]
def final_numbering():
	final_rank = []
	with open ('rankedonebitev.pickle', 'rb') as f:
		ebitev = pickle.load(f)
	with open('rankedonebitroce.pickle', 'rb') as file:
		ebitroce = pickle.load(file)

	for item in ebitev:
		ebit_rank = item[1]
		for entry in ebitroce:
			if (entry[0][0] == item[0][0]):
				roce_rank = entry[1]
				final_rank.append((item[0][0], ebit_rank + roce_rank))

	final_rank.sort(key = lambda x:x[1])
	for i in range(0, 20):
		print (final_rank[len(final_rank)-(i+1)][0])

#[DRIVER]
def testmain():
	# primary_dict = compilepimary()
	# first_rank(primary_dict)
	# first_numbering()
	# second_rank()
	# second_numbering()
	final_numbering()

testmain()
