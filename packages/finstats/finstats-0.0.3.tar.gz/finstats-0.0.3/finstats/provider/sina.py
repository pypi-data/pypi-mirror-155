

import json
import requests
import pandas as pd
from .abstract_provider import abstract_provider

daily_bar_url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&datalen={}&scale={}&ma={}'

class sina_provider(abstract_provider):
  
  def provide_daily_bar(
    self,
    symbol,
    datalen=1023,
    scale=240,
    ma=5,
  ):
    """
    Data source provided by Sina HTTP API (China A share only)
    examples:
    https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh510300&scale=240&ma=5&datalen=1023
    
    Parameters
    ----------
    symbol: stock code
    scale: periods. 5、15、30、60,120,240
    ma: moving average. 5、10、20、60,120
    datalen: number of records fetched
    """
    raw = requests.get(daily_bar_url.format(symbol, datalen, scale, ma))
    raw.encoding='utf-8'
    records = json.loads(raw.text)
    self.fill_return(records)
    ret = pd.DataFrame(records)
    ret['close'] = ret['close'].astype(float)
    return ret



