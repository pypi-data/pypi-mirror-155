import time
from datetime import datetime

import pandas as pd

from Exchanges.BaseExchange import BaseExchange
from Utils import KuCoinHelpers, DataHelpers
from kucoin.client import User, Trade, Market
from kucoin_futures.client import FuturesUser, FuturesTrade, FuturesMarket


def is_symbol_status_valid(symbolName, symbolDatas, futures=False):
    if futures:
        for symbolData in symbolDatas:
            if symbolData.symbol == symbolName:
                if symbolData.status == 'TRADING':
                    return True
                else:
                    return False
    else:
        for symbolData in symbolDatas:
            if symbolData['symbol'] == symbolName:
                if symbolData['enableTrading']:
                    return True
                else:
                    return False
    return False


def checkSpotOrderDataValid(orderData: DataHelpers.OrderData):
    checkOrderSide(orderData, futures=False)
    checkOrderSymbol(orderData)
    checkOrderType(orderData, futures=False)

    if orderData.orderType == 'market':
        checkOrderSize(orderData)
    else:
        if orderData.orderType == 'limit':
            checkOrderPrice(orderData)
            checkOrderSize(orderData)
        elif orderData.orderType == 'stop':
            checkStopOrderDatas(orderData)

        checkOrderTimeInForce(orderData)
        checkExtraParams(orderData)


def checkFuturesOrderDataValid(orderData):
    checkOrderSide(orderData, futures=True)
    checkOrderSymbol(orderData)
    checkOrderType(orderData, futures=True)

    if orderData.orderType == 'market':
        checkOrderSize(orderData, futures=True)
    elif orderData.orderType == 'limit':
        checkOrderPrice(orderData)
        checkOrderSize(orderData, futures=True)
        checkOrderTimeInForce(orderData, futures=True)
        checkExtraParams(orderData, futures=True)
    if orderData.stopPrice is not None:
        checkStopOrderDatas(orderData, futures=True)


def checkExtraParams(orderData, futures=False):
    if orderData.extraParams is not None:
        if futures:
            checkPostOnlyOrder(orderData, futures)
            checkIceBergOrder(orderData)
            checkOrderLeverage(orderData)
        else:
            checkCancelAfterOrder(orderData)
            checkPostOnlyOrder(orderData, futures)


def checkCancelAfterOrder(orderData):
    if 'cancelAfter' in orderData.extraParams.keys():
        if orderData.timeInForce != 'GTT':
            raise ValueError('\'cancelAfter\' field can only be used with \'GTT\' as \'timeInForce\' field.')


def checkOrderLeverage(orderData):
    if 'leverage' not in orderData.extraParams.keys():
        if orderData.closePosition is None:
            raise ValueError('Missing \'leverage\' field.')
        if not orderData.closePosition:
            raise ValueError('Missing \'leverage\' field.')


def checkIceBergOrder(orderData):
    if 'iceberg' in orderData.extraParams.keys():
        if 'visibleSize' not in orderData.extraParams.keys():
            raise ValueError('Specify \'visibleSize\' with \'iceberg\' set as true')


def checkPostOnlyOrder(orderData, futures=False):
    if 'postOnly' in orderData.extraParams.keys():
        if futures:
            if orderData.timeInForce in ['FOK']:
                raise ValueError('\'postOnly\' field can not be used with \'IOC\' as \'timeInForce\' field.')
            if 'hidden' in orderData.extraParams.keys():
                raise ValueError('Can\'t use \'hidden\' with \'postOnly\'')
            if 'iceberg' in orderData.extraParams.keys():
                raise ValueError('Can\'t use \'iceberg\' with \'postOnly\'')
        else:
            if orderData.timeInForce in ['IOC', 'FOK']:
                raise ValueError(
                    '\'postOnly\' field can not be used with \'IOC\' or \'FOK\' as \'timeInForce\' field.')


def checkOrderTimeInForce(orderData, futures=False):
    errorString = 'Invalid value for \'timeInForce\' specified'

    if futures:
        validValues = ['GTC', 'IOC']
    else:
        validValues = ['GTC', 'GTT', 'IOC', 'FOK']

    if orderData.timeInForce not in validValues:
        raise ValueError(errorString)


def checkOrderPrice(orderData):
    if orderData.price is None:
        raise ValueError('Missing \'price\' field for limit order type.')


def checkStopOrderDatas(orderData, futures=False):
    if futures:
        if 'stop' not in orderData.extraParams.keys():
            raise ValueError('Specify \'stop\' inside \'extraParams\'. Either \'down\' or \'up\'.')
        if 'stopPriceType' not in orderData.extraParams.keys():
            raise ValueError('Specify \'stopPriceType\' inside \'extraParams\'. Either \'TP\', \'IP\' or \'MP\'.')
    else:
        if orderData.extraParams is not None:
            if 'stopPrice' not in orderData.extraParams.keys():
                raise ValueError('Specify \'stopPrice\' in \'extraParams\' for stop order.')
        else:
            raise ValueError('Specify \'stopPrice\' in \'extraParams\' for stop order.')

        if orderData.quantity is None:
            raise ValueError('Missing \'quantity\' field for stop order type.')


def checkOrderSize(orderData, futures=False):
    errorString = 'Provide either \'quantity\' or \'quoteOrderQty\'.'
    if futures:
        if orderData.quantity is None and orderData.quoteQuantity is None:
            if orderData.closePosition is None:
                raise ValueError(errorString)
            if not orderData.closePosition:
                raise ValueError(errorString)
    else:
        if orderData.quantity is None and orderData.quoteOrderQty is None:
            raise ValueError(errorString)


def checkOrderType(orderData, futures=False):
    if futures:
        validTypes = ['limit', 'market', 'LIMIT', 'MARKET', 'Limit', 'Market']
    else:
        validTypes = ['limit', 'market', 'stop', 'LIMIT', 'MARKET', 'STOP', 'Limit', 'Market', 'Stop']

    if orderData.orderType is None or orderData.orderType not in validTypes:
        raise ValueError('Missing \'type\' field.')
    orderData.orderType = orderData.orderType.lower()


def checkOrderSymbol(orderData):
    if orderData.symbol is None:
        raise ValueError('Missing \'symbol\' field.')


def checkOrderSide(orderData, futures=False):
    errorString = 'Missing or incorrect \'side\' field.'
    if futures:
        if orderData.side is None or orderData.side not in ['buy', 'sell', 'BUY', 'SELL', 'Buy', 'Sell']:
            if orderData.closePosition is None:
                raise ValueError(errorString)
            if not orderData.closePosition:
                raise ValueError(errorString)
        if orderData.side is not None:
            orderData.side = orderData.side.lower()
    else:
        if orderData.side is None or orderData.side not in ['buy', 'sell', 'BUY', 'SELL', 'Buy', 'Sell']:
            raise ValueError(errorString)
        orderData.side = orderData.side.lower()


class KuCoinExchange(BaseExchange):
    timeIntervals = ['1min', '3min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '8hour', '12hour',
                     '1day', '1week']

    timeIntervalTranslate = {'1m': '1min', '3m': '3min', '5m': '5min', '15m': '15min', '30m': '30min', '1h': '1hour',
                             '2h': '2hour', '4h': '4hour', '6h': '6hour', '8h': '8hour', '12h': '12hour', '1d': '1day',
                             '1w': '1week'}

    noOrderIdsErrorString = 'Specify either \'orderId\' or \'localOrderId\' (only for active orders)'

    def __init__(self, credentials, sandbox=False, unifiedInOuts=True):
        self.spotApiKey = credentials['spot']['key']
        self.spotSecret = credentials['spot']['secret']
        self.spotPassphrase = credentials['spot']['passphrase']

        self.futuresApiKey = credentials['futures']['key']
        self.futuresSecret = credentials['futures']['secret']
        self.futuresPassphrase = credentials['futures']['passphrase']

        self.sandbox = sandbox
        self.unifiedInOuts = unifiedInOuts

        self.unavailableErrorText = 'This method is unavailable in KuCoin exchange'

        if sandbox:
            self.spotUser = User(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase,
                                 is_sandbox=True)
            self.spotTrade = Trade(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase,
                                   is_sandbox=True)
            self.spotMarket = Market(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase,
                                     is_sandbox=True)

            self.futuresUser = FuturesUser(key=self.futuresApiKey, secret=self.futuresSecret,
                                           passphrase=self.futuresPassphrase, is_sandbox=True)
            self.futuresTrade = FuturesTrade(key=self.futuresApiKey, secret=self.futuresSecret,
                                             passphrase=self.futuresPassphrase, is_sandbox=True)
            self.futuresMarket = FuturesMarket(key=self.futuresApiKey, secret=self.futuresSecret,
                                               passphrase=self.futuresPassphrase, is_sandbox=True)
        else:
            self.spotUser = User(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase)
            self.spotTrade = Trade(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase)
            self.spotMarket = Market(key=self.spotApiKey, secret=self.spotSecret, passphrase=self.spotPassphrase)

            self.futuresUser = FuturesUser(key=self.futuresApiKey, secret=self.futuresSecret,
                                           passphrase=self.futuresPassphrase)
            self.futuresTrade = FuturesTrade(key=self.futuresApiKey, secret=self.futuresSecret,
                                             passphrase=self.futuresPassphrase)
            self.futuresMarket = FuturesMarket(key=self.futuresApiKey, secret=self.futuresSecret,
                                               passphrase=self.futuresPassphrase)

    def getBalance(self, asset=None, futures=False):
        if futures:
            if asset is None:
                return KuCoinHelpers.unifyGetBalanceFuturesOut([self.futuresUser.get_account_overview(),
                                                                self.futuresUser.get_account_overview(currency='USDT')])
            else:
                return KuCoinHelpers.unifyGetBalanceFuturesOut(
                    self.futuresUser.get_account_overview(currency=asset), isSingle=True)

        else:
            if asset is None:
                return KuCoinHelpers.unifyGetBalanceSpotOut(self.spotUser.get_account_list(currency=asset))
            else:
                return KuCoinHelpers.unifyGetBalanceSpotOut(self.spotUser.get_account_list(currency=asset),
                                                            isSingle=True)

    def symbolAccountTradeHistory(self, symbol, futures=False, fromId=None, limit=None):
        if futures:
            return KuCoinHelpers.unifyTradeHistory(self.futuresTrade.get_fills_details(symbol=symbol)['items'],
                                                   futures=True)
        else:

            return KuCoinHelpers.unifyTradeHistory(self.spotTrade.get_fill_list(tradeType='TRADE')['items'])

    def testSpotOrder(self, orderData):
        checkSpotOrderDataValid(orderData)
        return orderData

    def makeSpotOrder(self, orderData):
        params = KuCoinHelpers.getSpotOrderAsDict(orderData)
        response = None

        if params['type'] == 'market':
            response = self.spotTrade.create_market_order(**params)
        if params['type'] == 'limit':
            response = self.spotTrade.create_limit_order(**params)
        if params['type'] == 'stop' and 'price' in params.keys():
            response = self.spotTrade.create_limit_stop_order(**params)
        if params['type'] == 'stop' and 'price' not in params.keys():
            response = self.spotTrade.create_market_stop_order(**params)

        return self.getOrder(params['symbol'], orderId=response['orderId'], futures=False)

    def createAndTestSpotOrder(self, symbol, side, orderType, quantity=None, price=None, timeInForce=None,
                               stopPrice=None, icebergQty=None, newOrderRespType=None, recvWindow=None,
                               newClientOrderId=None):
        currOrder = DataHelpers.setSpotOrderData(icebergQty, newClientOrderId, newOrderRespType, orderType, price,
                                                 quantity, recvWindow, side, stopPrice, symbol, timeInForce)

        self.testSpotOrder(currOrder)

        return currOrder

    def getSymbolOrders(self, symbol, futures=False, orderId=None, startTime=None, endTime=None, limit=None):
        if futures:
            args = {}
            if startTime is not None:
                args['startAt'] = startTime
            if endTime is not None:
                args['endAt'] = endTime
            args['symbol'] = symbol
            orderList = self.futuresTrade.get_order_list(**args)['items']
            return KuCoinHelpers.unifyGetSymbolOrders(orderList, futures=True)
        else:
            args = {}
            if startTime is not None:
                args['startAt'] = startTime
            if endTime is not None:
                args['endAt'] = endTime
            args['symbol'] = symbol
            orderList = self.spotTrade.get_order_list(**args)['items']
            return KuCoinHelpers.unifyGetSymbolOrders(orderList)

    def getOpenOrders(self, symbol, futures=False):
        args = {'symbol': symbol, 'status': 'active'}
        if futures:
            lotSize = self.getSymbolMinTrade(symbol=symbol, futures=True)['precisionStep']
            orderList = self.futuresTrade.get_order_list(**args)['items']
            return KuCoinHelpers.unifyGetSymbolOrders(orderList, futures=True, lotSize=lotSize)
        else:
            orderList = self.spotTrade.get_order_list(**args)['items']
            return KuCoinHelpers.unifyGetSymbolOrders(orderList)

    def cancelAllSymbolOpenOrders(self, symbol, futures=False):
        if futures:
            result = self.futuresTrade.cancel_all_limit_order(symbol)['cancelledOrderIds']
            result.append(self.futuresTrade.cancel_all_stop_order(symbol)['cancelledOrderIds'])
            return result
        else:
            args = {'symbol': symbol}
            result = self.spotTrade.cancel_all_orders(**args)
            return result['cancelledOrderIds']

    def cancelOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        if futures:
            if orderId is not None:
                cancelledOrderId = self.futuresTrade.cancel_order(orderId)['cancelledOrderIds'][0]
            elif localOrderId is not None:
                orderData = self.getOrder(symbol=symbol, localOrderId=localOrderId, futures=True)
                cancelledOrderId = self.futuresTrade.cancel_order(orderId=orderData['orderId'])['cancelledOrderIds'][0]
            else:
                raise ValueError(self.noOrderIdsErrorString)
            return self.getOrder(symbol, orderId=cancelledOrderId, futures=True)
        else:
            if orderId is not None:
                cancelledOrderId = self.spotTrade.cancel_order(orderId)['cancelledOrderIds'][0]
            elif localOrderId is not None:
                cancelledOrderId = self.spotTrade.cancel_client_order(localOrderId)['cancelledOrderId']
            else:
                raise ValueError(self.noOrderIdsErrorString)
            return self.getOrder(symbol, orderId=cancelledOrderId, futures=False)

    def getOrder(self, symbol, orderId=None, localOrderId=None, futures=False):
        if futures:
            if orderId is not None:
                orderData = self.futuresTrade.get_order_details(orderId)
            elif localOrderId is not None:
                orderData = self.futuresTrade.get_client_order_details(localOrderId)
            else:
                raise ValueError(self.noOrderIdsErrorString)

            lotSize = self.getSymbolMinTrade(symbol=symbol, futures=True)['precisionStep']
            return KuCoinHelpers.unifyGetOrder(orderData, futures=True, lotSize=lotSize)
        else:
            if orderId is not None:
                orderData = self.spotTrade.get_order_details(orderId)
            elif localOrderId is not None:
                orderData = self.spotTrade.get_client_order_details(localOrderId)
            else:
                raise ValueError(self.noOrderIdsErrorString)

            return KuCoinHelpers.unifyGetOrder(orderData)

    def getTradingFees(self, symbol=None, futures=False):
        if futures:
            if symbol is None:
                raise ValueError('Must specify futures contract symbol name.')
            contractInfo = self.futuresMarket.get_contract_detail(symbol=symbol)
            return {
                'symbol': contractInfo['symbol'],
                'takerFeeRate': contractInfo['takerFeeRate'],
                'makerFeeRate': contractInfo['makerFeeRate']
            }
        else:
            if symbol is None:
                return self.spotUser.get_base_fee()['data']
            else:
                return self.spotUser.get_actual_fee(symbols=[symbol])['data']

    def getSymbolTickerPrice(self, symbol, futures=False):
        if futures:
            return float(self.futuresMarket.get_ticker(symbol=symbol)['price'])
        else:
            return float(self.spotMarket.get_ticker(symbol=symbol)['price'])

    def getSymbolKlines(self, symbol, interval, startTime=None, endTime=None, limit=500, futures=False, blvtnav=False,
                        convertDateTime=False, doClean=False, toCleanDataframe=False):
        if interval not in KuCoinExchange.timeIntervals:
            if interval in KuCoinExchange.timeIntervalTranslate.keys():
                timeInterval = KuCoinExchange.timeIntervalTranslate[interval]
            else:
                raise ValueError('Time interval is not valid.')
        else:
            timeInterval = interval

        if startTime is not None and not isinstance(startTime, int):
            startTime = int(datetime.timestamp(datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')))
        if endTime is not None and not isinstance(endTime, int):
            endTime = int(datetime.timestamp(datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')))

        if futures:
            data = self._getFuturesSymbolKlines(endTime, timeInterval, limit, startTime, symbol)
        else:
            data = self._getSpotSymbolKlines(endTime, timeInterval, limit, startTime, symbol)

        if convertDateTime or toCleanDataframe:
            if futures:
                for datum in data:
                    datum.append(datum[-1])
                    datum[-1] = datetime.fromtimestamp((float(datum[0]) - 1) / 1000)
                    datum[0] = datetime.fromtimestamp(float(datum[0]) / 1000)
                    datum.append(None)
            else:
                for datum in data:
                    datum.append(datum[-1])
                    datum[-2] = datetime.fromtimestamp(float(datum[0]) - 1)
                    datum[0] = datetime.fromtimestamp(float(datum[0]))

        if doClean or toCleanDataframe:
            if toCleanDataframe:
                cleanDataFrame = pd.DataFrame(data, columns=['date', 'open', 'close', 'high', 'low', 'volume',
                                                             'closeDate', 'tradesNum'])
                cleanDataFrame.set_index('date', inplace=True)
                cleanDataFrame[cleanDataFrame.columns[:5]] = cleanDataFrame[cleanDataFrame.columns[:5]].apply(
                    pd.to_numeric, errors='coerce')
                cleanDataFrame[cleanDataFrame.columns[-1]] = cleanDataFrame[cleanDataFrame.columns[-1]].apply(
                    pd.to_numeric, errors='coerce')
                return cleanDataFrame
            return data
        else:
            return data

    def _getSpotSymbolKlines(self, endTime, timeInterval, limit, startTime, symbol):
        if limit is None:
            if startTime is None:
                if endTime is None:
                    data = self.spotMarket.get_kline(symbol=symbol, kline_type=timeInterval)
                else:
                    raise ValueError('Can\'t use endTime without limit.')
            else:
                if endTime is None:
                    data = self.spotMarket.get_kline(symbol=symbol, kline_type=timeInterval, startAt=startTime)
                else:
                    data = self.spotMarket.get_kline(symbol=symbol, kline_type=timeInterval, startAt=startTime,
                                                     endAt=endTime)
        else:
            if startTime is None:
                if endTime is None:
                    startAt = int(time.time()) - limit * self._getTimeIntervalInSeconds(timeInterval)
                    data = self.spotMarket.get_kline(symbol=symbol, kline_type=timeInterval, startAt=startAt,
                                                     endAt=int(time.time()))
                else:
                    startAt = endTime - limit * self._getTimeIntervalInSeconds(timeInterval)
                    data = self.spotMarket.get_kline(symbol=symbol, kline_type=timeInterval, startAt=startAt,
                                                     endAt=endTime)
            else:
                if endTime is None:
                    endAt = startTime + limit * self._getTimeIntervalInSeconds(timeInterval)
                    data = self.spotMarket.get_kline(symbol=symbol, kline_type=timeInterval, startAt=startTime,
                                                     endAt=endAt)
                else:
                    data = self.spotMarket.get_kline(symbol=symbol, kline_type=timeInterval, startAt=startTime,
                                                     endAt=endTime)
        return data[::-1]

    def _getFuturesSymbolKlines(self, endTime, timeInterval, limit, startTime, symbol):
        granularity = int(self._getTimeIntervalInSeconds(timeInterval) / 60)
        if limit is None:
            if startTime is None:
                if endTime is None:
                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity)
                else:
                    endTime = endTime - endTime % (granularity * 60)
                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity,
                                                             end_t=endTime * 1000)
            else:
                if endTime is None:
                    startTime = startTime - startTime % (granularity * 60)
                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity,
                                                             begin_t=startTime * 1000)
                else:
                    endTime = endTime - endTime % (granularity * 60)
                    startTime = startTime - startTime % (granularity * 60)

                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity,
                                                             begin_t=startTime * 1000, end_t=endTime * 1000)
        else:
            if startTime is None:
                if endTime is None:
                    endTime = int(time.time())
                    endTime = endTime - endTime % (granularity * 60)

                    startAt = endTime - limit * granularity * 60
                    startAt = startAt - startAt % (granularity * 60)

                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity,
                                                             begin_t=startAt * 1000)
                else:
                    endTime = endTime - endTime % (granularity * 60)

                    startTime = endTime - limit * granularity * 60
                    startTime = startTime - startTime % (granularity * 60)

                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity,
                                                             begin_t=startTime * 1000, end_t=endTime * 1000)
            else:
                if endTime is None:
                    startTime = startTime - startTime % (granularity * 60)

                    endTime = startTime + limit * granularity * 60
                    endTime = endTime - endTime % (granularity * 60)

                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity,
                                                             begin_t=startTime * 1000, end_t=endTime * 1000)
                else:
                    startTime = startTime - startTime % (granularity * 60)
                    endTime = endTime - endTime % (granularity * 60)

                    data = self.futuresMarket.get_kline_data(symbol=symbol, granularity=granularity,
                                                             begin_t=startTime * 1000, end_t=endTime * 1000)
        return data

    def _getTimeIntervalInSeconds(self, timeInterval):
        if timeInterval not in self.timeIntervals:
            raise ValueError('Time interval is not valid.')

        if timeInterval == '1min':
            return 60
        elif timeInterval == '3min':
            return 3 * 60
        elif timeInterval == '5min':
            return 5 * 60
        elif timeInterval == '15min':
            return 15 * 60
        elif timeInterval == '30min':
            return 40 * 60
        elif timeInterval == '1hour':
            return 3600
        elif timeInterval == '2hour':
            return 2 * 3600
        elif timeInterval == '4hour':
            return 4 * 3600
        elif timeInterval == '6hour':
            return 6 * 3600
        elif timeInterval == '8hour':
            return 8 * 3600
        elif timeInterval == '12hour':
            return 12 * 3600
        elif timeInterval == '1day':
            return 24 * 3600
        elif timeInterval == '1week':
            return 7 * 24 * 3600

    def getExchangeTime(self, futures=False):
        if futures:
            return self.futuresMarket.get_server_timestamp()
        else:
            return self.spotMarket.get_server_timestamp()

    def getSymbol24hTicker(self, symbol):
        return self.spotMarket.get_24h_stats(symbol)

    def testFuturesOrder(self, futuresOrderData):
        checkFuturesOrderDataValid(futuresOrderData)

    def makeFuturesOrder(self, futuresOrderData):
        if futuresOrderData.quantity is None:
            if futuresOrderData.quoteQuantity is not None:
                lotSize = self.getSymbolMinTrade(symbol=futuresOrderData.symbol, futures=True)['precisionStep']
                if futuresOrderData.price is None:
                    currPrice = self.getSymbolTickerPrice(futuresOrderData.symbol, futures=True)
                    futuresOrderData.quantity = int(round(futuresOrderData.quoteQuantity / currPrice / lotSize))
                else:
                    futuresOrderData.quantity = int(
                        round(futuresOrderData.quoteQuantity / futuresOrderData.price / lotSize))

        params = KuCoinHelpers.getFuturesOrderAsDict(futuresOrderData)

        symbol = params['symbol']
        del params['symbol']

        side = params['side']
        del params['side']

        if 'leverage' in params.keys():
            leverage = params['leverage']
            del params['leverage']
        else:
            leverage = None
        if params['type'] == 'market':
            result = self.futuresTrade.create_market_order(symbol, side, leverage, **params)
        elif params['type'] == 'limit':
            size = params['size']
            del params['size']

            price = params['price']
            del params['price']

            result = self.futuresTrade.create_limit_order(symbol, side, leverage, size, price, **params)
        else:
            result = None
        return self.getOrder(symbol, orderId=result['orderId'], futures=True)

    def createAndTestFuturesOrder(self, symbol, side, orderType, positionSide=None, timeInForce=None, quantity=None,
                                  reduceOnly=None, price=None, newClientOrderId=None,
                                  stopPrice=None, closePosition=None, activationPrice=None, callbackRate=None,
                                  workingType=None, priceProtect=None, newOrderRespType=None,
                                  recvWindow=None, extraParams=None, quoteQuantity=None):
        currOrder = DataHelpers.setFuturesOrderData(activationPrice, callbackRate, closePosition, extraParams,
                                                    newClientOrderId, newOrderRespType, orderType, positionSide, price,
                                                    priceProtect, quantity, recvWindow, reduceOnly, side, stopPrice,
                                                    symbol, timeInForce, workingType, quoteQuantity)

        lotSize = self.getSymbolMinTrade(symbol=symbol, futures=True)['precisionStep']
        if currOrder.quantity is not None:
            currOrder.quantity /= lotSize

        self.testFuturesOrder(currOrder)

        return currOrder

    def makeBatchFuturesOrder(self, futuresOrderDatas):
        raise NotImplementedError(self.unavailableErrorText)

    def changeInitialLeverage(self, symbol, leverage):
        raise NotImplementedError(self.unavailableErrorText)

    def changeMarginType(self, symbol, marginType, params):
        raise NotImplementedError(self.unavailableErrorText)

    def changePositionMargin(self, symbol, amount, marginType=None):
        enResult = self.futuresTrade.modify_auto_deposit_margin(symbol, True)
        if not enResult['data']:
            raise RuntimeError('Could not modify margin.')
        newPosition = self.futuresTrade.add_margin_manually(symbol=symbol, margin=amount, bizNo=str(time.time()))

        return KuCoinHelpers.unifyGetPositionInfo(newPosition)

    def getPosition(self):
        return self.futuresTrade.get_all_position()

    def spotBestBidAsks(self, symbol):
        tickerData = self.spotMarket.get_ticker(symbol)
        return KuCoinHelpers.unifyGetBestBidAsks(tickerData, symbol)

    def getSymbolOrderBook(self, symbol, limit=None, futures=False):
        if futures:
            orderBook = self.futuresMarket.l2_order_book(symbol)
            return orderBook
        else:
            orderBook = self.spotMarket.get_aggregated_order(symbol)
            return orderBook

    def getSymbolRecentTrades(self, symbol, limit=None, futures=False):
        if futures:
            tradeHistory = self.futuresMarket.get_trade_history(symbol=symbol)
            return pd.DataFrame(KuCoinHelpers.unifyRecentTrades(tradeHistory, futures=True))
        else:
            tradeHistory = self.spotMarket.get_trade_histories(symbol=symbol)
            return pd.DataFrame(KuCoinHelpers.unifyRecentTrades(tradeHistory))

    def getPositionInfo(self, symbol=None):
        if symbol is None:
            positionInfos = self.futuresTrade.get_all_position()
            return KuCoinHelpers.unifyGetPositionInfos(positionInfos)
        else:
            positionInfo = self.futuresTrade.get_position_details(symbol=symbol)
            return [KuCoinHelpers.unifyGetPositionInfo(positionInfo)]

    def getSymbolMinTrade(self, symbol, futures=False):
        if futures:
            contractInfos = self.futuresMarket.get_contract_detail(symbol)
            return KuCoinHelpers.unifyMinTrade(contractInfos, futures=True)
        else:
            symbolInfoList = self.spotMarket.get_symbol_list()

            symbolInfo = None
            for info in symbolInfoList:
                if info['symbol'] == symbol:
                    symbolInfo = info
            return KuCoinHelpers.unifyMinTrade(symbolInfo)

    def makeSlTpLimitFuturesOrder(self, symbol, orderSide, quantity=None, quoteQuantity=None, enterPrice=None,
                                  takeProfit=None, stopLoss=None, leverage=None, marginType=None):
        symbolInfo = self.getSymbolMinTrade(symbol=symbol, futures=True)

        if quantity is None:
            if quoteQuantity is None:
                raise ValueError('Specify either quantity or quoteQuantity')
            quantity = int(quoteQuantity / enterPrice / symbolInfo['precisionStep']) * symbolInfo['precisionStep']

        if quantity < symbolInfo['minQuantity']:
            raise ValueError('Quantity is lower than minimum quantity allowed.')

        mainOrder = self.createAndTestFuturesOrder(symbol, orderSide.upper(), 'LIMIT', quantity=quantity,
                                                   price=enterPrice, timeInForce='GTC',
                                                   extraParams={'leverage': leverage})

        tpSlSide = 'sell' if orderSide.upper() == 'BUY' else 'buy'

        slExtraParams = {
            'stop': 'down' if orderSide.upper() == 'BUY' else 'up',
            'stopPriceType': 'TP'
        }
        stopLossOrder = self.createAndTestFuturesOrder(symbol=symbol, side=tpSlSide, orderType='MARKET',
                                                       stopPrice=stopLoss, closePosition=True,
                                                       timeInForce='GTC', extraParams=slExtraParams)

        tpExtraParams = {
            'stop': 'up' if orderSide.upper() == 'BUY' else 'down',
            'stopPriceType': 'TP'
        }
        takeProfitOrder = self.createAndTestFuturesOrder(symbol=symbol, side=tpSlSide, orderType='MARKET',
                                                         stopPrice=takeProfit, closePosition=True,
                                                         timeInForce='GTC', extraParams=tpExtraParams)

        mainOrderRes = self.makeFuturesOrder(mainOrder)
        slOrderRes = self.makeFuturesOrder(stopLossOrder)
        tpOrderRes = self.makeFuturesOrder(takeProfitOrder)

        orderIds = {
            'mainOrder': mainOrderRes['orderId'],
            'stopLoss': slOrderRes['orderId'],
            'takeProfit': tpOrderRes['orderId']
        }

        return orderIds

    def getSymbol24hChanges(self, futures=False):
        changesList = []
        if futures:
            for ticker in self.futuresMarket.get_contracts_list():
                if ticker['status'] == 'Open':
                    changesList.append((ticker['symbol'], float(ticker['priceChgPct']) * 100))
        else:
            symbolInfos = self.spotMarket.get_symbol_list()
            for ticker in self.spotMarket.get_all_tickers()['ticker']:
                if is_symbol_status_valid(ticker['symbol'], symbolInfos, futures=False):
                    changesList.append((ticker['symbol'], float(ticker['changeRate']) * 100))

        return sorted(changesList, key=lambda x: x[1], reverse=True)

    def getSymbolList(self, futures=False):
        symbolNames = []
        if futures:
            for ticker in self.futuresMarket.get_contracts_list():
                symbolNames.append(ticker['symbol'])
        else:
            for ticker in self.spotMarket.get_all_tickers()['ticker']:
                symbolNames.append(ticker['symbol'])

        return symbolNames

    def getLatestSymbolNames(self, numOfSymbols=None, futures=False):
        symbolDatas = []
        if futures:
            for symbolInfo in self.futuresMarket.get_contracts_list():
                symbolDatas.append(
                    (symbolInfo['symbol'], datetime.fromtimestamp(float(symbolInfo['firstOpenDate']) / 1000)))
                symbolDatas.sort(key=lambda x: x[1], reverse=True)
            if numOfSymbols is not None and numOfSymbols > len(symbolDatas):
                numOfSymbols = len(symbolDatas)
        else:
            raise NotImplementedError()
        return symbolDatas[:numOfSymbols]
