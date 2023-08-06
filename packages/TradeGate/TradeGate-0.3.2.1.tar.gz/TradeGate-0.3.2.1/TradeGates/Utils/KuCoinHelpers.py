import pandas as pd


def unifyGetBalanceSpotOut(data, isSingle=False):
    allAssets = []

    for asset in data:
        assetIndex = getAssetIndexInList(asset['currency'], allAssets)
        if assetIndex == -1:
            assetInfo = newEmptyAsset(asset['currency'])
        else:
            assetInfo = allAssets[assetIndex]

        assetInfo['free'] += float(asset['available'])
        assetInfo['locked'] += float(asset['holds'])
        assetInfo['exchangeSpecific'].append(asset)

        if assetIndex == -1:
            allAssets.append(assetInfo)

    if isSingle:
        return allAssets[0]
    else:
        return allAssets


def newEmptyAsset(assetName):
    return {
        'asset': assetName,
        'free': 0.0,
        'locked': 0.0,
        'exchangeSpecific': []
    }


def getAssetIndexInList(assetName, allAssets):
    for i in range(len(allAssets)):
        if assetName == allAssets[i]['asset']:
            return i
    return -1


def unifyTradeHistory(tradeHistory, futures=False):
    unifiedTradeHistory = []

    if futures:
        for trade in tradeHistory:
            isBuyer = True if trade['liquidity'] == 'taker' else False
            isMaker = True if trade['liquidity'] == 'maker' else False
            unifiedTradeHistory.append({
                'symbol': trade['symbol'],
                'id': trade['tradeId'],
                'orderId': trade['orderId'],
                'orderListId': -1,
                'price': trade['price'],
                'qty': trade['value'],
                'quoteQty': trade['size'],
                'commission': trade['fee'],
                'commissionAsset': trade['feeCurrency'],
                'time': trade['tradeTime'],
                'isBuyer': isBuyer,
                'isMaker': isMaker,
                'isBestMatch': None,
                'exchangeSpecific': trade
            })
    else:
        for trade in tradeHistory:
            isBuyer = True if trade['liquidity'] == 'taker' else False
            isMaker = True if trade['liquidity'] == 'maker' else False
            unifiedTradeHistory.append({
                'symbol': trade['symbol'],
                'id': trade['tradeId'],
                'orderId': trade['orderId'],
                'orderListId': -1,
                'price': trade['price'],
                'qty': trade['size'],
                'quoteQty': trade['funds'],
                'commission': trade['fee'],
                'commissionAsset': trade['feeCurrency'],
                'time': trade['createdAt'],
                'isBuyer': isBuyer,
                'isMaker': isMaker,
                'isBestMatch': None,
                'exchangeSpecific': trade
            })

    return pd.DataFrame(unifiedTradeHistory)


def unifyRecentTrades(tradeHistory, futures=False):
    unifiedTradeHistory = []

    if futures:
        for trade in tradeHistory:
            unifiedTradeHistory.append({
                'id': int(trade['sequence']),
                'price': float(trade['price']),
                'qty': float(trade['size']),
                'quoteQty': float(trade['price']) * float(trade['size']),
                'time': int(trade['ts'] / 1000),
                'isBuyerMaker': None,
                'exchangeSpecific': trade
            })
    else:
        for trade in tradeHistory:
            unifiedTradeHistory.append({
                'id': int(trade['sequence']),
                'price': float(trade['price']),
                'qty': float(trade['size']),
                'quoteQty': float(trade['price']) * float(trade['size']),
                'time': int(trade['time'] / 1000),
                'isBuyerMaker': None,
                'isBestMatch': None,
                'exchangeSpecific': trade
            })

    return unifiedTradeHistory


def getSpotOrderAsDict(orderData):
    params = {'side': orderData.side, 'symbol': orderData.symbol, 'type': orderData.orderType}

    if orderData.newClientOrderId is not None:
        params['clientOid'] = orderData.newClientOrderId

    if orderData.price is not None:
        params['price'] = orderData.price

    if orderData.quantity is not None:
        params['size'] = orderData.quantity

    if orderData.timeInForce is not None:
        params['timeInForce'] = orderData.timeInForce

    if orderData.quoteOrderQty is not None and 'size' not in params.keys():
        params['funds'] = orderData.quoteOrderQty

    if orderData.extraParams is not None:
        if 'cancelAfter' in orderData.extraParams.keys():
            params['cancelAfter'] = orderData.extraParams['cancelAfter']

        if 'postOnly' in orderData.extraParams.keys():
            params['postOnly'] = orderData.extraParams['postOnly']

        if 'hidden' in orderData.extraParams.keys():
            params['hidden'] = orderData.extraParams['hidden']

        if 'iceberg' in orderData.extraParams.keys():
            params['iceberg'] = orderData.extraParams['iceberg']

        if 'visibleSize' in orderData.extraParams.keys():
            params['visibleSize'] = orderData.extraParams['visibleSize']

        if 'stopPrice' in orderData.extraParams.keys():
            params['stopPrice'] = orderData.extraParams['stopPrice']

    return params


def unifyGetOrder(orderData, futures=False, lotSize=None):
    if futures:
        if orderData['value'] is not None and orderData['price'] is None:
            if float(orderData['size']) > 0:
                orderData['price'] = float(orderData['value']) / (float(orderData['size']) * lotSize)

        if orderData['cancelExist']:
            orderStatus = 'CANCELLED'
        elif orderData['isActive']:
            orderStatus = 'NEW'
        else:
            orderStatus = 'FILLED'

        return {'symbol': orderData['symbol'],
                'orderId': orderData['id'],
                'clientOrderId': orderData['clientOid'],
                'transactTime': orderData['createdAt'],
                'price': orderData['price'],
                'origQty': float(orderData['size']) * lotSize,
                'executedQty': float(orderData['filledSize']) * lotSize,
                'cummulativeQuoteQty': 0 if orderData['price'] is None else float(orderData['filledSize']) * float(
                    orderData['price']) * lotSize,
                'status': orderStatus,
                'timeInForce': orderData['timeInForce'],
                'type': orderData['type'],
                'side': orderData['side'],
                'extraData': {'reduceOnly': orderData['reduceOnly'],
                              'stopPrice': 0.0 if orderData['stopPrice'] is None else float(orderData['stopPrice']),
                              'workingType': 'CONTRACT_PRICE',
                              'avgPrice': orderData['price'],
                              'origType': orderData['type'],
                              'positionSide': 'BOTH',
                              'activatePrice': None,
                              'priceRate': None,
                              'closePosition': orderData['closeOrder']
                              },
                'exchangeSpecific': orderData
                }
    else:
        if orderData['cancelExist']:
            orderStatus = 'CANCELLED'
        elif orderData['isActive']:
            orderStatus = 'NEW'
        else:
            orderStatus = 'FILLED'

        return {
            "symbol": orderData['symbol'],
            "orderId": orderData['id'],
            "orderListId": -1,
            "clientOrderId": orderData['clientOid'],
            "price": orderData['price'],
            "origQty": orderData['size'],
            "executedQty": orderData['dealSize'],
            "cummulativeQuoteQty": orderData['dealSize'],
            "status": orderStatus,
            "timeInForce": orderData['timeInForce'],
            "type": orderData['type'],
            "side": orderData['side'],
            "stopPrice": orderData['stopPrice'],
            "icebergQty": orderData['visibleSize'],
            "time": orderData['createdAt'],
            "updateTime": orderData['createdAt'],
            "isWorking": orderData['isActive'],
            "origQuoteOrderQty": orderData['dealFunds'],
            "exchangeSpecific": orderData
        }


def unifyGetSymbolOrders(ordersList, futures=False, lotSize=None):
    unifiedOrdersList = []
    for orderData in ordersList:
        unifiedOrdersList.append(unifyGetOrder(orderData, futures, lotSize))
    return unifiedOrdersList


def unifyGetBestBidAsks(ticker, symbol):
    return {
        "symbol": symbol,
        "bidPrice": ticker['bestBid'],
        "bidQty": ticker['bestBidSize'],
        "askPrice": ticker['bestAsk'],
        "askQty": ticker['bestAskSize']
    }


def unifyGetBalanceFuturesOut(data, isSingle=False):
    if isSingle:
        return {
            'asset': data['currency'],
            'free': data['availableBalance'],
            'locked': data['positionMargin'],
            'exchangeSpecific': data
        }
    else:
        balances = []
        for assetData in data:
            balances.append({'asset': assetData['currency'], 'free': assetData['availableBalance'],
                             'locked': assetData['positionMargin'], 'exchangeSpecific': assetData})
        return balances


def getFuturesOrderAsDict(orderData):
    params = {'side': orderData.side,
              'symbol': orderData.symbol,
              'type': orderData.orderType}

    if 'leverage' in orderData.extraParams.keys():
        params['leverage'] = orderData.extraParams['leverage']

    if orderData.newClientOrderId is not None:
        params['clientOid'] = orderData.newClientOrderId
    else:
        params['clientOid'] = ''

    if orderData.price is not None:
        params['price'] = str(orderData.price)

    if orderData.quantity is not None:
        params['size'] = float(orderData.quantity)

    if orderData.timeInForce is not None:
        params['timeInForce'] = orderData.timeInForce

    if orderData.stopPrice is not None:
        params['stopPrice'] = orderData.stopPrice
        params['stop'] = orderData.extraParams['stop']
        params['stopPriceType'] = orderData.extraParams['stopPriceType']

    if orderData.closePosition is not None:
        params['closeOrder'] = orderData.closePosition

    if orderData.extraParams is not None:
        if 'postOnly' in orderData.extraParams.keys():
            params['postOnly'] = orderData.extraParams['postOnly']

        if 'hidden' in orderData.extraParams.keys():
            params['hidden'] = orderData.extraParams['hidden']

        if 'iceberg' in orderData.extraParams.keys():
            params['iceberg'] = orderData.extraParams['iceberg']

        if 'visibleSize' in orderData.extraParams.keys():
            params['visibleSize'] = orderData.extraParams['visibleSize']

        if 'reduceOnly' in orderData.extraParams.keys():
            params['reduceOnly'] = orderData.extraParams['reduceOnly']

        if 'forceHold' in orderData.extraParams.keys():
            params['forceHold'] = orderData.extraParams['forceHold']

        if 'postOnly' in orderData.extraParams.keys():
            params['postOnly'] = orderData.extraParams['postOnly']

        if 'hidden' in orderData.extraParams.keys():
            params['hidden'] = orderData.extraParams['hidden']

    return params


def unifyGetPositionInfo(positionInfo):
    return {
        'entryPrice': positionInfo['avgEntryPrice'],
        'isAutoAddMargin': positionInfo['autoDeposit'],
        'leverage': positionInfo['realLeverage'],
        'maxNotionalValue': None,
        'liquidationPrice': positionInfo['liquidationPrice'],
        'markPrice': positionInfo['markPrice'],
        'positionAmt': positionInfo['currentQty'],
        'symbol': positionInfo['symbol'],
        'unrealizedProfit': positionInfo['unrealisedPnl'],
        'marginType': 'cross' if positionInfo['crossMode'] else 'isolated',
        'isolatedMargin': positionInfo['maintMargin'],
        'positionSide': 'BOTH',
        'exchangeSpecific': positionInfo
    }


def unifyGetPositionInfos(positionInfos):
    posInfosList = []
    for posInfo in positionInfos:
        posInfosList.append(unifyGetPositionInfo(posInfo))
    return posInfosList


def unifyMinTrade(info, futures=False):
    if futures:
        params = {
            'minQuantity': float(info['multiplier'] * info['lotSize']),
            'precisionStep': float(info['multiplier'] * info['lotSize']),
            'stepPrice': info['tickSize']
        }
        params['minQuoteQuantity'] = params['precisionStep'] * info['lastTradePrice']
    else:
        params = {
            'minQuantity': info['baseMinSize'],
            'minQuoteQuantity': info['quoteMinSize'],
            'precisionStep': info['baseIncrement'],
            'stepPrice': info['priceIncrement']
        }
    return params
