# trade/order_executor.py

import MetaTrader5 as mt5

def place_order(symbol, order_type, volume, sl, tp):
    """
    Gửi lệnh mua/bán vào MT5.
    """
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 234000,
        "comment": "Trading Bot Order",
        "type_filling": mt5.ORDER_FILLING_IOC,
        "type_time": mt5.ORDER_TIME_GTC
    }
    
    result = mt5.order_send(request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Lỗi gửi lệnh: {result.comment}")
    else:
        print(f"Lệnh {order_type} {symbol} đã được thực hiện.")
    
    return result
