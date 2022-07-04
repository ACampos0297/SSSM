from datetime import datetime, timedelta

class Market:
    def __init__(self, products):
        self.transaction_log = {}
        self.brokerage_products = {}
        
        for entry in products:
            self.brokerage_products[entry.symbol] = entry

    def transact(self, symbol, quantity, transaction_type):
        par_val = self.brokerage_products[symbol].value
        price = quantity * par_val
        timestamp = datetime.now() 
        transaction_id = (timestamp, symbol)
        self.transaction_log[transaction_id] = {
                'transaction_type': transaction_type,
                'value': par_val,
                'quantity': quantity,
                'price': price
        }

        return transaction_id

    def calculate_dividend_yield(self, symbol, price):
        #   Calculate dividend yield using provided formula depending on share type "Common"/"Preferred"
        type = self.brokerage_products[symbol].type 
        dividend = 0
        
        if type == 'Common':
            dividend = self.brokerage_products[symbol].last_dividend
            return dividend/price
        elif type == 'Preferred':
            dividend = self.brokerage_products[symbol].fixed_dividend
            par_value = self.brokerage_products[symbol].value
            return (dividend*par_value)/price
        else:
            return -1 

    def calculate_price_earning_ratio(self, symbol, price):
        #   Calculate price earning ratio using provided formula of price/dividend
        dividend = self.brokerage_products[symbol].last_dividend

        if dividend == 0.0:   #   A company with negative or zero earnings doesnt have a P/E ratio
            return -1
        else:
            return price/dividend

    def calculate_volume_weighted_stock_price(self, symbol):
        # Calculate VWAP doesnt matter if buy or sale just the transacted amount 
        quantity_transacted = 0.0
        weighted_transactions = []

        cur_time = datetime.now()

        for log_entry in self.transaction_log.keys():
            if log_entry[1] == symbol and log_entry[0] > (cur_time - timedelta(minutes=15)):
                transaction = self.transaction_log[log_entry]
                weighted_transactions.append(transaction['price']*transaction['quantity'])
                quantity_transacted += transaction['quantity']
        
        if quantity_transacted > 0.0: 
            return sum(weighted_transactions)/quantity_transacted
        else:   
            return -1

    def show_transaction_log(self):
        log_entry_ids = sorted(self.transaction_log.keys(), key= lambda x: x[0])    
        for log_entry in log_entry_ids:
            transaction = self.transaction_log[log_entry] 
            print(f'''{log_entry[0].strftime("%Y-%m-%d %H:%M:%S")}: {log_entry[1]} {transaction['transaction_type']} total ${transaction['price']} for {transaction['quantity']} at ${transaction['value']} ''')


