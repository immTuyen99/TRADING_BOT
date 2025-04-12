# signals/signal_filter.py

import logging

def calculate_probability(signal_count, total_count):
    """
    Tính xác suất của tín hiệu dựa trên số lần tín hiệu thành công.
    """
    if total_count == 0:
        logging.warning("Tổng số tín hiệu không thể bằng 0.")
        return 0
    probability = (signal_count / total_count) * 100
    logging.info(f"Xác suất tín hiệu: {probability}%")
    return probability

def filter_signals(signals, min_probability=70):
    """
    Lọc các tín hiệu có xác suất trên một ngưỡng cho phép.
    """
    filtered_signals = []
    
    for signal in signals:
        if signal['probability'] >= min_probability:
            filtered_signals.append(signal)
        else:
            logging.info(f"Tín hiệu bị loại bỏ: {signal['type']} với xác suất {signal['probability']}%")
    
    logging.info(f"Đã lọc {len(filtered_signals)} tín hiệu từ tổng số {len(signals)} tín hiệu.")
    return filtered_signals

def evaluate_signal(signal):
    """
    Đánh giá tín hiệu và tính xác suất thắng.
    Ví dụ: tín hiệu nến Bullish Engulfing có xác suất thắng cao hơn tín hiệu Pin Bar.
    """
    if signal['type'] == 'bullish_engulfing':
        signal['probability'] = 80  # Tín hiệu Bullish Engulfing giả sử có xác suất thắng 80%
    elif signal['type'] == 'pin_bar':
        signal['probability'] = 60  # Tín hiệu Pin Bar giả sử có xác suất thắng 60%
    elif signal['type'] == 'volume_spike':
        signal['probability'] = 70  # Tín hiệu Volume Spike giả sử có xác suất thắng 70%
    else:
        signal['probability'] = 50  # Mặc định cho tín hiệu không xác định
    
    logging.info(f"Tín hiệu {signal['type']} có xác suất: {signal['probability']}%")
    return signal
