"""
TradeGate - An algorithmic trading library to use as a gateway to different exchanges.
"""

__version__ = "0.3.2"

from Exchanges import BinanceExchange, BybitExchange, KuCoinExchange


def getCorrectExchange(exchangeName):
    if exchangeName.lower() == 'binance':
        return BinanceExchange.BinanceExchange
    if exchangeName.lower() == 'bybit':
        return BybitExchange.BybitExchange
    if exchangeName.lower() == 'kucoin':
        return KuCoinExchange.KuCoinExchange


class TradeGate:
    def __init__(self, configDict, sandbox=False):
        self.exchangeName = configDict['exchangeName']
        exchangeClass = getCorrectExchange(self.exchangeName)
        if sandbox:
            self.apiKey = configDict['credentials']['test']['spot']['key']
            self.apiSecret = configDict['credentials']['test']['spot']['secret']

            self.exchange = exchangeClass(configDict['credentials']['test'], sandbox=True)
        else:
            self.apiKey = configDict['credentials']['main']['spot']['key']
            self.apiSecret = configDict['credentials']['main']['spot']['secret']

            self.exchange = exchangeClass(configDict['credentials']['main'], sandbox=False)

    def getBalance(self, asset=None, futures=False):
        """ Returns account balance of all assets or a single asset

        :param asset: a valid asset name, defaults to None
        :type asset: str , optional
        :param futures: False for spot market and True for spot market, defaults to False
        :type futures: bool , optional
        :return: Returns a single asset balance or list of assets if no asset was specified.
        :rtype: dict or list(dict)
        :Output with asset specified:

            .. code-block:: python

                {
                    'asset': 'BNB',
                    'free': '1000.00000000',
                    'locked': '0.00000000'
                }

        :Output without asset specified:

            .. code-block:: python

                [
                    {
                        'asset': 'BNB',
                        'free': '1000.00000000',
                        'locked': '0.00000000'
                    },
                    {
                        'asset': 'BTC',
                        'free': '1.02000000',
                        'locked': '0.00000000'
                    },
                    ...
                ]

        """
        return self.exchange.getBalance(asset, futures)

    def createAndTestSpotOrder(self, symbol, side, orderType, quantity=None, price=None, timeInForce=None,
                               stopPrice=None, icebergQty=None, newOrderRespType=None, recvWindow=None,
                               newClientOrderId=None):

        return self.exchange.createAndTestSpotOrder(symbol, side, orderType, quantity, price, timeInForce, stopPrice,
                                                    icebergQty, newOrderRespType, recvWindow, newClientOrderId)

    def makeSpotOrder(self, orderData):
        return self.exchange.makeSpotOrder(orderData)

    def getSymbolOrders(self, symbol, futures=False, orderId=None, startTime=None, endTime=None, limit=None):
        return self.exchange.getSymbolOrders(symbol=symbol, futures=futures, orderId=orderId, startTime=startTime,
                                             endTime=endTime, limit=limit)

    def getOpenOrders(self, symbol, futures=False):
        return self.exchange.getOpenOrders(symbol, futures)

    def getOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        return self.exchange.getOrder(symbol, orderId, localOrderId, futures=futures)

    def cancelAllSymbolOpenOrders(self, symbol, futures=False):
        return self.exchange.cancelAllSymbolOpenOrders(symbol, futures)

    def cancelOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        return self.exchange.cancelOrder(symbol, orderId, localOrderId, futures)

    def getTradingFees(self):
        return self.exchange.getTradingFees()

    def getSymbolTickerPrice(self, symbol, futures=False):
        return self.exchange.getSymbolTickerPrice(symbol, futures)

    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=None, futures=False, blvtnav=False,
                        convertDateTime=False, doClean=False, toCleanDataframe=False):
        return self.exchange.getSymbolKlines(symbol, interval, startTime, endTime, limit, futures, blvtnav,
                                             convertDateTime, doClean, toCleanDataframe)

    def getExchangeTime(self, futures=False):
        return self.exchange.getExchangeTime(futures)

    def createAndTestFuturesOrder(self, symbol, side, orderType, positionSide=None, timeInForce=None, quantity=None,
                                  reduceOnly=None, price=None, newClientOrderId=None,
                                  stopPrice=None, closePosition=None, activationPrice=None, callbackRate=None,
                                  workingType=None, priceProtect=None, newOrderRespType=None,
                                  recvWindow=None, extraParams=None, quoteQuantity=None):

        return self.exchange.createAndTestFuturesOrder(symbol, side, orderType, positionSide, timeInForce,
                                                       quantity, reduceOnly, price, newClientOrderId, stopPrice,
                                                       closePosition, activationPrice, callbackRate, workingType,
                                                       priceProtect, newOrderRespType, recvWindow, extraParams,
                                                       quoteQuantity=quoteQuantity)

    def makeFuturesOrder(self, futuresOrderData):
        return self.exchange.makeFuturesOrder(futuresOrderData)

    def makeBatchFuturesOrder(self, batchOrders):
        return self.exchange.makeBatchFuturesOrder(batchOrders)

    def changeInitialLeverage(self, symbol, leverage):
        return self.exchange.changeInitialLeverage(symbol, leverage)

    def changeMarginType(self, symbol, marginType, params=None):
        return self.exchange.changeMarginType(symbol, marginType, params)

    def changePositionMargin(self, symbol, amount, marginType):
        return self.exchange.changePositionMargin(symbol, amount, marginType)

    def getPosition(self):
        return self.exchange.getPosition()

    def spotBestBidAsks(self, symbol=None):
        return self.exchange.spotBestBidAsks(symbol)

    def getSymbolOrderBook(self, symbol, limit=None, futures=False):
        return self.exchange.getSymbolOrderBook(symbol, limit, futures)

    def getSymbolRecentTrades(self, symbol, limit=None, futures=False):
        return self.exchange.getSymbolRecentTrades(symbol, limit, futures)

    def symbolAccountTradeHistory(self, symbol, futures=False, fromId=None, limit=None):
        return self.exchange.symbolAccountTradeHistory(symbol=symbol, futures=futures, fromId=fromId, limit=limit)

    def makeSlTpLimitFuturesOrder(self, symbol, orderSide, quantity=None, quoteQuantity=None, enterPrice=None,
                                  takeProfit=None, stopLoss=None, leverage=None, marginType=None):
        return self.exchange.makeSlTpLimitFuturesOrder(symbol, orderSide, quantity, quoteQuantity, enterPrice,
                                                       takeProfit, stopLoss, leverage, marginType)

    def makeSlTpMarketFuturesOrder(self, symbol, orderSide, quantity=None, quoteQuantity=None,
                                   takeProfit=None, stopLoss=None, leverage=None, marginType=None):
        return self.exchange.makeSlTpMarketFuturesOrder(symbol, orderSide, quantity, quoteQuantity, takeProfit,
                                                        stopLoss, leverage, marginType)

    def getPositionInfo(self, symbol=None):
        return self.exchange.getPositionInfo(symbol)

    def getSymbolMinTrade(self, symbol, futures=False):
        return self.exchange.getSymbolMinTrade(symbol, futures)

    def getIncomeHistory(self, symbol, incomeType=None, startTime=None, endTime=None, limit=None):
        return self.exchange.getIncomeHistory(symbol, incomeType, startTime, endTime, limit)

    def getSymbolList(self, futures=False):
        """ Returns list of symbol names available for trade

        :param futures: False for spot market and True for spot market, defaults to False
        :type futures: bool , optional
        :return: Returns a list of strings
        :rtype: list(str)
        :Output:

            .. code-block:: python

                [
                    'BTCUSDT',
                    'ETHUSDT',
                    'BCHUSDT',
                    'XRPUSDT',
                    'EOSUSDT',
                    'LTCUSDT',
                    'TRXUSDT',
                    ...
                ]

        """
        return self.exchange.getSymbolList(futures=futures)

    def getSymbol24hChanges(self, futures=False):
        """ Returns all symbols 24-hour change percentages

        :param futures: False for spot market and True for spot market, defaults to False
        :type futures: bool , optional
        :return: Returns a list of tuples containing asset names and percentage of change in 24-hour
        :rtype: list(tuple)
        :Output:

            .. code-block:: python

                [
                    ('PONDUSDT', 28.45),
                    ('PONDBTC', 28.261),
                    ('PONDBUSD', 28.162),
                    ('NULSBTC', 24.321),
                    ('NULSUSDT', 23.975),
                    ('NULSBUSD', 23.244),
                    ('CTXCBTC', 20.551),
                    ('CTXCUSDT', 19.959),
                    ('CTXCBUSD', 19.776),
                    ...
                ]

        """
        return self.exchange.getSymbol24hChanges(futures=futures)

    def getLatestSymbolNames(self, numOfSymbols=None, futures=True):
        """ Returns list of newly added symbols to the exchange. Currently, only working for futures market.

        :param numOfSymbols: Number of symbols returned, sorted for the newest to oldest.
        :type numOfSymbols: int, optional
        :param futures: False for spot market and True for spot market, defaults to False
        :type futures: bool , optional
        :return: Returns a list of tuples containing asset names and a datetime object specifying its listed date.
        :rtype: list(tuple)
        :Output:

            .. code-block:: python

                [
                    ('DOTBUSD', datetime.datetime(2022, 6, 7, 11, 30)),
                    ('TLMBUSD', datetime.datetime(2022, 6, 7, 11, 30)),
                    ('ICPBUSD', datetime.datetime(2022, 6, 7, 11, 30)),
                    ('OPUSDT', datetime.datetime(2022, 6, 1, 11, 30)),
                    ('LUNA2BUSD', datetime.datetime(2022, 5, 31, 11, 30)),
                    ('1000LUNCBUSD', datetime.datetime(2022, 5, 30, 11, 30)),
                    ('GALABUSD', datetime.datetime(2022, 5, 25, 11, 30)),
                    ('TRXBUSD', datetime.datetime(2022, 5, 25, 11, 30)),
                    ('DODOBUSD', datetime.datetime(2022, 5, 24, 11, 30)),
                    ('ANCBUSD', datetime.datetime(2022, 5, 24, 11, 30))
                ]

        """
        return self.exchange.getLatestSymbolNames(numOfSymbols=numOfSymbols, futures=futures)
