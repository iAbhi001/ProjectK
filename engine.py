import requests
import pandas as pd

class StockEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    def get_daily_prices(self, symbol):
        """Fetches historical price data for the chart."""
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "compact"
        }
        try:
            response = requests.get(self.base_url, params=params).json()
            data = response['Time Series (Daily)']
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            df.columns = [c.split(' ')[1] for c in df.columns]
            return df.sort_index()
        except Exception:
            return None

    def get_company_overview(self, symbol):
        """Fetches fundamental data (PE, Market Cap, etc.)."""
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        return requests.get(self.base_url, params=params).json()

    def get_stock_news(self, symbol):
        """Fetches the latest 5 news articles and sentiment."""
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "apikey": self.api_key,
            "limit": 5
        }
        try:
            response = requests.get(self.base_url, params=params).json()
            return response.get('feed', [])
        except Exception:
            return []