# signals/candle_signals.py

import logging

def is_bullish_engulfing(prev_candle, curr_candle):
    """
    Kiểm tra tín hiệu Bullish Engulfing.
    """
    is_bullish = (
        prev_candle['close'] < prev_candle['open'] and  # Nến trước giảm
        curr_candle['close'] > curr_candle['open'] and  # Nến sau tăng
        curr_candle['close'] > prev_candle['open'] and  # Nến sau vượt qua giá mở cửa nến trước
        curr_candle['open'] < prev_candle['close']  # Giá mở cửa nến sau nhỏ hơn giá đóng cửa nến trước
    )
    logging.info(f"Kiểm tra Bullish Engulfing: {is_bullish}")
    return is_bullish

def is_pin_bar(candle, ratio=0.66):
    """
    Kiểm tra tín hiệu Pin Bar.
    """
    body = abs(candle['close'] - candle['open'])
    upper_wick = candle['high'] - max(candle['close'], candle['open'])
    lower_wick = min(candle['close'], candle['open']) - candle['low']
    
    is_pin_bar_signal = (
        (lower_wick > body * ratio and upper_wick < body * 0.5) or
        (upper_wick > body * ratio and lower_wick < body * 0.5)
    )
    logging.info(f"Kiểm tra Pin Bar: {is_pin_bar_signal}")
    return is_pin_bar_signal

def is_volume_spike(candle, avg_volume, multiplier=1.5):
    """
    Kiểm tra tín hiệu Volume Spike (tăng đột biến khối lượng giao dịch).
    """
    is_spike = candle['volume'] > avg_volume * multiplier
    logging.info(f"Kiểm tra Volume Spike: {is_spike}")
    return is_spike

def is_strong_bullish_candle(candle, avg_volume, volume_multiplier=1.2, body_ratio=0.7):
    """
    Kiểm tra tín hiệu Strong Bullish Candle (nến tăng mạnh với khối lượng lớn).
    """
    body = abs(candle['close'] - candle['open'])
    range_ = candle['high'] - candle['low']
    
    is_strong_bullish = (
        candle['close'] > candle['open'] and  # Nến tăng
        body >= range_ * body_ratio and  # Nến có thân lớn
        candle['volume'] > avg_volume * volume_multiplier  # Khối lượng lớn
    )
    logging.info(f"Kiểm tra Strong Bullish Candle: {is_strong_bullish}")
    return is_strong_bullish
