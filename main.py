import MetaTrader5 as mt5
import logging
import time
from signals.signal_filter import evaluate_signal, filter_signals
from signals.candle_signals import is_bullish_engulfing, is_pin_bar, is_volume_spike
from risk.sl_tp_manager import calculate_sl, calculate_tp, adjust_sl_to_breakeven
from risk.trailing_manager import update_trailing_stop

logging.basicConfig(level=logging.INFO)

def check_open_orders():
    """
    Kiểm tra xem MetaTrader 5 đã kết nối chưa và kiểm tra các lệnh mở.
    """
    if not mt5.initialize():
        logging.error("Failed to initialize MetaTrader 5.")
        return None

    account_info = mt5.account_info()
    if account_info is None:
        logging.error("Failed to retrieve account info")
        return None

    orders = mt5.orders_get(symbol="BTCUSDm")
    if orders is None:
        logging.error("Failed to retrieve open orders")
        return None

    return orders, account_info

def open_order(symbol, volume):
    """
    Mở một lệnh BUY với thông số SL và TP mặc định.
    """
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

def evaluate_and_open_order(symbol, account_info):
    """
    Đánh giá tín hiệu và mở lệnh nếu tín hiệu hợp lệ và tài khoản có đủ số dư.
    """
    # Lọc tín hiệu có xác suất cao
    signals = []  # Lấy các tín hiệu từ các module tín hiệu
    signals = filter_signals(signals)

    # Kiểm tra nếu có tín hiệu phù hợp
    if signals:
        for signal in signals:
            signal = evaluate_signal(signal)  # Đánh giá tín hiệu
            if signal['probability'] >= 70:  # Chỉ mở lệnh nếu tín hiệu đủ mạnh
                logging.info(f"Signal {signal['type']} detected with probability {signal['probability']}%")
                # Nếu tín hiệu là Bullish Engulfing hoặc Pin Bar
                if is_bullish_engulfing(signal['prev_candle'], signal['curr_candle']):
                    volume = 0.1  # Đặt khối lượng
                    open_order(symbol, volume)
                    break

def manage_open_orders(open_orders, account_info):
    """
    Quản lý các lệnh mở, điều chỉnh SL/TP và trailing stop nếu cần.
    """
    for order in open_orders:
        # Cập nhật trailing stop
        update_trailing_stop(order, trailing_step=10, market_price=mt5.symbol_info_tick(order['symbol']).ask)

        # Dời SL về breakeven khi đủ điều kiện
        order = adjust_sl_to_breakeven(order, breakeven_pips=20)

        # Kiểm tra điều kiện đóng lệnh nếu cần
        if mt5.symbol_info_tick(order['symbol']).ask > order['tp']:
            logging.info(f"Take profit reached for order {order['ticket']}. Closing order.")
            mt5.order_send({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": order['symbol'],
                "volume": order['volume'],
                "type": mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(order['symbol']).bid,
                "ticket": order['ticket'],
            })

def main():
    """
    Chạy bot, kiểm tra các lệnh mở, mở lệnh mới nếu đủ điều kiện và quản lý lệnh.
    """
    # Kiểm tra các lệnh mở và lấy thông tin tài khoản
    result = check_open_orders()
    if result is None:
        return

    open_orders, account_info = result

    # Kiểm tra số dư tài khoản
    if account_info.balance <= 0:
        logging.error("No available balance to open order. Waiting for funds.")
        return

    logging.info(f"Account balance: {account_info.balance}")

    # Nếu không có lệnh mở và có đủ tiền, mở một lệnh BUY
    if not open_orders and account_info.balance > 0:
        evaluate_and_open_order("BTCUSDm", account_info)
    else:
        # Nếu có lệnh mở, tiếp tục quản lý các lệnh
        manage_open_orders(open_orders, account_info)

if __name__ == "__main__":
    while True:  # Thêm vòng lặp để bot tiếp tục hoạt động và kiểm tra liên tục
        main()
        time.sleep(10)  # Đợi 10 giây trước khi kiểm tra lại
