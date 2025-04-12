import MetaTrader5 as mt5
import logging
import time

class MT5Trader:
    def __init__(self, account, password, server, symbol, lot_size, sl, tp):
        self.account = account
        self.password = password
        self.server = server
        self.symbol = symbol
        self.lot_size = lot_size
        self.sl = sl
        self.tp = tp

    def connect(self):
        if not mt5.initialize():
            logging.error("Failed to initialize MT5")
            return False
        if not mt5.login(self.account, password=self.password, server=self.server):
            logging.error("Failed to connect to MT5 account")
            return False
        return True

    def open_order(self, order_type="buy"):
        symbol_info = mt5.symbol_info(self.symbol)
        if symbol_info is None:
            logging.error(f"Symbol info not found for {self.symbol}")
            return None
        
        digits = symbol_info.digits
        tick = mt5.symbol_info_tick(self.symbol)

        if order_type == "buy":
            price = tick.ask
            sl = price - self.sl
            tp = price + self.tp
            order_type_mt5 = mt5.ORDER_TYPE_BUY
        else:
            price = tick.bid
            sl = price + self.sl
            tp = price - self.tp
            order_type_mt5 = mt5.ORDER_TYPE_SELL

        # Làm tròn giá trị
        price = round(price, digits)
        sl = round(sl, digits)
        tp = round(tp, digits)

        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": order_type_mt5,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234000,
            "comment": "Trading Bot Order",
            "type_filling": mt5.ORDER_FILLING_IOC,
            "type_time": mt5.ORDER_TIME_GTC,
        }

        result = mt5.order_send(order)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Failed to open order: {result.retcode}")
            logging.error(f"Full result: {result}")
            return None

        logging.info(f"Order opened successfully: {result}")
        return result

    def close_order(self, order_id):
        result = mt5.order_send({
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": order_id,
        })
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Failed to close order: {result.retcode}")
            return False
        logging.info(f"Order closed: {result}")
        return True

    def get_balance(self):
        account_info = mt5.account_info()
        if account_info is None:
            logging.error("Failed to retrieve account info")
            return None
        return account_info.balance

    def disconnect(self):
        mt5.shutdown()
