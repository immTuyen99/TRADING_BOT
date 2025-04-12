# utils/mt5_helper.py

import MetaTrader5 as mt5
import time

def initialize_mt5():
    """
    Khởi tạo kết nối với MetaTrader 5.
    """
    if not mt5.initialize():
        print("Không thể kết nối với MetaTrader 5.")
        return False
    print("Kết nối MetaTrader 5 thành công.")
    return True

def shutdown_mt5():
    """
    Đóng kết nối với MetaTrader 5.
    """
    mt5.shutdown()
    print("Kết nối MetaTrader 5 đã được đóng.")

def get_symbol_data(symbol, timeframe, n_bars=100):
    """
    Lấy dữ liệu giá từ MetaTrader 5.
    """
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_bars)
    if rates is None:
        print(f"Lỗi lấy dữ liệu {symbol}.")
        return None
    return rates

def place_order(symbol, action, volume, price, sl, tp):
    """
    Gửi lệnh Buy/Sell.
    """
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
        "magic": 234000,
        "comment": "Trading Bot",
        "type_filling": mt5.ORDER_FILLING_IOC,
        "type_time": mt5.ORDER_TIME_GTC
    }
    
    result = mt5.order_send(request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Lỗi gửi lệnh: {result.comment}")
    else:
        print(f"Lệnh {action} {symbol} đã được thực hiện.")
    
    return result
