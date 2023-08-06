import json
import logging
import time

import pytest

from TradeGates.TradeGate import TradeGate

loglevel = logging.INFO
logging.basicConfig(level=loglevel)
log = logging.getLogger(__name__)


@pytest.fixture
def getGatesAndSymbolNames():
    gates = []
    symbolNames = {}
    with open('../config.json') as f:
        config = json.load(f)

    for key in config.keys():
        gates.append(TradeGate(config[key], sandbox=True))
        if gates[-1].exchangeName.lower() == 'kucoin':
            symbolNames[gates[-1].exchangeName] = 'XBTUSDTM'
        else:
            symbolNames[gates[-1].exchangeName] = 'BTCUSDT'

    return gates, symbolNames


def testSymbolFuturesOrders(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        symbolFutureOrders = gate.getSymbolOrders(symbolName, futures=True)
        # print('\nSymbol future orders from {} exchange: {}'.format(gate.exchangeName, symbolFutureOrders))
        assert symbolFutureOrders is not None, 'Problem in futures order list from {} exchange.'.format(
            gate.exchangeName)


def testFuturesBalance(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        balance = gate.getBalance(futures=True)
        # print('\nFutures balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Problem in futures balance from {} exchange.'.format(gate.exchangeName)

        try:
            if gate.exchangeName != 'Binance':
                if sorted(list(balance[0].keys())) != sorted(['asset', 'free', 'locked', 'exchangeSpecific']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
            else:
                if sorted(list(balance[0].keys())) != sorted(['asset', 'free', 'locked']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
        except:
            assert False, 'Bad fetch single coin balance interface for {} exchange,'.format(gate.exchangeName)


def testFuturesSingleCoinBalance(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        balance = gate.getBalance('USDT', futures=True)
        # print('\nUSDT Futures balance from {} exchange: {}'.format(gate.exchangeName, balance))
        assert balance is not None, 'Problem in fetching futures single coin balance from {} exchange.'.format(
            gate.exchangeName)

        try:
            if gate.exchangeName != 'Binance':
                if sorted(list(balance.keys())) != sorted(['asset', 'free', 'locked', 'exchangeSpecific']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
            else:
                if sorted(list(balance.keys())) != sorted(['asset', 'free', 'locked']):
                    assert False, 'Bad fetch balance interface for {} exchange,'.format(gate.exchangeName)
        except:
            assert False, 'Bad fetch single coin balance interface for {} exchange,'.format(gate.exchangeName)


def testCreatingFuturesOrder(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        if gate.exchangeName.lower() == 'kucoin':
            extraParams = {'leverage': 5}
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'MARKET', quantity=0.002,
                                                              extraParams=extraParams)
        else:
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'MARKET', quantity=0.002)
        # print('\nTest creating futures order in {} exchange: {}'.format(gate.exchangeName, futuresOrderData))
        assert futuresOrderData is not None, 'Problem in creating futures order in {} exchange.'.format(
            gate.exchangeName)


def testFuturesOrder(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        if gate.exchangeName.lower() == 'kucoin':
            extraParams = {'leverage': 5}
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'MARKET', quantity=0.002,
                                                              extraParams=extraParams)
        else:
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'MARKET', quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)
        print('\nFuture ordering in {} exchange: {}'.format(gate.exchangeName, result))
        assert result is not None, 'Problem in submitting futures order in {} exchange.'.format(gate.exchangeName)


def testBatchFuturesOrders(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        if gate.exchangeName.lower() == 'kucoin':
            continue
        symbolName = symbolNamesDict[gate.exchangeName]
        try:
            verifiedOrders = [gate.createAndTestFuturesOrder(symbolName, 'BUY', 'MARKET', quantity=0.1),
                              gate.createAndTestFuturesOrder(symbolName, 'BUY', 'MARKET', quantity=0.2),
                              gate.createAndTestFuturesOrder(symbolName, 'BUY', 'MARKET', quantity=0.3)]

            result = gate.makeBatchFuturesOrder(verifiedOrders)
            # print('\nResult of batch ordering from {} exchange: {}'.format(gate.exchangeName, result))
            assert result is not None, 'Problem in making new order in {} exchange'.format(gate.exchangeName)
        except Exception:
            assert False, 'Problem in making new order in {} exchange'.format(gate.exchangeName)


# @pytest.mark.skip(reason="For Special Purposes")
def testFuturesTpSlLimitOrder(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        if gate.exchangeName.lower() != 'kucoin':
            continue
        try:
            result = gate.makeSlTpLimitFuturesOrder(symbol=symbolName, orderSide='BUY',
                                                    quantity=0.002, enterPrice=20500, takeProfit=21500,
                                                    stopLoss=20000, leverage=10, marginType='ISOLATED')
            # print('\nResult of TP-SL-Limit ordering from {} exchange: {}'.format(gate.exchangeName, result))
            assert result is not None, 'Problem in making new order in {} exchange'.format(gate.exchangeName)
        except Exception:
            assert False, 'Problem in making new SL-TP-Limit order in {} exchange'.format(gate.exchangeName)


def testFuturesTpSlMarketOrder(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        if gate.exchangeName.lower() != 'binance':
            continue
        try:
            result = gate.makeSlTpMarketFuturesOrder(symbol=symbolName, orderSide='BUY', quantity=None,
                                                     quoteQuantity=40,
                                                     takeProfit=47000, stopLoss=45000, leverage=10,
                                                     marginType='ISOLATED')
            print('\nResult of TP-SL-Market ordering from {} exchange: {}'.format(gate.exchangeName, result))
            assert result is not None, 'Problem in making new order in {} exchange'.format(gate.exchangeName)
        except Exception:
            assert False, 'Problem in making new SL-TP-Limit order in {} exchange'.format(gate.exchangeName)


def testGetFuturesOpenOrders(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        symbolOpenOrders = gate.getOpenOrders(symbolName, futures=True)

        print('\n\'BTCUSDT\' open orders from {} exchange: {}'.format(gate.exchangeName, symbolOpenOrders))

        assert symbolOpenOrders is not None, \
            'Problem in getting list of open orders with symbol from {} exchange.'.format(gate.exchangeName)


def testGetPositionInformation(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        openPosition = gate.getPositionInfo(symbolName)

        print('\nOpen position information from {} exchange: {}'.format(gate.exchangeName, openPosition))

        assert openPosition is not None, 'Problem in getting position information without symbol from {} exchange.'.format(
            gate.exchangeName)


def testGetFuturesOrder(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        if gate.exchangeName.lower() == 'bybit':
            continue
        symbolName = symbolNamesDict[gate.exchangeName]
        if gate.exchangeName.lower() == 'kucoin':
            extraParams = {'leverage': 5}
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=20, extraParams=extraParams)
        else:
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=0.002)
        result = gate.makeFuturesOrder(futuresOrderData)
        order = gate.getOrder(symbolName, orderId=result['orderId'], futures=True)

        # print('\nOrder data fetched from {} exchange: {}'.format(gate.exchangeName, order))

        assert order['clientOrderId'] == result[
            'clientOrderId'], 'Futures fetch client orderID is not equal to the actual client orderID from {} exchange.'.format(
            gate.exchangeName)

        order = gate.getOrder(symbolName, localOrderId=result['clientOrderId'], futures=True)
        assert order['orderId'] == result[
            'orderId'], 'Futures fetch orderID is not equal to the actual orderID from {} exchange.'.format(
            gate.exchangeName)


def testCancelingAllFuturesOpenOrders(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        if gate.exchangeName.lower() == 'kucoin':
            extraParams = {'leverage': 5}
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=20, extraParams=extraParams)
        else:
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=0.002)
        gate.makeFuturesOrder(futuresOrderData)

        gate.cancelAllSymbolOpenOrders(symbolName, futures=True)

        openOrders = gate.getOpenOrders(symbolName, futures=True)
        assert len(openOrders) == 0, 'Problem in canceling all Open Orders in {} exchange.'.format(gate.exchangeName)


def testCancelingOrder(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        if gate.exchangeName.lower() == 'kucoin':
            extraParams = {'leverage': 5}
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=20, extraParams=extraParams,
                                                              newClientOrderId=str(int(time.time())))
        else:
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=0.002,
                                                              newClientOrderId=str(int(time.time())))

        result = gate.makeFuturesOrder(futuresOrderData)

        gate.cancelOrder(symbol=symbolName, orderId=result['orderId'], futures=True)

        result = gate.getOrder(symbol=symbolName, localOrderId=result['clientOrderId'], futures=True)
        assert result['status'].lower() in ['canceled', 'cancelled'], \
            'Problem in canceling specified open order by orderId from {} exchange.'.format(gate.exchangeName)

        if gate.exchangeName.lower() == 'kucoin':
            extraParams = {'leverage': 5}
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=20, extraParams=extraParams,
                                                              newClientOrderId=str(int(time.time())))
        else:
            futuresOrderData = gate.createAndTestFuturesOrder(symbolName, 'BUY', 'LIMIT', timeInForce='GTC',
                                                              price=20000, quantity=0.002,
                                                              newClientOrderId=str(int(time.time())))

        result = gate.makeFuturesOrder(futuresOrderData)

        gate.cancelOrder(symbol=symbolName, localOrderId=result['clientOrderId'], futures=True)

        result = gate.getOrder(symbol=symbolName, localOrderId=result['clientOrderId'], futures=True)
        assert result['status'].lower() in ['canceled', 'cancelled'], \
            'Problem in canceling specified open order by clientOrderId from {} exchange.'.format(gate.exchangeName)


def testFuturesTradeHistory(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        symbolName = symbolNamesDict[gate.exchangeName]
        tradeHistory = gate.symbolAccountTradeHistory(symbolName, futures=True)
        # print('\nTrade history from {} exchange: {}'.format(gate.exchangeName, tradeHistory))

        assert tradeHistory is not None, 'Problem in fetching trade history from {} exchange.'.format(gate.exchangeName)

        interface = ['symbol', 'id', 'orderId', 'orderListId', 'price', 'qty', 'quoteQty', 'commission',
                     'commissionAsset', 'time', 'isBuyer', 'isMaker', 'isBestMatch']

        errorMessage = 'Bad fetch trade history interface for {} exchange,'.format(gate.exchangeName)
        try:
            if gate.exchangeName != 'Binance':
                interface.append('exchangeSpecific')
                if sorted(list(tradeHistory[0].keys())) != sorted(interface):
                    assert False, errorMessage
            else:
                if sorted(list(tradeHistory[0].keys())) != sorted(interface):
                    assert False, errorMessage
        except Exception:
            assert False, errorMessage


def testFuturesSymbolList(getGatesAndSymbolNames):
    gates, symbolNamesDict = getGatesAndSymbolNames
    for gate in gates:
        if gate.exchangeName.lower() != 'binance':
            continue
        symbolList = gate.getSymbolList(futures=True)

        assert symbolList is not None
