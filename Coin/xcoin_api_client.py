#
# XCoin API-call related functions
#
# @author	btckorea
# @date	2017-04-12
#
# Compatible with python3 version.

import sys
import time
import math
import base64
import hmac, hashlib
import urllib.parse
import pycurl
import json


class XCoinAPI:
	api_url = "https://api.bithumb.com";
	api_key = "";
	api_secret = "";

	def __init__(self, api_key, api_secret):
		self.api_key = api_key;
		self.api_secret = api_secret;

	def body_callback(self, buf):
		self.contents = buf;

	def microtime(self, get_as_float = False):
		if get_as_float:
			return time.time()
		else:
			return '%f %d' % math.modf(time.time())

	def usecTime(self) :
		mt = self.microtime(False)
		mt_array = mt.split(" ")[:2];
		return mt_array[1] + mt_array[0][2:5];

	def xcoinApiCall(self, endpoint, rgParams):
		# 1. Api-Sign and Api-Nonce information generation.
		# 2. Request related information from the Bithumb API server.
		#
		# - nonce: it is an arbitrary number that may only be used once.
		# - api_sign: API signature information created in various combinations values.

		endpoint_item_array = {
			"endpoint" : endpoint
		};

		uri_array = dict(endpoint_item_array, **rgParams); # Concatenate the two arrays.
		#print("uri_array=",uri_array);

		str_data = urllib.parse.urlencode(uri_array);
		#print("str_data=", str_data);

		nonce = self.usecTime();
		#print("nonce =", nonce);

		data = endpoint + chr(0) + str_data + chr(0) + nonce;
		#print("data =", data);
		utf8_data = data.encode('utf-8');
		#print("utf8_data =", utf8_data);

		key = self.api_secret;
		#print("key =", key);
		utf8_key = key.encode('utf-8');
		#print("utf8_key =", utf8_key);

		h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512);
		#print("h =", h);
		hex_output = h.hexdigest();
		#print("hex_output =", hex_output);

		utf8_hex_output = hex_output.encode('utf-8');
		#print("utf8_hex_output =", utf8_hex_output);

		api_sign = base64.b64encode(utf8_hex_output);
		#print("api_sign =", api_sign);
		utf8_api_sign = api_sign.decode('utf-8');
		#print("utf8_api_sign =", utf8_api_sign);


		curl_handle = pycurl.Curl();
		curl_handle.setopt(pycurl.POST, 1);
		#curl_handle.setopt(pycurl.VERBOSE, 1); # vervose mode :: 1 => True, 0 => False
		curl_handle.setopt(pycurl.POSTFIELDS, str_data);

		url = self.api_url + endpoint;
		#print("url=", url);
		curl_handle.setopt(curl_handle.URL, url);
		#headers = { 'User-Agent' : 'Mozilla/5.0' }
		usragent = "Mozilla/5.0"
		utf8_usragent = usragent.encode('utf-8');
		curl_handle.setopt(curl_handle.HTTPHEADER, ['Api-Key: ' + self.api_key, 'Api-Sign: ' + utf8_api_sign, 'Api-Nonce: ' + nonce, 'User-Agent: ' + usragent]);
		curl_handle.setopt(curl_handle.WRITEFUNCTION, self.body_callback);
		curl_handle.perform();

		#response_code = curl_handle.getinfo(pycurl.RESPONSE_CODE); # Get http response status code.

		curl_handle.close();

		#print(self.contents);
		return (json.loads(self.contents));
