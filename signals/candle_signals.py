# signals/candle_signals.py

def is_bullish_engulfing(prev_candle, curr_candle):
    return (
        prev_candle['close'] < prev_candle['open'] and
        curr_candle['close'] > curr_candle['open'] and
        curr_candle['close'] > prev_candle['open'] and
        curr_candle['open'] < prev_candle['close']
    )

def is_pin_bar(candle, ratio=0.66):
    body = abs(candle['close'] - candle['open'])
    upper_wick = candle['high'] - max(candle['close'], candle['open'])
    lower_wick = min(candle['close'], candle['open']) - candle['low']
    return (
        (lower_wick > body * ratio and upper_wick < body * 0.5) or
        (upper_wick > body * ratio and lower_wick < body * 0.5)
    )

def is_volume_spike(candle, avg_volume, multiplier=1.5):
    return candle['volume'] > avg_volume * multiplier

def is_strong_bullish_candle(candle, avg_volume, volume_multiplier=1.2, body_ratio=0.7):
    body = abs(candle['close'] - candle['open'])
    range_ = candle['high'] - candle['low']
    return (
        candle['close'] > candle['open'] and
        body >= range_ * body_ratio and
        candle['volume'] > avg_volume * volume_multiplier
    )
