import logging
import yfinance as yf
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FinancialAnalyst:
   async def get_stock_price(self, ticker):
      try:
         stock = yf.Ticker(ticker)
         info = stock.info
         current_price = info.get('currentPrice', None)
         if current_price is not None:
             return f"Текущая цена акции {ticker}: {current_price:.2f} USD"
         else:
            logging.error(f"Информация о текущей цене для акции {ticker} не найдена.")
            return f"Информация о текущей цене для акции {ticker} не найдена."
      except Exception as e:
           logging.error(f"Ошибка при получении информации о ценах акций: {e}")
           return f"Ошибка при получении информации о ценах акций: {e}"

   async def get_historical_data(self, ticker, period='1mo'):
       try:
           stock = yf.Ticker(ticker)
           history = stock.history(period=period)

           if history.empty:
              return f"Нет исторических данных для акции {ticker} за период '{period}'."
           # Настройка pandas для корректного вывода
           pd.set_option('display.max_rows', None)
           pd.set_option('display.max_columns', None)
           pd.set_option('display.width', None)
           pd.set_option('display.max_colwidth', None)
           return f"Исторические данные для акции {ticker} за период '{period}':\n{history}"
       except Exception as e:
           logging.error(f"Ошибка при получении исторических данных акций: {e}")
           return f"Ошибка при получении исторических данных акций: {e}"
   async def get_financial_data(self, ticker):
      try:
         stock = yf.Ticker(ticker)
         info = stock.info
         if not info:
             return "Информация по запрошенной акции не найдена."
         result = ""
         for key, value in info.items():
            if isinstance(value, (str, int, float, bool)):
              result += f"{key}: {value}\n"
            elif isinstance(value, dict):
                result += f"{key}:\n"
                for k, v in value.items():
                    if isinstance(v, (str, int, float, bool)):
                      result+= f"    {k}: {v}\n"
         return result
      except Exception as e:
            logging.error(f"Ошибка при получении финансовой информации: {e}")
            return f"Ошибка при получении финансовой информации: {e}"