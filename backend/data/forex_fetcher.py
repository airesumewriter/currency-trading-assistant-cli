import requests
import sqlite3
import os
import json
import time
from cli.utils.config import load_config

class ForexDataFetcher:
    def __init__(self, api_keys=None, cache_db="forex_cache.db", ttl_live=300):
        """
        api_keys: dict of API keys (optional - will try to load from config if not provided)
        cache_db: SQLite file for caching
        ttl_live: time-to-live for live prices (seconds), default 5 min
        """
        # Try to load API keys from config if not provided
        if api_keys is None:
            api_keys = self._load_api_keys_from_config()
        
        self.api_keys = api_keys or {}
        self.cache_db = cache_db
        self.ttl_live = ttl_live

        # Init SQLite cache
        self._init_cache()

        # Priority order for live
        self.live_sources = [
            self.fetch_alpha_vantage_live,
            self.fetch_exchangerate_host_live,
            self.fetch_freeforexapi_live
        ]

        # Priority order for daily history
        self.history_sources_daily = [
            self.fetch_alpha_vantage_history_daily,
            self.fetch_exchangerate_host_history
        ]

    def _load_api_keys_from_config(self):
        """Safely load API keys from config with error handling"""
        try:
            config = load_config()
            api_keys = {}
            if 'api_keys' in config and 'alpha_vantage' in config['api_keys']:
                api_keys['alpha_vantage'] = config['api_keys']['alpha_vantage']
            return api_keys
        except Exception as e:
            print(f"[WARN] Failed to load API keys from config: {e}")
            return {}

    # ---------------- CACHE ----------------
    def _init_cache(self):
        conn = sqlite3.connect(self.cache_db)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            data TEXT,
            timestamp REAL,
            permanent INTEGER
        )
        """)
        conn.commit()
        conn.close()

    def _get_cache(self, key, is_live=False):
        conn = sqlite3.connect(self.cache_db)
        cur = conn.cursor()
        cur.execute("SELECT data, timestamp, permanent FROM cache WHERE key=?", (key,))
        row = cur.fetchone()
        conn.close()
        if row:
            data, timestamp, permanent = row
            # Permanent = never expires
            if permanent:
                return json.loads(data)
            # Live data = TTL-based
            if is_live and (time.time() - timestamp < self.ttl_live):
                return json.loads(data)
        return None

    def _set_cache(self, key, data, permanent=False):
        conn = sqlite3.connect(self.cache_db)
        cur = conn.cursor()
        cur.execute(
            "REPLACE INTO cache (key, data, timestamp, permanent) VALUES (?, ?, ?, ?)",
            (key, json.dumps(data), time.time(), 1 if permanent else 0)
        )
        conn.commit()
        conn.close()

    def invalidate_live_cache(self):
        """
        Clears all live cache entries (non-permanent),
        keeps historical (permanent) data intact.
        """
        conn = sqlite3.connect(self.cache_db)
        cur = conn.cursor()
        cur.execute("DELETE FROM cache WHERE permanent=0")
        conn.commit()
        conn.close()
        print("[INFO] Live cache cleared, historical data kept intact.")

    # ---------------- LIVE PRICE ----------------
    def get_price(self, base, quote):
        cache_key = f"live:{base}{quote}"
        cached = self._get_cache(cache_key, is_live=True)
        if cached:
            return cached

        for source in self.live_sources:
            try:
                price = source(base, quote)
                if price:
                    result = {"base": base, "quote": quote, "price": price, "source": source.__name__}
                    self._set_cache(cache_key, result, permanent=False)
                    return result
            except Exception as e:
                print(f"[WARN] {source.__name__} failed: {e}")
        raise RuntimeError("All sources failed to fetch live forex data.")

    def fetch_alpha_vantage_live(self, base, quote):
        api_key = self.api_keys.get("alpha_vantage")
        if not api_key:
            return None
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={base}&to_currency={quote}&apikey={api_key}"
        r = requests.get(url, timeout=5)
        data = r.json()
        if "Realtime Currency Exchange Rate" in data:
            return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        return None

    def fetch_exchangerate_host_live(self, base, quote):
        url = f"https://api.exchangerate.host/latest?base={base}&symbols={quote}"
        r = requests.get(url, timeout=5)
        data = r.json()
        if "rates" in data and quote in data["rates"]:
            return float(data["rates"][quote])
        return None

    def fetch_freeforexapi_live(self, base, quote):
        symbol = f"{base}{quote}"
        url = f"https://www.freeforexapi.com/api/live?pairs={symbol}"
        r = requests.get(url, timeout=5)
        data = r.json()
        if "rates" in data and symbol in data["rates"]:
            return float(data["rates"][symbol]["rate"])
        return None

    # ---------------- DAILY HISTORICAL ----------------
    def get_history_daily(self, base, quote, start_date, end_date):
        cache_key = f"daily:{base}{quote}:{start_date}:{end_date}"
        cached = self._get_cache(cache_key, is_live=False)
        if cached:
            return cached

        for source in self.history_sources_daily:
            try:
                history = source(base, quote, start_date, end_date)
                if history:
                    result = {"base": base, "quote": quote, "history": history, "source": source.__name__}
                    # Store permanently
                    self._set_cache(cache_key, result, permanent=True)
                    return result
            except Exception as e:
                print(f"[WARN] {source.__name__} failed: {e}")
        raise RuntimeError("All sources failed to fetch daily history.")

    def fetch_alpha_vantage_history_daily(self, base, quote, start_date, end_date):
        api_key = self.api_keys.get("alpha_vantage")
        if not api_key:
            return None
        url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={base}&to_symbol={quote}&apikey={api_key}&outputsize=full"
        r = requests.get(url, timeout=10)
        data = r.json()
        if "Time Series FX (Daily)" not in data:
            return None
        ts = data["Time Series FX (Daily)"]
        history = {}
        for date_str, values in ts.items():
            if start_date <= date_str <= end_date:
                history[date_str] = float(values["4. close"])
        return dict(sorted(history.items()))

    def fetch_exchangerate_host_history(self, base, quote, start_date, end_date):
        url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base={base}&symbols={quote}"
        r = requests.get(url, timeout=10)
        data = r.json()
        if "rates" not in data:
            return None
        history = {}
        for date_str, values in data["rates"].items():
            if quote in values:
                history[date_str] = float(values[quote])
        return dict(sorted(history.items()))

    # ---------------- INTRADAY HISTORICAL ----------------
    def get_history_intraday(self, base, quote, interval="5min", output_size="compact"):
        cache_key = f"intraday:{base}{quote}:{interval}:{output_size}"
        cached = self._get_cache(cache_key, is_live=False)
        if cached:
            return cached

        result = self.fetch_alpha_vantage_history_intraday(base, quote, interval, output_size)
        if result:
            # Store permanently
            wrapped = {"base": base, "quote": quote, "history": result, "source": "fetch_alpha_vantage_history_intraday"}
            self._set_cache(cache_key, wrapped, permanent=True)
            return wrapped
        raise RuntimeError("Intraday history unavailable (Alpha Vantage only).")

    def fetch_alpha_vantage_history_intraday(self, base, quote, interval, output_size):
        api_key = self.api_keys.get("alpha_vantage")
        if not api_key:
            return None
        url = (
            f"https://www.alphavantage.co/query?"
            f"function=FX_INTRADAY&from_symbol={base}&to_symbol={quote}"
            f"&interval={interval}&apikey={api_key}&outputsize={output_size}"
        )
        r = requests.get(url, timeout=10)
        data = r.json()
        key = f"Time Series FX ({interval})"
        if key not in data:
            return None
        ts = data[key]
        history = {}
        for timestamp, values in ts.items():
            history[timestamp] = float(values["4. close"])
        return dict(sorted(history.items()))


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    # Test without config dependency first
    fetcher = ForexDataFetcher(api_keys={"alpha_vantage": "GARJ46JPDQ5H5PFW"}, ttl_live=120)

    # Live price (short TTL cache)
    try:
        live = fetcher.get_price("EUR", "USD")
        print(f"Live: {live}")
    except Exception as e:
        print(f"Live price failed: {e}")

    # Test free sources
    try:
        eur_usd = fetcher.fetch_exchangerate_host_live("EUR", "USD")
        print(f"ExchangeRate.host: {eur_usd}")
    except Exception as e:
        print(f"ExchangeRate.host failed: {e}")
