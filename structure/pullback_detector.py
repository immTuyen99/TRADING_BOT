# structure/pullback_detector.py

import logging

# Hàm kiểm tra pullback

def check_pullback(prices, threshold=0.5):
    """
    Kiểm tra xem giá hiện tại có phải là pullback hợp lệ hay không.

    Args:
        prices (list): Danh sách các giá (object có thuộc tính close).
        threshold (float): Tỷ lệ pullback tối thiểu.

    Returns:
        bool: True nếu là pullback hợp lệ.
    """
    last_swing_price = get_last_swing(prices)
    current_price = prices[-1].close

    direction = check_hh_hl(prices)
    logging.info(f"Current price: {current_price}, Last swing: {last_swing_price}, Direction: {direction}")

    if direction not in ["uptrend", "downtrend"]:
        return False

    return is_valid_pullback(current_price, last_swing_price, direction, threshold)

# Lấy giá swing gần nhất

def get_last_swing(prices):
    """
    Tìm giá swing (HH/HL) gần nhất từ danh sách giá.

    Args:
        prices (list): Danh sách các giá đóng cửa.

    Returns:
        float: Giá swing gần nhất.
    """
    if len(prices) < 2:
        return prices[0].close

    if prices[-1].close > prices[-2].close:
        return prices[-2].close  # HL trước đó
    else:
        return prices[-2].close  # HH trước đó

# Kiểm tra xem pullback có hợp lệ hay không

def is_valid_pullback(price, last_swing_price, direction="uptrend", threshold=0.5):
    """
    Kiểm tra xem giá hiện tại có phải là pullback hợp lệ so với điểm HH/HL gần nhất không.

    Args:
        price (float): Giá hiện tại.
        last_swing_price (float): Giá tại swing HH hoặc HL gần nhất.
        direction (str): "uptrend" hoặc "downtrend".
        threshold (float): Tỷ lệ tối thiểu để xem là pullback (VD: 0.5 = 50%).

    Returns:
        bool: True nếu là pullback hợp lệ.
    """
    delta = abs(price - last_swing_price)

    if direction == "uptrend":
        valid = price < last_swing_price and delta >= threshold
    elif direction == "downtrend":
        valid = price > last_swing_price and delta >= threshold
    else:
        valid = False

    logging.info(f"Pullback delta: {delta}, Valid: {valid}")
    return valid

# Kiểm tra xu hướng HH/HL

def check_hh_hl(prices):
    """
    Kiểm tra xu hướng HH/HL từ danh sách giá.

    Args:
        prices (list): Danh sách các giá đóng cửa.

    Returns:
        str: Xu hướng thị trường ("uptrend", "downtrend", "neutral").
    """
    if len(prices) < 2:
        return "neutral"

    if prices[-1].close > prices[-2].close:
        return "uptrend"
    elif prices[-1].close < prices[-2].close:
        return "downtrend"
    else:
        return "neutral"

# Logging để kiểm tra hoạt động của các hàm
logging.basicConfig(level=logging.INFO)

# Ví dụ sử dụng
if __name__ == "__main__":
    class Price:
        def __init__(self, close):
            self.close = close

    prices = [Price(100), Price(105), Price(110), Price(107)]
    trend = check_hh_hl(prices)
    pullback = check_pullback(prices)

    logging.info(f"Current Trend: {trend}, Pullback status: {pullback}")
