# Running this from matlab
import yfinance as yf
import pandas as pd
import os
import requests
from requests.exceptions import HTTPError

# https://aroussi.com/post/python-yahoo-finance
def fetch_yfin_data(ticker_list, start_date, end_date):
    
    """When matlab calls, fetches  data from yahoo finance and saves to csv for matlab to read
     :Parameters:
         ticket_list_txt_file : str
             text file with excention .txt containing a list of tickers
             eg ticket_list_txt_file = "ticker_lists/firstgrocerystore.txt"
         start: str (same as tfinance download call)
             Download start date string (YYYY-MM-DD)
                start_date = "2024-01-01"
        end: str (same as tfinance download call)
                Download end date string (YYYY-MM-DD)
                end_date = "2024-03-01"
    """
    ticker_list = ticker_list.split() #split string to list
    
    df = yf.download(ticker_list, start=start_date, end=end_date,auto_adjust=True,interval="1d")
    
    cwd = os.getcwd() #get Current Working Directory
    
    # Create conjoined name
    # totalnames = ""
    # for element in ticker_list:
    #     ticker = yf.Ticker(element)
    #     totalnames = totalnames + ticker.info['symbol'] + "_"

    # Historical Market Data
    df_open = df['Open']
    openname = "tickers_open.csv"
    open_file_path = os.path.join(cwd, openname)
    df_open.to_csv(open_file_path)
    
    df_close = df['Close']
    closename = "tickers_close.csv"
    close_file_path = os.path.join(cwd, closename)
    df_close.to_csv(close_file_path)
    
    df_volume = df['Volume']
    volumename = "tickers_volume.csv"
    volume_file_path = os.path.join(cwd, volumename)
    df_volume.to_csv(volume_file_path)

    # empty list to store dataframes
    df_insidertransact = []
    df_insiderpurchase = []
    df_splits = []
    df_shares = []
    df_dividends = []
    df_recommendations = []
    df_cashflow = []

    
    #singular ticker in list data grabber
    for element in ticker_list:

        ticker = yf.Ticker(element)
        
        # insider transactions
        try:
            df_insider1 = ticker.insider_transactions
        except:
            print("Insider transcations not found")
        else:
            df_insider1['Ticker'] = ticker.info['symbol']
            df_insidertransact.append(df_insider1)

        #insider purchases
        try:
            df_insider2 = ticker.insider_purchases
        except:
            print("Insider purchases not found")
        else:
            df_insider2['Ticker'] = ticker.info['symbol']
            df_insiderpurchase.append(df_insider2)

        #splits
        try:
            splits = ticker.splits
        except:
            print("Splits not found")
        else:
            #turn series to dataframe
            splits_new = pd.DataFrame({'time':splits.index, 'value':splits.values})
            splits_new['Ticker'] = ticker.info['symbol']
            df_splits.append(splits_new)

        #dividends
        try:
            dividends = ticker.dividends
        except:
            print("Dividends not found")
        else:
            #turn series to dataframe
            dividends_new = pd.DataFrame({'time':dividends.index, 'value':dividends.values})
            dividends_new['Ticker'] = ticker.info['symbol']
            df_dividends.append(dividends_new)

        #analylist recommendations
        try:
            recommendations = ticker.recommendations
        except:
            print("Analylist not found")
        else:
            recommendations['Ticker'] = ticker.info['symbol']
            df_recommendations.append(recommendations)

        #cashflow
        try:
            cashflow = ticker.cashflow
        except:
            print("Cashflow not found")
        else:
            cashflow = cashflow.transpose()
            cashflow['Ticker'] = ticker.info['symbol']
            df_cashflow.append(cashflow)

        #share count
        try:
            shares = ticker.get_shares_full(start=start_date, end=end_date)
        except:
            print("Shares not found")
        else:
            #turn series to dataframe
            shares_new = pd.DataFrame({'time':shares.index, 'value':shares.values})
            shares_new['Ticker'] = ticker.info['symbol']
            df_shares.append(shares_new)
        
    #combine to one dataframe and put in csv
    if df_insidertransact != []:
        combined_transact = pd.concat(df_insidertransact)
        insider1_file_path = os.path.join(cwd, "tickers_insidertransact.csv")
        combined_transact.to_csv(insider1_file_path)

    if df_insiderpurchase != []:
        combined_purchase = pd.concat(df_insiderpurchase)
        insider2_file_path = os.path.join(cwd, "tickers_insiderpurchase.csv")
        combined_purchase.to_csv(insider2_file_path) 

    if df_splits != []:
        combined_splits = pd.concat(df_splits)
        combined_splits.columns = ["Time", "Splits", "Ticker"]
        splits_file_path = os.path.join(cwd, "tickers_splits.csv")
        combined_splits.to_csv(splits_file_path, index=True)

    if df_dividends != []:
        combined_dividends = pd.concat(df_dividends)
        combined_dividends.columns = ["Time", "Dividends", "Ticker"]
        dividends_file_path = os.path.join(cwd, "tickers_dividends.csv")
        combined_dividends.to_csv(dividends_file_path, index=True)

    if df_recommendations != []:
        combined_recommendations = pd.concat(df_recommendations)
        recommendations_file_path = os.path.join(cwd, "tickers_recommendations.csv")
        combined_recommendations.to_csv(recommendations_file_path, index=True)

    if df_cashflow != []:
        combined_cashflow = pd.concat(df_cashflow)
        cashflow_file_path = os.path.join(cwd, "tickers_cashflow.csv")
        combined_cashflow.to_csv(cashflow_file_path, index=True)
    
    if df_shares != []:
        combined_shares = pd.concat(df_shares)
        combined_shares.columns = ["Time", "Shares", "Ticker"]
        shares_file_path = os.path.join(cwd, "tickers_shares.csv")
        combined_shares.to_csv(shares_file_path, index=True) 


# test
# ticker_list = "MSFT AAPL"
# fetch_yfin_data(ticker_list, "2024-01-01", "2024-03-01")

# data = pd.read_csv("tickers_cashflow.csv") 
# data_top = data.head() 
# print(data_top)

ticker = yf.Ticker('MSFT')
try:
    tickertransactions = ticker.insider_transactions
except HTTPError:
    print ("error")
else:
    print(tickertransactions)

# cwd = os.getcwd()
# filepath = os.path.join(cwd, "cashflowtest.csv")
# cashflowtest.to_csv(filepath, index=True)

# print(cashflowtest.columns)
# print(cashflowtest.index)
# print(cashflowtest.values)

# cashflowtest = cashflowtest.transpose()
# print(cashflowtest)

# tickerStrings = ['AAPL', 'MSFT']
# df_list = []
# for ticker in tickerStrings:
#     data = yf.download(ticker, group_by="Ticker", period='2d')
#     data['ticker'] = ticker  # Add ticker column
#     df_list.append(data)

# # Combine all dataframes into a single dataframe
# df = pd.concat(df_list)
# df.to_csv('ticker.csv')

# keep this because matlab will call this function. do not change argument names, matlab needs them

# fetch_yfin_data(ticker_list, yfin_start_date, yfin_end_date)