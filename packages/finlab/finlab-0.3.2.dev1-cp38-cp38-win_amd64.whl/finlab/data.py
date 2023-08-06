import os
import re
import time
import json
import pickle
import logging
import datetime
import numpy as np
import pandas as pd
from io import BytesIO
from finlab.utils import check_version, requests
from finlab import login, get_token, dataframe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheSystem():

  def __init__(self):
    self.cache = {}
    self.cache_time = {}
    self.stock_names = {}

  @staticmethod
  def expired(cache_time):
    now = datetime.datetime.now(datetime.timezone.utc)
    pm7 = datetime.datetime(now.year, now.month, now.day, hour=11, tzinfo=datetime.timezone.utc)

    if now > pm7 and cache_time < pm7:
      return True
    if now - cache_time > datetime.timedelta(hours=12):
      return True
    return False

  def exists(self, dfname):
    now = datetime.datetime.now(datetime.timezone.utc)

    if (dfname in self.cache) and not self.expired(self.cache_time[dfname]):
      return True
    return False

  def save_cache(self, dfname, df):
    now = datetime.datetime.now(datetime.timezone.utc)
    self.cache[dfname] = df
    self.cache_time[dfname] = now

  def cache_stock_names(self, new_stock_names):
    self.stock_names = {**self.stock_names, **new_stock_names}

  def get_cache(self, dfname):
    return self.cache[dfname]

  def get_stock_names(self):
    return self.stock_names

class FileCacheSystem():
  def __init__(self, path='./finlab_db'):
    self.path = path
    self.cache = {}
    self.stock_names = None

    if not os.path.isdir(path):
      os.mkdir(path)
      pickle.dump({}, open(os.path.join(path, 'timestamp.pkl'), 'wb'))
      pickle.dump({}, open(os.path.join(path, 'stock_names.pkl'), 'wb'))
    else:
      self.stock_names = pickle.load(open(os.path.join(self.path, 'stock_names.pkl'), 'rb'))

  def save_cache(self, dfname, df):
    file_path = os.path.join(self.path, dfname + '.pickle')
    df.to_pickle(file_path)
    self.cache[dfname] = df

  def get_cache(self, dfname):

    if dfname in self.cache:
      return self.cache[dfname]

    file_path = os.path.join(self.path, dfname + '.pickle')
    if os.path.isfile(file_path):
      ret = pd.read_pickle(file_path)
      self.cache[dfname] = ret
      return ret
    return None

  def exists(self, dfname):

    file_path = os.path.join(self.path, dfname + '.pickle')
    if not os.path.isfile(file_path):
      return False

    modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    timezone_offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    modify_time = modify_time + datetime.timedelta(hours=timezone_offset / 60 / 60 * -1 )
    modify_time = modify_time.replace(tzinfo=datetime.timezone.utc)

    if CacheSystem.expired(modify_time):
      return False

    return True

  def cache_stock_names(self, new_stock_names):
    stock_names = pickle.load(open(os.path.join(self.path, 'stock_names.pkl'), 'rb'))
    stock_names = {**stock_names, **new_stock_names}
    pickle.dump(stock_names, open(os.path.join(self.path, 'stock_names.pkl'), 'wb'))
    self.stock_names = stock_names

  def get_stock_names(self):
    if self.stock_names is not None:
      return self.stock_names

    stock_names = pickle.load(open(os.path.join(self.path, 'stock_names.pkl'), 'rb'))
    self.stock_names = stock_names
    return stock_names

cs = CacheSystem()
universe_stocks = set()

def set_cache_system(cs_):
  global cs
  cs = cs_

class universe():
    def __init__(self, market='ALL', category='ALL'):
        self.market = market
        self.category = category

    def __enter__(self):
        set_universe(self.market, self.category)

        return self
    def __exit__(self, type, value, traceback):
        set_universe()

def set_universe(market='ALL', category='ALL'):
  """Set subset of stock ids when retrieve data using data.get or data.indicator

  Args:
      market (str): universe market type. ex: 'ALL', 'TSE', 'OTC', 'TSE_OTC', 'ETF'
      category (str): stock categories, can be either a string or a list. ex: '光電業', '其他', '其他電子業',
 '化學工業', '半導體', '塑膠工業', '存託憑證', '建材營造', '文化創意業', '橡膠工業', '水泥工業',
 '汽車工業', '油電燃氣業', '玻璃陶瓷', '生技醫療', '生技醫療業', '紡織纖維', '航運業', '觀光事業', '貿易百貨',
 '資訊服務業', '農業科技', '通信網路業', '造紙工業', '金融', '鋼鐵工業', '電器電纜', '電子商務',
 '電子通路業', '電子零組件', '電機機械', '電腦及週邊', '食品工業'

  Returns:
      None

  """

  categories = get('security_categories')

  market_match = pd.Series(True, categories.index)

  if market == 'ALL':
    pass
  elif market == 'TSE':
    market_match = categories.market == 'sii'
  elif market == 'OTC':
    market_match = categories.market == 'otc'
  elif market == 'TSE_OTC':
    market_match = (categories.market == 'sii') | (categories.market == 'otc')
  elif market == 'ETF':
    market_match = categories.market == 'other_securities'

  category_match = pd.Series(True, categories.index)

  if category == 'ALL':
    pass
  else:
    if isinstance(category, str):
      category = [category]

    matched_categories = set()
    all_categories = set(categories.category)
    for ca in category:
        matched_categories |= (set([c for c in all_categories if isinstance(c, str) and re.search(ca, c)]))
    category_match = categories.category.isin(matched_categories)

  global universe_stocks
  universe_stocks = set(categories.stock_id[market_match & category_match])


def get(dataset, use_cache=True):
    check_version()

    global universe_stocks

    not_available_universe_stocks = ['benchmark_return', 'institutional_investors_trading_all_market_summary',
                                     'margin_balance', 'intraday_trading_stat',
                                     'stock_index_price', 'stock_index_vol',
                                     'taiex_total_index', 'broker_info',
                                     'rotc_monthly_revenue', 'rotc_price',
                                     'world_index', 'rotc_broker_trade_record',
                                     'us_price', 'us_sp500',
                                     'us_tickers', 'security_categories',
                                     ]

    # use cache if possible
    if cs.exists(dataset):
        ret = cs.get_cache(dataset)
        if dataset.split(':')[0] in not_available_universe_stocks:
            return ret
        if ':' in dataset:
            return ret if not universe_stocks else ret[ret.columns.intersection(universe_stocks)]
        else:
            if 'stock_id' in ret.columns:
                return ret if not universe_stocks else ret[ret['stock_id'].isin(universe_stocks)]
            else:
                return ret

    api_token = get_token()

    # request for auth url
    request_args = {
        'api_token': api_token,
        'bucket_name': 'finlab_tw_stock_item',
        'blob_name': dataset.replace(':', '#') + '.feather'
    }

    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_generate_data_url_limit_test'
    res = requests.post(url, request_args)
    url_data = res.json()

    if 'quota' in url_data:
        logger.info(f'{dataset} -- Daily data usage: {url_data["quota"]:.1f} / {url_data["limit_size"]} MB')

    if 'error' in url_data:

        if url_data['error'] in [
            'request not valid',
            'User not found',
            'api_token not valid',
            'api_token not match', ]:
            login()
            return get(dataset, use_cache)

        logger.error(f"**Error: {url_data['error']}")
        return None

    assert 'url' in url_data

    res = requests.get(url_data['url'])
    df = pd.read_feather(BytesIO(res.content))

    # set date as index
    if 'date' in df:
        df.set_index('date', inplace=True)

        table_name = dataset.split(':')[0]
        if table_name in ['monthly_revenue', 'rotc_monthly_revnue', 'financial_statement', 'fundamental_features']:
            if isinstance(df.index[0], pd.Timestamp):
                close = get('price:收盤價')
                df.index = df.index.map(
                    lambda d: d if len(close.loc[d:]) == 0 or d < close.index[0] else close.loc[d:].index[0])

        # if column is stock name
        if (df.columns.str.find(' ') != -1).all():

            # remove stock names
            df.columns = df.columns.str.split(' ').str[0]

            # combine same stock history according to sid
            check_numeric_dtype = pd.api.types.is_numeric_dtype(df.values)
            if check_numeric_dtype:
                df = df.transpose().groupby(level=0).mean().transpose()

        df = dataframe.FinlabDataFrame(df)

        if table_name in ['monthly_revenue', 'rotc_monthly_revenue']:
            df = df._index_date_to_str_month()
        elif table_name in ['financial_statement', 'fundamental_features']:
            df = df._index_date_to_str_season()

    # save cache
    if use_cache:
        cs.save_cache(dataset, df)

    if dataset.split(':')[0] in not_available_universe_stocks:
        return df

    if ':' in dataset:
        return df if not universe_stocks else df[df.columns.intersection(universe_stocks)]

    if 'stock_id' in df.columns:
        return df if not universe_stocks else df[df['stock_id'].isin(universe_stocks)]

    return df



def indicator(indname, adjust_price=False, resample='D', **kwargs):
  
    package = None

    try:
      from talib import abstract
      func = getattr(abstract, indname)
      package = 'talib'
    except:
      try:
        import pandas_ta
        func = lambda df, **kwargs: getattr(df.ta, indname)(**kwargs)
        package = 'pandas_ta'
      except:
        raise Exception("Please install TA-Lib or pandas_ta to get indicators.")

    if adjust_price:
        close  = get('etl:adj_close')
        open_  = get('etl:adj_open')
        high   = get('etl:adj_high')
        low    = get('etl:adj_low')
        volume = get('price:成交股數')
    else:
        close  = get('price:收盤價')
        open_  = get('price:開盤價')
        high   = get('price:最高價')
        low    = get('price:最低價')
        volume = get('price:成交股數')

    if resample.upper() != 'D':
        close = close.resample(resample).last()
        open_ = open_.resample(resample).first()
        high = high.resample(resample).max()
        low = low.resample(resample).min()
        volume = volume.resample(resample).sum()

    dfs = {}
    default_output_columns = None
    for key in close.columns:
        
        prices = {'open':open_[key].ffill(),
                  'high':high[key].ffill(),
                  'low':low[key].ffill(),
                  'close':close[key].ffill(),
                  'volume':volume[key].ffill()}
        
        if package == 'pandas_ta':
          prices = pd.DataFrame(prices)

        s = func(prices, **kwargs)
        
        if isinstance(s, list):
          s = {i:series for i, series in enumerate(s)}
          
        if isinstance(s, np.ndarray):
          s = {0: s}
        
        if isinstance(s, pd.Series):
          s = {0: s.values}
          
        if isinstance(s, pd.DataFrame):
          s = {i: series.values for i, series in s.items()}
        
        if default_output_columns is None:
            default_output_columns = list(s.keys())

        for colname, series in s.items():
            if colname not in dfs:
              dfs[colname] = {}
            dfs[colname][key] = series if isinstance(series, pd.Series) else series  

    newdic = {}
    for key, df in dfs.items():
        newdic[key] = pd.DataFrame(df, index=close.index)
        
    ret = [newdic[n] for n in default_output_columns]
    ret = [d.apply(lambda s:pd.to_numeric(s, errors='coerce')) for d in ret]
    
    if len(ret) == 1:
        return dataframe.FinlabDataFrame(ret[0])

    return tuple([dataframe.FinlabDataFrame(df) for df in ret])


def get_strategies(api_token=None):
    if api_token is None:
        api_token = get_token()

    request_args = {
        'api_token': api_token,
    }

    url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_get_strategies'
    response = requests.get(url, request_args)
    status_code = response.status_code
    if status_code in [400, 401]:
        logger.error("The authentication code is wrong or the account is not existed."
                     "Please input right authentication code or register account ")
        return {}
    try:
        return json.loads(response.text)
    except:
        pass

    return response.text

