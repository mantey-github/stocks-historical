import requests
from datetime import datetime

class Fetcher:
    BASE_URL = "https://your-server.com/api/v1/stocks"

    def __init__(self, market: str, symbol: str, start: int, end: int):
        self.market = market
        self.symbol = symbol.upper()
        self.start = start
        self.end = end

    def fetch_data(self):
        try:
            url = f"{self.BASE_URL}/{self.market}/{self.symbol}"
            params = {"start": self.start, "end": self.end}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching data: {e}")

    @staticmethod
    def format_data(data):
        """
        Format JSON data into a Python-friendly dictionary with datetime objects.
        """
        formatted = {
            "meta": data.get("meta", {}),
            "data": [
                {
                    "timestamp": datetime.fromtimestamp(ts),
                    "open": q.get("open"),
                    "high": q.get("high"),
                    "low": q.get("low"),
                    "close": q.get("close"),
                    "volume": q.get("volume"),
                }
                for ts, q in zip(data["timestamp"], data["indicators"]["quote"][0]["open"])
            ],
        }
        return formatted
