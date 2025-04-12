# risk/sl_tp_manager.py

import logging

def calculate_sl(entry_price, stop_loss_points):
    """
    Tính mức Stop Loss (SL) cho lệnh dựa trên mức giá entry và số điểm SL.
    """
    if stop_loss_points <= 0:
        logging.warning(f"Số điểm Stop Loss không hợp lệ: {stop_loss_points}. Phải lớn hơn 0.")
        return None

    sl_price = entry_price - stop_loss_points
    logging.info(f"Tính SL: {sl_price} từ entry_price: {entry_price} với stop_loss_points: {stop_loss_points}")
    return sl_price

def calculate_tp(entry_price, take_profit_points):
    """
    Tính mức Take Profit (TP) cho lệnh dựa trên mức giá entry và số điểm TP.
    """
    if take_profit_points <= 0:
        logging.warning(f"Số điểm Take Profit không hợp lệ: {take_profit_points}. Phải lớn hơn 0.")
        return None

    tp_price = entry_price + take_profit_points
    logging.info(f"Tính TP: {tp_price} từ entry_price: {entry_price} với take_profit_points: {take_profit_points}")
    return tp_price

def adjust_sl_to_breakeven(order, breakeven_pips):
    """
    Dời Stop Loss về mức breakeven khi giá đã di chuyển đủ số pip.
    """
    if breakeven_pips <= 0:
        logging.warning(f"Số pip breakeven không hợp lệ: {breakeven_pips}. Phải lớn hơn 0.")
        return order

    if order['current_price'] >= order['entry_price'] + breakeven_pips:
        order['sl'] = order['entry_price']
        logging.info(f"Dời SL về mức breakeven: {order['sl']} cho lệnh {order['id']}")
    else:
        logging.info(f"Không đủ pip để dời SL về breakeven cho lệnh {order['id']}.")
    return order
