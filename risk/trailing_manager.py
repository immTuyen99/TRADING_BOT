# risk/trailing_manager.py

import logging

def update_trailing_stop(order, trailing_step, market_price):
    """
    Cập nhật mức trailing stop dựa trên mức giá thị trường và trailing_step.
    """
    if trailing_step <= 0:
        logging.warning(f"Mức trailing_step không hợp lệ: {trailing_step}. Phải lớn hơn 0.")
        return order

    if order['sl'] < market_price - trailing_step:
        new_sl = market_price - trailing_step
        order['sl'] = new_sl
        logging.info(f"Đã cập nhật trailing stop cho lệnh {order['id']}: {order['sl']}")
    else:
        logging.info(f"Không đủ điều kiện để cập nhật trailing stop cho lệnh {order['id']}.")

    return order
