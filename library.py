# [AUTHOR: RAHUL MEHTA]
# [ALPHA VERSION: JUNE 23, 2020]
# [NAME: library.py]

from __future__ import print_function
from finviz.screener import Screener
import csv
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint

intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'Ojc5MDA4MWViMDRlN2E1MzNlNTExY2M1ZWE4MjhhNDA1'
company_api = intrinio_sdk.CompanyApi()
tag = 'ebit'

def compilepimary():
	dictionary_ticker_mc = {}
	filters = ['f=cap_microover','geo_usa']  #
	stock_list = Screener(filters=filters, table='Valuation', order='market cap')  # Get the performance table and sort it by price ascending
	for stock in stock_list:
		dictionary_ticker_mc[stock['Ticker']] = stock['Market Cap']
	remove = [k for k,v in dictionary_ticker_mc.items() if v == '-']
	for k in remove: 
		del dictionary_ticker_mc[k]
	return dictionary_ticker_mc

def firstrank(pdict):
	second_dict = {}
	for k,v in pdict.items():
		try:
			identifier = k
			api_response = company_api.get_company_data_point_number(identifer, tag)
			pprint (api_response)
		except:
			print ("EXCEPTION")
    
def testmain():
	primary_dict = compilepimary()
	first_rank = firstrank(primary_dict)

testmain()
