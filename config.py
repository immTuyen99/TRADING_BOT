# config.py

# --- TÀI KHOẢN MT5 ---
ACCOUNT = 204041814
PASSWORD = "dmT290699@"
SERVER = "Exness-MT5Trial7"

# --- CẶP GIAO DỊCH & THÔNG SỐ CƠ BẢN ---
SYMBOL = "BTCUSDm"
DEFAULT_LOT_SIZE = 0.1

# --- QUẢN LÝ RỦI RO & CHỐT LỜI ---
STOP_LOSS = 150           # SL cố định (points)
TAKE_PROFIT = 500         # TP cố định (points)
BREAKEVEN_PIPS = 20       # Dời SL về entry sau khi lời X points
SPREAD_MAX = 15           # Spread tối đa cho phép (points)
MAX_ORDERS = 5            # Số lệnh mở tối đa cùng lúc
RISK_PERCENTAGE = 1.0     # % rủi ro tối đa cho mỗi lệnh

# --- TRAILING STOP ---
USE_TRAILING_STOP = True
TRAILING_STEP = 15        # Dời SL theo bước (points)

# --- THỜI GIAN ---
TIMEFRAME = "M5"          # Timeframe phân tích
CANDLE_HISTORY = 2000     # Số lượng nến để học xác suất
