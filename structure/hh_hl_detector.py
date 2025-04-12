import logging

def is_valid_pullback(price, last_swing_price, direction="up", threshold=0.5):
    """
    Kiểm tra xem giá hiện tại có phải là pullback hợp lệ so với điểm HH/HL gần nhất không.

    Args:
        price (float): Giá hiện tại.
        last_swing_price (float): Giá tại swing HH hoặc HL gần nhất.
        direction (str): "up" nếu xu hướng tăng, "down" nếu xu hướng giảm.
        threshold (float): Tỷ lệ tối thiểu để xem là pullback (VD: 0.5 = 50%).

    Returns:
        bool: True nếu là pullback hợp lệ.
    """
    if direction == "up":
        # Kiểm tra pullback trong xu hướng tăng
        if price <= last_swing_price and abs(price - last_swing_price) >= threshold * last_swing_price:
            logging.info(f"Uptrend pullback detected: Price = {price}, Last Swing Price = {last_swing_price}")
            return True
        else:
            logging.info(f"No uptrend pullback: Price = {price}, Last Swing Price = {last_swing_price}")
    
    elif direction == "down":
        # Kiểm tra pullback trong xu hướng giảm
        if price >= last_swing_price and abs(price - last_swing_price) >= threshold * last_swing_price:
            logging.info(f"Downtrend pullback detected: Price = {price}, Last Swing Price = {last_swing_price}")
            return True
        else:
            logging.info(f"No downtrend pullback: Price = {price}, Last Swing Price = {last_swing_price}")
    
    return False
