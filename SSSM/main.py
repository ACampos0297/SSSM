from Market import Market
from Products import Shares, Index

def cleaned_data(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        user_input = input(prompt)
        if type_ is not None:
            try:
                user_input = type_(user_input)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and user_input > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and user_input < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and user_input not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        else:
            return user_input



def cli_market():
    print('-'*50)
    print('1)View Products\n2)Transact\n3)Calculate Dividend Yield\n4)Calculate Price/Earnings Ratio')
    print('5)Calculate VWAP\n6)Show Transaction History\n7)Exit')
    print('-'*50)
    
if __name__=='__main__':
    shares = [Shares('TEA', 'Common', 100, True, 0, 0), Shares('POP', 'Common', 100, True, 8, 0), 
        Shares('ALE', 'Common', 65, True, 23, 0), Shares('GIN', 'Preferred', 100, True, 8, 2), 
        Shares('JOE', 'Common', 250, True, 13, 0), Shares('DYS', 'Preferred', 200, True, 10, 0), 
        Shares('TSLA','Preferred',50,True,5,2)]

    index = Index('GBCE', shares[:-2])

    market = Market(shares + [index])
    
    market.transact('TEA', 5, 'B')
    market.transact('ALE', 3.5, 'B')
    market.transact('JOE', 2.1, 'B')
    market.transact('JOE', 0.1, 'B')
    market.transact('JOE', 1.5, 'S')
    market.transact('JOE', 3, 'B')
    market.transact('JOE', 4, 'B')
    market.transact('JOE', 1, 'S')



    exit = False
    while not exit:
        cli_market()
        choice = cleaned_data('Select a menu option ', int, 1, 7)
        print('-'*50)
        if choice == 1:
            print('Products in market')
            market.view_product_list()
        if choice >= 2 and choice <= 5: # Transact
            symbol = cleaned_data('Select a symbol (Enter \'q\' to go back): ', 
                    type_=str, range_=market.get_products()+['q'])
            if symbol == 'q':
                continue
            if not market.check_tradeable(symbol):
                print(f'Sorry, {symbol} is not tradeable')
                continue

        if choice >=3 and choice <= 4:
            price = round(cleaned_data('Enter a price per share: ', type_=float, min_=0.01, max_=100000.0),2)

        if choice == 2:
            print('Transact')
            transaction_type = cleaned_data(f'Sell or Buy {symbol} (S/B)? ', str, range_=['S','B','b','s']).upper()
            quantity = round(cleaned_data(f'Amount of {symbol} to {"buy" if transaction_type=="B" else "sell"}: ',float, 0.01, 100000.0),2)
            estimated_price = market.get_value(symbol)*quantity 
            print(f'Placing order to {"buy" if transaction_type=="B" else "sell"} {quantity} of {symbol} for ${estimated_price}')
            confirm = cleaned_data('Confirm (y/n)? ', str, range_=['y','n'])
            
            transaction = None
            if confirm == 'y':
                transaction = market.transact(symbol, quantity, transaction_type)

            print(f'Transaction executed at {transaction["transaction_id"][0].strftime("%Y-%m-%d %H:%M:%S")} at price ${transaction["price"]}')

        if choice == 3:
            print('Calculate Dividend Yield')

            dividend_yield = market.calculate_dividend_yield(symbol, price)
            print(f'The dividend yield for {symbol} at price ${price} is {round(dividend_yield*100,3)}%')

        if choice == 4:
            print('Calculate Price/Earnings Ratio')

            pe_ratio = market.calculate_price_earning_ratio(symbol, price)
            print(f'The price to earnings ratio for {symbol} at price ${price} is {round(pe_ratio,3)}')

        if choice == 5:
            print('Volume Weighted Stock Price')
            weighted_stock_price = market.calculate_volume_weighted_stock_price(symbol)

            if weighted_stock_price == -1:
                print(f'{symbol} has not been transacted today')
            else:
                print(f'{symbol} VWAP is {round(weighted_stock_price,3)}')

        if choice ==  6:
            market.show_transaction_log()

        if choice == 7:
            exit = True
            continue 

        print('-'*50)

        choice = cleaned_data('Press enter go back ', str, range_=[''])
