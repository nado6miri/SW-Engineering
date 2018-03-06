import os
import sys
from xcoin_api_client import *
from binance.client import Client
import pprint

import json
import urllib.request
from urllib.request import Request, urlopen

import threading
import datetime
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

ret = 0;

bithumb_rgParams = {
	"order_currency" : "ALL",
	"payment_currency" : "KRW"
};

coin = ["ETH", "EOS", "ETC", "LTC", "DASH", "XRP", "XMR", "QTUM", "ZEC"];
coin_binance = ["ETHUSDT", "EOSETH", "ETCETH", "LTCETH", "DASHETH", "XRPETH", "XMRETH", "QTUMETH", "ZECETH"];

coin_map = {
			"ETHUSDT" : "ETH",
			"EOSETH" : "EOS",
			"ETCETH" : "ETC",
			"LTCETH" : "LTC",
			"DASHETH" : "DASH",
			"XRPETH" : "XRP",
			"XMRETH" : "XMR",
			"QTUMETH" : "QTUM",
			"ZECETH" : "ZEC"
			};

class Exchange:
	infoA = {
		'Exchange' : "----", # User Input Value
		'Cur_Price' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, # Get Price valule from Server Api
		'ETH_Ratio' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, # ETH_Ratio["EOS"] = Cur_Price["ETH"] / Cur_Price["EOS"]
		'Coin_Cnt' : { "ETH" : 1, "EOS" : 11806, "ETC" : 1000, "LTC" : 1000, "DASH" : 1000, "XRP" : 1000, "XMR" : 1000, "QTUM" : 1000, "ZEC" : 1000 }, # User Input Value
		'ETH_Cnt' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, # ETH_Cnt["EOS"] = Coint_Cnt["EOS"] * (1/ETH_Ratio["EOS"])
		'Result_Cnt' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, #이동후 변환개수 : Result_Cnt["EOS"] = Dest(ETH_Ratio["EOS"]) * Dest(ETH_Cnt["EOS"])
		'Profit_Cnt' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, #손익판단 : Profit_Cnt["EOS"] = Result_Cnt["EOS"] - Conie_Cnt["EOS"]
	};

	infoB = {
		'Exchange' : "----", # User Input Value
		'Cur_Price' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, # Get Price valule from Server Api
		'ETH_Ratio' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, # ETH_Ratio["EOS"] = Cur_Price["ETH"] / Cur_Price["EOS"]
		'Coin_Cnt' : { "ETH" : 1, "EOS" : 11806, "ETC" : 1000, "LTC" : 1000, "DASH" : 1000, "XRP" : 1000, "XMR" : 1000, "QTUM" : 1000, "ZEC" : 1000 }, # User Input Value
		'ETH_Cnt' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, # ETH_Cnt["EOS"] = Coint_Cnt["EOS"] * (1/ETH_Ratio["EOS"])
		'Result_Cnt' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, #이동후 변환개수 : Result_Cnt["EOS"] = Dest(ETH_Ratio["EOS"]) * Dest(ETH_Cnt["EOS"])
		'Profit_Cnt' : { "ETH" : 1, "EOS" : 0, "ETC" : 0, "LTC" : 0, "DASH" : 0, "XRP" : 0, "XMR" : 0, "QTUM" : 0, "ZEC" : 0 }, #손익판단 : Profit_Cnt["EOS"] = Result_Cnt["EOS"] - Conie_Cnt["EOS"]
	};




form_class = uic.loadUiType("./QtUI/Coin.ui")[0];

#class MyWindow(QMainWindow):
class MyWindow(QMainWindow, form_class) :
	def __init__(self):
		super().__init__();
		self.setWindowTitle("Coin Master");
		self.setupUi(self);
		self.exchg = Exchange();

		self.myEOSCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["EOS"]));
		self.myLTCCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["LTC"]));
		self.myXMRCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["XMR"]));
		self.myXRPCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["XRP"]));
		self.myZECCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["ZEC"]));
		self.myQTUMCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["QTUM"]));
		self.myETCCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["ETC"]));
		self.myDASHCnt.setText(str(self.exchg.infoA["Coin_Cnt"]["DASH"]));

		self.myEOSCnt.textChanged.connect(self.setMyEOSCnt);
		self.myLTCCnt.textChanged.connect(self.setMyLTCCnt);
		self.myXMRCnt.textChanged.connect(self.setMyXMRCnt);
		self.myXRPCnt.textChanged.connect(self.setMyXRPCnt);
		self.myZECCnt.textChanged.connect(self.setMyZECCnt);
		self.myQTUMCnt.textChanged.connect(self.setMyQTUMCnt);
		self.myETCCnt.textChanged.connect(self.setMyETCCnt);
		self.myDASHCnt.textChanged.connect(self.setMyDASHCnt);

		self.coin_timer_start();
		self.get_curtime_start();

	def setMyEOSCnt(self):
		data = self.myEOSCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["EOS"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["EOS"] = int(data);
		print("setMyEOSCnt= ", self.myEOSCnt.text());
		pass

	def setMyLTCCnt(self):
		data = self.myLTCCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["LTC"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["LTC"] = int(data);
		print("setMyLTCCnt= ", self.myLTCCnt.text());
		pass

	def setMyXMRCnt(self):
		data = self.myXMRCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["XMR"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["XMR"] = int(data);
		print("setMyXMRCnt= ", self.myXMRCnt.text());
		pass

	def setMyXRPCnt(self):
		data = self.myXRPCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["XRP"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["XRP"] = int(data);
		print("setMyXRPCnt= ", self.myXRPCnt.text());
		pass

	def setMyZECCnt(self):
		data = self.myZECCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["ZEC"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["ZEC"] = int(data);
		print("setMyZECCnt= ", self.myZECCnt.text());
		pass

	def setMyQTUMCnt(self):
		data = self.myQTUMCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["QTUM"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["QTUM"] = int(data);
		print("setMyQTUMCnt= ", self.myQTUMCnt.text());
		pass

	def setMyDASHCnt(self):
		data = self.myDASHCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["DASH"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["DASH"] = int(data);
		print("setMyDASHCnt= ", self.myDASHCnt.text());
		pass

	def setMyETCCnt(self):
		data = self.myETCCnt.text();
		if(data == ""):
			self.exchg.infoA["Coin_Cnt"]["ETC"] = 1;
		else:
			self.exchg.infoA["Coin_Cnt"]["ETC"] = int(data);
		print("setMyETCCnt= ", self.myETCCnt.text());
		pass


	def getConnection(self, kindofexchange):
		client = 0;
		if(kindofexchange == "Bithumb") :
			#print("\ngetConnection : Bithumb");
			api_key = "api_connect_key";
			api_secret = "api_secret_key";
			client = XCoinAPI(api_key, api_secret);
			return client;
		elif (kindofexchange == "Binance") :
			#print("\ngetConnection : Binance");
			api_key = "AD0eZpGTPLSsmmVKNaQfmcF84SeimFX884i5hkz4ESHse4IG93KVTmpN5Zn5Rw996";
			api_secret = "Ao1CShHsHxVzzPmGH1mxRrG9Pw4rcXoTKNM9sxG9KKMWDBe3yRNzArKFbOxYGPU7j";
			client = Client(api_key, api_secret)
			return client;
		else :
			print("getConnection : none");

	def getCryptoCurrencyPrice(self, connection, kindofexchange, kindofcoine):
		if(kindofexchange == "Bithumb") :
			#print("Bithumb Price of " + kindofcoine + "\n");
			bithumb_rgParams["order_currency"] = kindofcoine;
			#print(bithumb_rgParams);
			coin = "/public/ticker/" + kindofcoine;
			#coin = "/public/ticker/all";
			#print("Bithumb Price of " + bithumb_rgParams["order_currency"]);
			ret = connection.xcoinApiCall(coin, bithumb_rgParams);
		elif (kindofexchange == "Binance") :
			#print("get_orderbook_ticker\n");
			ret = connection.get_orderbook_ticker(symbol=kindofcoine);
		else:
			ret = 0;
		return ret;

	def coin_pricecheck(self):
		# get coin price from Binance Exchange
		bApi = self.getConnection("Binance");
		self.exchg.infoB["Exchange"] = "Binance";
		index = 0;
		for i in coin_binance:
			result = self.getCryptoCurrencyPrice(bApi, "Binance", i);
			j = coin_map[i];
			index += 1;
			#print("coin/eth = ", j + "--> sell: " + result["bidPrice"]);
			if(j == "ETH") :
				self.exchg.infoB["Cur_Price"][j] = float(result["bidPrice"]);
				self.exchg.infoB["ETH_Ratio"][j] = 1;
			else :
				self.exchg.infoB["Cur_Price"][j] = float(self.exchg.infoB["Cur_Price"]["ETH"]) * float(result["bidPrice"]);
				self.exchg.infoB["ETH_Ratio"][j] = float(result["bidPrice"]);
				self.exchg.infoB["ETH_Cnt"][j] = self.exchg.infoB["Coin_Cnt"][j] * self.exchg.infoB["ETH_Ratio"][j];

		# get coin price from Bithumb Exchange
		aApi = self.getConnection("Bithumb");
		self.exchg.infoA["Exchange"] = "Bithumb";
		for i in coin:
			result = self.getCryptoCurrencyPrice(aApi, "Bithumb", i);
			if(result["status"] == "0000"):
				#print("coin = ", i + "--> sell: " + result["data"]["sell_price"]);
				self.exchg.infoA["Cur_Price"][i] = float(result["data"]["sell_price"]);
				if(i == "ETH") :
					self.exchg.infoA["ETH_Ratio"][i] = 1;
					continue
				else :
					self.exchg.infoA["ETH_Ratio"][i] = float(self.exchg.infoA["Cur_Price"][i]) / float(self.exchg.infoA["Cur_Price"]["ETH"]);
					self.exchg.infoA["ETH_Cnt"][i] = self.exchg.infoA["Coin_Cnt"][i] * self.exchg.infoA["ETH_Ratio"][i];

		# Calculate Transfer profit
		for i in coin:
			if(i == "ETH") :
				self.exchg.infoA["Result_Cnt"][i] = 1;
			else :
				self.exchg.infoA["Result_Cnt"][i] = (self.exchg.infoA["ETH_Cnt"][i] * 0.995) / self.exchg.infoB["ETH_Ratio"][i];
				self.exchg.infoA["Profit_Cnt"][i] = self.exchg.infoA["Result_Cnt"][i] - self.exchg.infoA["Coin_Cnt"][i];

		index = 0;
		for i in coin_binance:
			j = coin_map[i];
			index += 1;
			if(j == "ETH") :
				self.exchg.infoB["Result_Cnt"][j] = 1;
			else :
				self.exchg.infoB["Result_Cnt"][j] = (self.exchg.infoB["ETH_Cnt"][j] * 0.995) / self.exchg.infoA["ETH_Ratio"][j];
				self.exchg.infoB["Profit_Cnt"][j] = self.exchg.infoB["Result_Cnt"][j] - self.exchg.infoB["Coin_Cnt"][j];

		print("==================================");
		print("Bithumb --> Binance : ", self.exchg.infoA["Profit_Cnt"]["EOS"]);
		print("Binance --> Bithumb : ", self.exchg.infoB["Profit_Cnt"]["EOS"]);
		print("==================================");
		self.coinview_Update();
		pass

	def coinview_Update(self):
		print("Call coinview_Update");
		# 재정거래 예상 이익
		self.EOS_Diff.display(self.exchg.infoA["Profit_Cnt"]["EOS"]);
		self.ETC_Diff.display(self.exchg.infoA["Profit_Cnt"]["ETC"]);
		self.LTC_Diff.display(self.exchg.infoA["Profit_Cnt"]["LTC"]);
		self.XMR_Diff.display(self.exchg.infoA["Profit_Cnt"]["XMR"]);
		self.QTUM_Diff.display(self.exchg.infoA["Profit_Cnt"]["QTUM"]);
		self.ZEC_Diff.display(self.exchg.infoA["Profit_Cnt"]["ZEC"]);
		self.XRP_Diff.display(self.exchg.infoA["Profit_Cnt"]["XRP"]);
		self.DASH_Diff.display(self.exchg.infoA["Profit_Cnt"]["DASH"]);

		self.Src_ETH_Price.display(self.exchg.infoA["Cur_Price"]["ETH"]);
		self.Src_EOS_Price.display(self.exchg.infoA["Cur_Price"]["EOS"]);
		self.Src_ETC_Price.display(self.exchg.infoA["Cur_Price"]["ETC"]);
		self.Src_LTC_Price.display(self.exchg.infoA["Cur_Price"]["LTC"]);
		self.Src_XMR_Price.display(self.exchg.infoA["Cur_Price"]["XMR"]);
		self.Src_QTUM_Price.display(self.exchg.infoA["Cur_Price"]["QTUM"]);
		self.Src_ZEC_Price.display(self.exchg.infoA["Cur_Price"]["ZEC"]);
		self.Src_XRP_Price.display(self.exchg.infoA["Cur_Price"]["XRP"]);
		self.Src_DASH_Price.display(self.exchg.infoA["Cur_Price"]["DASH"]);

		self.Src_EOSETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["EOS"]);
		self.Src_ETCETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["ETC"]);
		self.Src_LTCETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["LTC"]);
		self.Src_XMRETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["XMR"]);
		self.Src_QTUMETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["QTUM"]);
		self.Src_ZECETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["ZEC"]);
		self.Src_XRPETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["XRP"]);
		self.Src_DASHETH_Ratio.display(self.exchg.infoA["ETH_Ratio"]["DASH"]);

		# 재정거래 예상
		self.Dst_EOS_TCnt.display(self.exchg.infoA["Result_Cnt"]["EOS"]);
		self.Dst_ETC_TCnt.display(self.exchg.infoA["Result_Cnt"]["ETC"]);
		self.Dst_LTC_TCnt.display(self.exchg.infoA["Result_Cnt"]["LTC"]);
		self.Dst_XMR_TCnt.display(self.exchg.infoA["Result_Cnt"]["XMR"]);
		self.Dst_QTUM_TCnt.display(self.exchg.infoA["Result_Cnt"]["QTUM"]);
		self.Dst_ZEC_TCnt.display(self.exchg.infoA["Result_Cnt"]["ZEC"]);
		self.Dst_XRP_TCnt.display(self.exchg.infoA["Result_Cnt"]["XRP"]);
		self.Dst_DASH_TCnt.display(self.exchg.infoA["Result_Cnt"]["DASH"]);

		# 재정거래 예상 이익
		self.EOS_PRatio.display(self.exchg.infoA["Profit_Cnt"]["EOS"]*100/self.exchg.infoA["Coin_Cnt"]["EOS"]);
		self.ETC_PRatio.display(self.exchg.infoA["Profit_Cnt"]["ETC"]*100/self.exchg.infoA["Coin_Cnt"]["ETC"]);
		self.LTC_PRatio.display(self.exchg.infoA["Profit_Cnt"]["LTC"]*100/self.exchg.infoA["Coin_Cnt"]["LTC"]);
		self.XMR_PRatio.display(self.exchg.infoA["Profit_Cnt"]["XMR"]*100/self.exchg.infoA["Coin_Cnt"]["XMR"]);
		self.QTUM_PRatio.display(self.exchg.infoA["Profit_Cnt"]["QTUM"]*100/self.exchg.infoA["Coin_Cnt"]["QTUM"]);
		self.ZEC_PRatio.display(self.exchg.infoA["Profit_Cnt"]["ZEC"]*100/self.exchg.infoA["Coin_Cnt"]["ZEC"]);
		self.XRP_PRatio.display(self.exchg.infoA["Profit_Cnt"]["XRP"]*100/self.exchg.infoA["Coin_Cnt"]["XRP"]);
		self.DASH_PRatio.display(self.exchg.infoA["Profit_Cnt"]["DASH"]*100/self.exchg.infoA["Coin_Cnt"]["DASH"]);


		self.Dst_ETH_Price.display(self.exchg.infoB["Cur_Price"]["ETH"]);
		self.Dst_EOS_Price.display(self.exchg.infoB["Cur_Price"]["EOS"]);
		self.Dst_ETC_Price.display(self.exchg.infoB["Cur_Price"]["ETC"]);
		self.Dst_LTC_Price.display(self.exchg.infoB["Cur_Price"]["LTC"]);
		self.Dst_XMR_Price.display(self.exchg.infoB["Cur_Price"]["XMR"]);
		self.Dst_QTUM_Price.display(self.exchg.infoB["Cur_Price"]["QTUM"]);
		self.Dst_ZEC_Price.display(self.exchg.infoB["Cur_Price"]["ZEC"]);
		self.Dst_XRP_Price.display(self.exchg.infoB["Cur_Price"]["XRP"]);
		self.Dst_DASH_Price.display(self.exchg.infoB["Cur_Price"]["DASH"]);

		self.Dst_EOSETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["EOS"]);
		self.Dst_ETCETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["ETC"]);
		self.Dst_LTCETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["LTC"]);
		self.Dst_XMRETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["XMR"]);
		self.Dst_QTUMETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["QTUM"]);
		self.Dst_ZECETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["ZEC"]);
		self.Dst_XRPETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["XRP"]);
		self.Dst_DASHETH_Ratio.display(self.exchg.infoB["ETH_Ratio"]["DASH"]);


	def coin_timer(self, mode, count, period):
		#print("Timer option is " + str(mode) + "Period = " + str(period));
		if(mode == "oneshot"):
			self.coin_pricecheck();
		elif (mode == "refresh"):
			i = 0;
			while i < count:
				#print("Timer Call = ", i);
				self.coin_pricecheck();
				time.sleep(period);
				i += 1;
		elif (mode == "infinite"):
			while True:
				self.coin_pricecheck();
				time.sleep(period);
		else:
			print("Timer option error\n");


	def coin_timer_start(self):
	    #threading.Timer(delay, 함수, args=[매개변수,]) - delay초 후에 함수실행
		#timer2 = threading.Timer(10, self.coin_timer, args=['infinite', 5, 10]);
		self.timer = threading.Timer(1, self.coin_timer, args=['infinite', 5, 10]);
		self.timer.start();

	def get_curtime_timer(self, period):
		while True:
			myTime = time.strftime('%H:%M:%S');
			#print(myTime);
			self.cur_time.setText(str(myTime));
			time.sleep(period);

	def get_curtime_start(self):
	    #threading.Timer(delay, 함수, args=[매개변수,]) - delay초 후에 함수실행
		#timer2 = threading.Timer(10, self.coin_timer, args=['infinite', 5, 10]);
		self.timetimer = threading.Timer(1, self.get_curtime_timer, args=[1]);
		self.timetimer.start();


if __name__ == "__main__":
	app = QApplication(sys.argv);
	myWindow = MyWindow();
	myWindow.show();
	app.exec_();


    # Timer 10 sec
	#timer = threading.Thread(name='time', target=coin_timer, args=('infinite', 5, 30));
	#timer.start();



#https://api.binance.com/api//ticker/bookTicker
#https://api.binance.com/api/v1/ticker/24hr
'''

	# Create Thread
	def theradfunc(param1, param2):
		print("==================================");
		print("threadfunc create = ", param1, param2);
		print("==================================");
		pass

	jobb = threading.Thread(name="jobb", target=theradfunc, args=(1, 100000));
	jobb.start();

class bithumb:
    urlTicker = urllib.request.urlopen('https://api.bithumb.com/public/ticker/all')
	headers = { 'User-Agent' : 'Mozilla/5.0' }
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)
    FindBTC = jsonTicker['data']['BTC']['sell_price']
    BTC = int(FindBTC)
    FindETH = jsonTicker['data']['ETH']['sell_price']
    ETH = int(FindETH)
    FindDASH = jsonTicker['data']['DASH']['sell_price']
    DASH = int(FindDASH)
    FindLTC = jsonTicker['data']['LTC']['sell_price']
    LTC = int(FindLTC)
    FindETC = jsonTicker['data']['ETC']['sell_price']
    ETC = int(FindETC)
    FindXRP = jsonTicker['data']['XRP']['sell_price']
    XRP = int(FindXRP)

	if(result["status"] == "0000"):
		#print(result);
		print("status: " + result["status"]);
		print("sell: " + result["data"]["sell_price"]);
		print("buy: " + result["data"]["buy_price"]);
		exchg = Exchange();
		exchg.infoA["Exchange"] = "Bithumb";
		exchg.infoB["Exchange"] = "Binance";
		print(exchg.infoA);
		print(exchg.infoB);


		#print("Binance Price of " + kindofcoine + "\n");
		#ret = connection.get_all_orders(symbol='BNBBTC', requests_params={'timeout': 5});
		#print(ret);
		#ret = connection.get_symbol_info('EOSETH');
		#print(ret);

		print("get_all_tickers\n");
		ret = connection.get_all_tickers();
		print(ret);
		print("\n");

		print("get_symbol_ticker\n");
		ret = connection.get_symbol_ticker(symbol='EOSETH');
		print(ret);
		print("\n");


		#ret = connection.get_exchange_info();
		#print(ret);
		print("\n");
'''
