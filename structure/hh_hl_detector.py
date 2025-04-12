# structure/pullback_detector.py

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
        print(f"find the up....")
        return price <= last_swing_price and abs(price - last_swing_price) >= threshold
    elif direction == "down":
        print(f"find the down....")
        return price >= last_swing_price and abs(price - last_swing_price) >= threshold
    return False
