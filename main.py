import MetaTrader5 as mt5
import logging
import time

logging.basicConfig(level=logging.INFO)

def check_open_orders():
    # Kiểm tra xem MetaTrader 5 đã kết nối chưa
    if not mt5.initialize():
        logging.error("Failed to initialize MetaTrader 5.")
        return None

    # Kiểm tra thông tin tài khoản
    account_info = mt5.account_info()
    if account_info is None:
        logging.error("Failed to retrieve account info")
        return None

    # Kiểm tra các lệnh đã mở
    orders = mt5.orders_get(symbol="BTCUSDm")
    if orders is None:
        logging.error("Failed to retrieve open orders")
        return None

    return orders, account_info

def open_order(symbol, volume):
    # Mở một lệnh BUY
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).ask,
        "sl": mt5.symbol_info_tick(symbol).ask - 100,  # Stop loss
        "tp": mt5.symbol_info_tick(symbol).ask + 100,  # Take profit
        "deviation": 10,
        "magic": 234000,
        "comment": "Trading Bot Order",
        "type_filling": mt5.ORDER_FILLING_IOC,
        "type_time": mt5.ORDER_TIME_GTC
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Failed to open order: {result}")
    else:
        logging.info(f"Order opened successfully: {result}")
    return result

def main():
    # Kiểm tra các lệnh mở và lấy thông tin tài khoản
    result = check_open_orders()
    
    if result is None:
        return

    open_orders, account_info = result
    
    # In ra thông tin các lệnh mở
    if open_orders:
        logging.info(f"Open orders: {len(open_orders)}")
    else:
        logging.info("No open orders.")
    
    # Kiểm tra số dư tài khoản
    if account_info.balance <= 0:
        logging.error("No available balance to open order. Waiting for funds.")
        # Tiếp tục kiểm tra và đợi, không thoát bot
        return

    logging.info(f"Account balance: {account_info.balance}")
    
    # Nếu không có lệnh mở và có đủ tiền, mở một lệnh BUY
    if not open_orders and account_info.balance > 0:
        volume = 0.1  # Đặt khối lượng lệnh
        open_order("BTCUSDm", volume)

if __name__ == "__main__":
    while True:  # Thêm vòng lặp để bot tiếp tục hoạt động và kiểm tra liên tục
        main()
        time.sleep(10)  # Đợi 10 giây trước khi kiểm tra lại
