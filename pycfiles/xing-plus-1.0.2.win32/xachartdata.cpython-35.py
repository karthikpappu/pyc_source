# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\xing\xachartdata.py
# Compiled at: 2016-01-16 19:19:25
# Size of source mod 2**32: 8917 bytes
from pandas import DataFrame, Series
from talib import abstract
from xing.xaquery import Query

class Chartdata:
    __doc__ = '차트 데이터를 추출 및 관리하고, 이를 통해 보조지표를 생성하는 클래스\n\n        :param shcode: 종목 코드\n        :type shcode: str\n\n    ::\n\n        chart = Chartdata("012510")\n    '
    DAY = 99997
    WEEK = 99998
    MONTH = 99999

    def __init__(self, shcode):
        self._shcode = shcode
        self._data = {}

    def _parseParam(self, param):
        p = {}
        for k, v in param.items():
            if isinstance(v, (list, tuple)):
                if len(v) < 2:
                    p[k] = [
                     v[0], '99999999']
                else:
                    p[k] = v[:2]
            else:
                p[k] = [
                 v, '99999999']

        return p

    def load(self, param):
        """차트 데이터를 조회하여 누적한다.

            :param param: 조회할 차트 종류(분,일,월,주)와 조회할 기간
            :type param: object { 조회할차트정보 : [시작일(yyyymmdd), 종료일(yyyymmdd)]}
            :return: self

            .. note:: 한번 load한 데이터는 load는 clean 하지 않는 이상, 기존 데이터를 갱신하지 않고, 존재하지 않는 기간만 추가한다.

            ::

                chart = Chartdata("012510")
                chart.load({
                    Chartdata.DAY : [ startdate , enddate ]
                    Chartdata.WEEK : [ startdate , enddate ]
                    Chartdata.MONTH : [ startdate ]
                    1 : startdate
                })
        """
        p = self._parseParam(param)
        for k, v in p.items():
            if k in self._data:
                lastDate = self._data[k].iloc[(len(self._data[k]) - 1)]['date']
                if lastDate >= p[k][1]:
                    print('skip...', lastDate, p[k][1])
                else:
                    df = self._data[k][(self._data[k].date != lastDate)]
                    appendDf = self._query(k, lastDate, p[k][1])
                    dfLen = len(df)
                    for i in range(len(appendDf)):
                        for col in list(appendDf.columns.values):
                            df.set_value(dfLen + i, col, appendDf.get_value(i, col))

                    self._data[k] = df
            else:
                self._data[k] = self._query(k, p[k][0], p[k][1])
            print(self._data[k])

        return self

    def _query(self, type, startdate='', enddate='99999999'):
        chartType = self._getChartType(type)
        if chartType == 0:
            df = Query('t8412', True).request({'InBlock': {'shcode': self._shcode, 
                         'qrycnt': 2000, 
                         'comp_yn': 'Y', 
                         'sdate': startdate, 
                         'edate': enddate, 
                         'ncnt': type}}, {'OutBlock': ('cts_date', 'cts_time'), 
             'OutBlock1': DataFrame(columns=('date', 'time', 'open', 'high', 'low', 'close', 'jdiff_vol', 'sign'))})['OutBlock1']
        else:
            df = Query('t8413', True).request({'InBlock': {'shcode': self._shcode, 
                         'gubun': chartType, 
                         'qrycnt': 2000, 
                         'sdate': startdate, 
                         'edate': enddate, 
                         'comp_yn': 'Y'}}, {'OutBlock': ('cts_date', ), 
             'OutBlock1': DataFrame(columns=('date', 'open', 'high', 'low', 'close', 'jdiff_vol', 'sign'))})['OutBlock1']
        return df

    def _getChartType(self, type):
        chartType = 0
        if type >= Chartdata.DAY:
            if type == Chartdata.DAY:
                chartType = 2
            elif type == Chartdata.WEEK:
                chartType = 3
        elif type == Chartdata.MONTH:
            chartType = 4
        return chartType

    def process(self, param):
        """load에 의해 누적된 데이터를 기준으로 보조 지표를 계산한다.

            :param param: 보조지표 정보를 전달한다.
            :type param: object { "SMA" : [], "BBANDS" : [], "ATR" : number, "STOCH" : [], "MACD" : [], "RSI" : number }

            .. warning:: process는 load 이후에 호출되어야 의미가 있다.

        ::

            chart.process({
                "SMA" : [ 5, 10, 20, 60],   # 이동평균선
                "BBANDS" : [20, 2], #볼랜져 밴드 period, 승수
                "ATR" : 14, #ATR 지표 period
                "STOCH" : [ 5, 3, 0],   #스토케스틱 K period, D period, D type
                "MACD" : [12, 26, 9],  # short, long, signal
                "RSI" : 14,  # period
            })
        """
        for k, v in self._data.items():
            data = {'open': v['open'].astype(float), 
             'high': v['high'].astype(float), 
             'low': v['low'].astype(float), 
             'close': v['close'].astype(float), 
             'volume': v['jdiff_vol'].astype(float)}
            if 'SMA' in param:
                for p in param['SMA']:
                    v['SMA' + str(p)] = Series(abstract.SMA(data, p), index=v.index)

            if 'BBANDS' in param:
                temp = abstract.BBANDS(data, param['BBANDS'][0], param['BBANDS'][1], param['BBANDS'][1])
                v['BBANDS-UPPER'] = temp[0]
                v['BBANDS-MIDDLE'] = temp[1]
                v['BBANDS-LOWER'] = temp[2]
            if 'STOCH' in param:
                temp = abstract.STOCH(data, param['STOCH'][0], param['STOCH'][1], param['STOCH'][2])
                v['STOCH-K'] = temp[0]
                v['STOCH-D'] = temp[1]
            if 'ATR' in param:
                v['ATR'] = Series(abstract.ATR(data, param['ATR']), index=v.index)
            if 'MACD' in param:
                temp = abstract.MACD(data, param['MACD'][0], param['MACD'][1], param['MACD'][2])
                v['MACD-OUT'] = temp[0]
                v['MACD-SIGNAL'] = temp[1]
                v['MACD-HIST'] = temp[2]
            if 'RSI' in param:
                v['RSI'] = Series(abstract.RSI(data, param['RSI']), index=v.index)

        return self

    def get(self, type=None):
        """load와 process에 의해 처리된 데이터를 반환한다.

            :param type: 차트의 종류 (예, 일,주,월,1분, 5분, ...). 기본값은 None
            :type type: str, int
            :return: 데이터를 반환한다.
            :rtype: DataFrame, None

        ::

            chart.get() # 전체 데이터를 반환한다.
            chart.get(5)    # 5분 차트 데이터를 반환한다.
            chart.get(Chartdata.DAY)    # 일 차트 데이터를 반환한다.
        """
        if type:
            if type in self._data:
                return self._data[type]
            else:
                return
        else:
            return self._data

    def clean(self, type=None):
        """load와 process에 의해 처리된 데이터를 삭제한다.

            :param type: 차트의 종류 (예, 일,주,월,1분, 5분, ...). 기본값 None
            :type type: str, int

        ::

            chart.clean() # 전체 데이터를 삭제한다.
            chart.clean(5)    # 5분 차트 데이터를 삭제한다.
            chart.get(Chartdata.DAY)    # 일 차트 데이터를 삭제한다.
        """
        if type and type in self._data:
            self._data[type] = None
        else:
            self._data = {}