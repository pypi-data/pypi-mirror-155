import abc


class abstract_provider():

  datalen = 0

  @abc.abstractmethod
  def provide_daily_bar():
    pass

  def fill_return(slef, records):
    """
    For data source with only 'close', we add a return column.
    return = (closeT2 - closeT1) / closeT1
    """
    for index, record in enumerate(records):
      record['close'] = float(record['close'])
      if index == 0:
        record['return'] = None
        continue
      pre_record = records[index - 1]
      returns = (record['close'] - pre_record['close']) / pre_record['close']
      record['return'] = returns
