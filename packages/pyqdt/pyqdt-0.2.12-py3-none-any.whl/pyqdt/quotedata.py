# -*- coding: utf-8 -*-
import multiprocessing
import os, sys
from functools import lru_cache, wraps

import threading

import math
from inspect import isfunction

import numpy as np
import pandas as pd

from .technical_analysis import *
from .utils import *

if check_sharedmemory_support():
    from multiprocessing import shared_memory


def assert_quote_init(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        data_path = QuoteData().get_data_path()
        if not data_path or not os.path.exists(data_path):
            print("QuoteData is not initialized.")
        else:
            return func(*args, **kwargs)

    return _wrapper


def _rehabilitation_worker(start=None, end=None, fq_date=None, fq_vol=False, xrxd=None, precision=2
                           , data=None, shm_name=None, shape=None):
    if not xrxd:
        return

    if shm_name:
        shm = shared_memory.SharedMemory(name=shm_name)
        data = np.ndarray(shape, dtype=np.float64, buffer=shm.buf)

    if not start:
        start = 0
    if not end:
        end = len(data)
    if not fq_date:
        fq_date = pd.Timestamp(time.localtime('%Y-%m-%d'))

    values = data[start:end]
    n = data.shape[1] - 1 - (1 if fq_vol else 0)

    for row in xrxd:
        ts_date = row['date']
        r = 10 / (10 + (row['dividend_ratio'] if not math.isnan(row['dividend_ratio']) else 0) + (
            row['transfer_ratio'] if not math.isnan(row['transfer_ratio']) else 0))
        v = (row['bonus_ratio'] if not math.isnan(row['bonus_ratio']) else 0) / 10

        # 前复权处理
        if ts_date <= fq_date:
            #   c = data[data['datetime'] < ts_date]
            c = np.where(values[:, 0] < ts_date.value)
            values[c, 1: 1 + n] = np.round((values[c, 1: 1 + n] - v) * r, precision)
            if fq_vol:
                values[c, -1] = np.round(values[c, -1] / r)
        # 后复权处理
        else:
            #    c = data[data['datetime'] >= ts_date]
            c = np.where(values[:, 0] >= ts_date.value)
            values[c, 1: 1 + n] = np.round(values[c, 1: 1 + n] / r + v, precision)
            if fq_vol:
                values[c, -1] = np.round(values[c, -1] * r)

    if shm_name:
        shm.close()


def _arithmetic_worker(df, func, kw):
    arithmetic_reset()
    return df.apply(func, **kw)


class QuoteData(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """单例模式-线程保护"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, data_path=None):
        """本地行情数据类

        参数:
            data_path: 数据目录

        """
        if not hasattr(self, '_data_path'):
            self._data_path = ''
        if data_path:
            self.init(data_path)
        if not hasattr(self, '_options'):
            self._options = {
                'debug': False,
                'refer_num': 200,
                'multi_process': False
            }

    @assert_quote_init
    @lru_cache(maxsize=None, typed=True)
    def _fetch_data(self, filename, date_columns=None):
        """获取数据

        参数:
            filename: 数据文件名
            dtype: 字段类型
            parse_dates: 日期字段

        返回值: DataFrame

        """

        data_file = os.path.join(self._data_path, filename)
        if not os.path.exists(data_file):
            return

        result = None
        extname = os.path.splitext(filename)[-1][1:].lower()
        if extname == 'csv':
            if not date_columns:
                parse_dates = False
            elif type(date_columns) is list:
                parse_dates = date_columns
            elif type(date_columns) is tuple:
                parse_dates = list(date_columns)
            elif type(date_columns) is str:
                parse_dates = [date_columns]
            else:
                raise ValueError('date_columns is error.')
            result = pd.read_csv(data_file, dtype={'code': str}, parse_dates=parse_dates)
        elif extname == 'txt':
            with open(data_file, 'r') as f:
                result = f.readlines()
        return result

    def init(self, data_path):
        """初始化

        参数:
            data_path: 数据目录

        """
        if not data_path or not os.path.exists(data_path):
            raise Exception('initialization failed. data_path %s is not exists.' % data_path)
        self._data_path = data_path

    def get_data_path(self):
        """获取数据目录

        返回值: 数据目录

        """
        return self._data_path

    def get_option(self, name):
        """获取可选项值

        参数:
            name: 可选项名

        返回值:
            可选项值

        """
        if name not in self._options:
            raise ValueError('option %s is not exists.' % name)

    def set_option(self, name, value):
        """设置可选项值

        参数:
            name: 可选项名
            value: 可选项值

        """
        if name not in self._options:
            raise ValueError('option %s is not exists.' % name)
        self._options[name] = value

    @classmethod
    def _get_price_precision(cls, security) -> int:
        """获取价格精度

        参数:
            security: 字符串或列表

        返回值: 精度或精度列表

        """
        if type(security) is str:
            n = 2
            p = security.find('.')
            if p >= 0:
                code = security[:p]
                exch = security[p + 1:]
                if exch == 'SZ':
                    if code[0] == '1':
                        n = 3
                    elif code[0:3] == '399' or code[0:4] == '9000':
                        n = 4
                elif exch == 'SH':
                    if code[0] == '5':
                        n = 3
                    elif code[0:3] == '000' or code[0:4] == '1000':
                        n = 4
            return n
        elif type(security) is list:
            r = []
            for s in security:
                r.append(cls._get_price_precision(s))
            return r

    @classmethod
    def _parse_period_str(cls, period) -> (str, int):
        """分析周期字串

        参数:
            period: 周期

        返回值: 类型，间隔

        """
        if period in ['day', 'daily', '1d', 'week', '1w', 'mon', 'month', '1M', 'season', 'year']:
            period_type = 'day'
            period_step = 0
        elif period[-1] == 'm' and period[:-1].isdecimal():
            period_type = 'mn1'
            period_step = int(period[:-1])
        elif period[0:2] == 'mn' and period[2:].isdecimal():
            period_type = 'mn1'
            period_step = int(period[2:])
        else:
            raise Exception('period is invalid.')
        return period_type, period_step

    def _parse_period_start(self, period, date, count):
        """分析周期开始时间

        参数:
            period: 周期
            date: 参考时间
            count: 数量

        返回值:
            参考时间 - count 个周期后的开始时间

        """
        year_minimum = 1990
        start = datetime.datetime(2005,1,1).date()
        if period in ['day', 'daily', '1d']:
            trade_list = self.get_trade_days(end_date=date, count=count)
            if trade_list:
                start = trade_list[0].timetuple()
        elif period in ['week', '1w']:
            trade_list = self.get_trade_days(end_date=date, count=count * 5)
            if trade_list:
                week_maps = [x.isocalendar()[0] * 100 + x.isocalendar()[1] for x in trade_list]
                week_list = list(set(week_maps))
                week_list.sort()
                w = week_list[-count]
                start = trade_list[week_maps.index(w)].timetuple()
        elif period in ['mon', 'month', '1M']:
            y = date.tm_year
            m = date.tm_mon + 1 - count
            while m <= 0:
                y -= 1
                m += 12
            y = max(y, year_minimum)
            start = datetime.datetime(y, m, 1).timetuple()
        elif period == 'season':
            y = date.tm_year
            s = (date.tm_mon - 1) // 3 + 1 - count
            while s < 0:
                y -= 1
                s += 4
            y = max(y, year_minimum)
            start = datetime.datetime(y, s * 3 + 1, 1).timetuple()
        elif period == 'year':
            y = date.tm_year + 1 - count
            y = max(y, year_minimum)
            start = datetime.datetime(y, 1, 1).timetuple()
        else:
            t, n = self._parse_period_str(period)
            if t != 'mn1':
                return
            days = math.ceil(count * n / 240)
            trade_list = self.get_trade_days(end_date=date, count=days)
            if trade_list:
                start = trade_list[0].timetuple()
        return start

    def trace(self, *args):
        if self._options.get('debug', False):
            print(time.strftime('%Y-%m-%d %H:%M:%S'), *args)

    @assert_quote_init
    def execute_rehabilitation(self, data, fq='pre', fq_vol=False, start_date=None, end_date=None
                               , columns=None, inplace=False, skip_sort=False) -> pd.DataFrame:
        """执行复权操作

        复权逻辑：
            data 为 DataFrame 行情数据，基中 datetime 作为时间字段识别出 start_date 和 end_date
            当 fq == 'pre' 时，复权参考日为 end_date
            当 fq == 'post' 时，复权参考日为 start_date
            当 除权除息日 <= 复权参考日 时，所有 < 除权除息日 的数据进行前复权
            当 除权除息日 > 复权参考日 时，所有 >= 除权除息日 的数据进行后复权
            start_date 与 end_date 指除权除息发生时间，仅复权该时间段内的行情数据

        参数:
            data: 输入数据
            fq: 复权方式或复权参考日
            fq_vol: 是否复权成交量：默认值 False
            start_date: 复权开始日，默认值为 data.datetime 的最小值
            end_date: 复权结束日，默认值为 data.datetime 的最大值
            columns: 需要复权的字段列表
            inplace: 是否复盖输入数据，默认值 False
            skip_sort: 跳过排序，默认值 False；传入的 data 必须符合 code, datetime 排序，否则处理结果会有误

        返回值: 输出数据

        """
        proc_start = time.time()
        default_cols_px = ['open', 'close', 'high', 'low', 'pre_close', 'high_limit', 'low_limit']
        default_cols_vm = ['volume']

        df = data if inplace else data.copy()
        if not fq or len(df) == 0:
            return df
        if not columns:
            columns = df.columns

        security = list(set(df['code'].tolist()))
        start_date = formatter_st(start_date, min(df['datetime']).strftime('%Y-%m-%d'))
        end_date = formatter_st(end_date, max(df['datetime']).strftime('%Y-%m-%d'))
        self.trace('rehabilitate from %s to %s'
                   % (time.strftime('%Y-%m-%d', start_date), time.strftime('%Y-%m-%d', end_date)))

        if fq == 'pre':
            fq_date = pd.Timestamp(time.strftime('%Y-%m-%d', end_date))
        elif fq == 'post':
            fq_date = pd.Timestamp(time.strftime('%Y-%m-%d', start_date))
        else:
            fq_date = pd.Timestamp(time.strftime('%Y-%m-%d', formatter_st(fq)))

        xrxd = self.get_security_xrxd(security=security, start_date=start_date, end_date=end_date)
        if xrxd is None:
            return df
        xrxd.sort_values(by=['code', 'date'], inplace=True)
        xrxd.set_index('code', drop=True, inplace=True)

        cols_px = [x for x in list(df.columns) if x in columns and x in default_cols_px]
        cols_vm = [x for x in list(df.columns) if x in columns and x in default_cols_vm] if fq_vol else []
        if not cols_px and not cols_vm:
            return df
        self.trace('exec', time.time() - proc_start)

        if not skip_sort:
            df.sort_values(by=['code', 'datetime'], axis=0, ascending=True, inplace=True)
            df.reset_index(drop=True, inplace=True)

        shape = (len(df), 1 + len(cols_px) + len(cols_vm))
        multi_process = self._options.get('multi_process', False)
        if multi_process and not check_sharedmemory_support():
            multi_process = False
            self.trace('shared memory not support, multi-process disabled')

        if multi_process:
            self.trace('rehabilitation within multi-process')

            shm = shared_memory.SharedMemory(create=True, size=shape[0] * shape[1] * 8)
            np_data = np.ndarray(shape=shape, dtype=np.float64, buffer=shm.buf)
            np_data[:, 0] = df['datetime'].values.astype('float')
            np_data[:, 1:] = df[cols_px + cols_vm].values
            self.trace('exec', time.time() - proc_start)

            operate_params = []
            for code, group in df.groupby(by='code'):
                if len(group) == 0 or code not in xrxd.index:
                    continue
                kw = {'start': group.index[0], 'end': group.index[-1] + 1, 'fq_date': fq_date, 'fq_vol': fq_vol
                    , 'xrxd': xrxd.loc[[code]].to_dict(orient='records'), 'precision': self._get_price_precision(code)
                    , 'shm_name': shm.name, 'shape': shape}
                operate_params.append(kw)

            tasks = []
            pool = multiprocessing.Pool(processes=multi_process if type(multi_process) is int else None)
            for kw in operate_params:
                tasks.append(pool.apply_async(_rehabilitation_worker, kwds=kw))
            pool.close()
            pool.join()

            df[cols_px + cols_vm] = np_data[:, 1:]
            shm.close()
            shm.unlink()
        else:
            np_data = np.empty(shape=shape, dtype=np.float64)
            np_data[:, 0] = df['datetime'].values.astype('float')
            np_data[:, 1:] = df[cols_px + cols_vm].values
            for code, group in df.groupby(by='code'):
                if len(group) == 0 or code not in xrxd.index:
                    continue
                # self.trace('rehabilitate %s' % code)
                kw = {'start': group.index[0], 'end': group.index[-1] + 1, 'fq_date': fq_date, 'fq_vol': fq_vol
                    , 'xrxd': xrxd.loc[[code]].to_dict(orient='records'), 'precision': self._get_price_precision(code)
                    , 'data': np_data}
                _rehabilitation_worker(**kw)
            self.trace('exec', time.time() - proc_start)
            df[cols_px + cols_vm] = np_data[:, 1:]
            self.trace('exec', time.time() - proc_start)

        self.trace('exec', time.time() - proc_start)
        return df

    @assert_quote_init
    def execute_technical_analysis(self, data, indications, prefix=None
                                   , lowercase=True, inplace=False, skip_sort=False) -> pd.DataFrame:
        """执行技术指标运算

        参数:
            data: 输入数据
            indications: 技术指标及参与，单个或List
                         单个指标：（'MA', 5)，
                         多个指标：[('MA', 5), ('KDJ', 9, 3, 3)]
                         可省略参数：['MA', 'KDJ']
            prefix: 指标名称前缀，默认值 None
            lowercase: 指标名称是否小写，默认值 True
            inplace: 是否复盖输入数据，默认值 False
            skip_sort: 跳过排序，默认值 False；传入的 data 必须符合 code, datetime 排序，否则处理结果会有误

        返回值: 输出数据

        """
        proc_start = time.time()
        df = data if inplace else data.copy()

        if not skip_sort:
            df.sort_values(by=['code', 'datetime'], axis=0, ascending=True, inplace=True)
            df.reset_index(drop=True, inplace=True)

        operate_params = []
        cols_techansi = []
        indications = formatter_list(indications)
        for v in indications:
            v = [v] if type(v) is str or isfunction(v) else list(v)
            c = v.pop(0)
            if isfunction(c):
                func = c
                c = func.__name__
            else:
                func = globals().get(c)
            if not func:
                print('%s is not exists.' % c)
                continue
            if not hasattr(func, '__wrapped__'):
                print('%s is unavailable.' % c)
                continue
            f_wrapped = getattr(func, '__wrapped__')
            f_args = [x for x in f_wrapped.__code__.co_varnames[:f_wrapped.__code__.co_argcount]]
            if len(f_args) > 0 and f_args[0] == 'X' and len(v) > 0 and type(v[0]) is not str:
                f_args.pop(0)
            kw = dict(axis=1)
            for i in range(len(v)):
                if i >= len(f_args):
                    break
                kw[f_args[i]] = v[i]

            # 获取返回值字段名
            cols_fn = arithmetic_returns(f_wrapped, v)
            if not cols_fn:
                cols_fn = c
            if type(cols_fn) is str:
                cols_fn = [cols_fn]
            cols_fn = [x for x in cols_fn]
            if not cols_fn:
                raise Exception('columns name not support.')

            # 字段重名处理
            cols_nums = dict()
            for x in cols_techansi:
                arr = x.split('_')
                if len(arr) > 1 and arr[-1].isdigit():
                    y = int(arr[-1])
                    x = '_'.join(arr[:-1])
                    if y >= cols_nums[x]:
                        cols_nums[x] = y + 1
                else:
                    cols_nums[x] = 1
            for i in range(len(cols_fn)):
                x = cols_fn[i]
                if x in cols_nums.keys():
                    cols_fn[i] = x + '_' + str(cols_nums[x])
            '''
            if [x for x in cols_fn if x in cols_techansi]:
                c_arr = [str(x) for x in v]
                if len(cols_fn) > 1:
                    c_arr.insert(0, c)
                    cols_fn = ['_'.join(c_arr) + '_' + x for x in cols_fn]
                elif len(cols_fn) == 1:
                    if cols_fn[0] == c:
                        c_arr.insert(0, c)
                        cols_fn = ['_'.join(c_arr)]
                    else:
                        c_arr.insert(0, cols_fn[0])
                        cols_fn = ['_'.join(c_arr)]
            '''

            # 加入操作参数
            operate_params.append((cols_fn, func, kw))
            cols_techansi.extend([x for x in cols_fn if x not in cols_techansi])

        # 提交指标函数处理
        multi_process = self._options.get('multi_process', False)
        if multi_process:
            self.trace('arithmetic within multi-process')

            tasks = []
            pool = multiprocessing.Pool(processes=multi_process if type(multi_process) is int else None)
            for code, group in df.groupby(by='code'):
                for cols_fn, func, kw in operate_params:
                    tasks.append((cols_fn, pool.apply_async(_arithmetic_worker, (group, func, kw))))
            pool.close()
            pool.join()

            for x in cols_techansi:
                df[x] = np.nan
            for cols_fn, result in tasks:
                se = result.get()
                se.dropna(inplace=True)
                if not se.empty:
                    df.loc[se.index, cols_fn] = se.tolist() if len(cols_fn) > 1 else se
        else:
            for x in cols_techansi:
                df[x] = np.nan
            for cols_fn, func, kw in operate_params:
                se = _arithmetic_worker(df, func, kw)
                se.dropna(inplace=True)
                if not se.empty:
                    df.loc[se.index, cols_fn] = se.tolist() if len(cols_fn) > 1 else se

        #指标名称-变更前缀或转换大小写
        cols_maps = dict()
        for x in df.columns:
            if x not in cols_techansi:
                continue
            y = x
            y = y.lower() if lowercase else y.upper()
            if prefix:
                y = prefix + y
            if x != y:
                cols_maps[x] = y
        df.rename(columns=cols_maps, inplace=True)

        # self.trace('exec', time.time() - proc_start)
        return df

    @assert_quote_init
    def get_quote_date(self) -> datetime.date:
        """获取行情日期

        返回值:
            最新行情日期

        """
        filename = 'ckvalid.txt'
        txt = self._fetch_data(filename)
        if not txt:
            raise Exception('fetch data from %s failed.' % filename)

        result = dict()
        for s in txt:
            s = s.strip()
            if not s:
                continue
            p = s.find('=')
            if p <= 0:
                continue
            k = s[0:p].strip()
            v = s[p + 1:].strip()
            if not k or not v:
                continue
            result[k] = v
        # self.trace(result)
        stime = result.get('last_date')
        if not stime:
            raise Exception('the quote_data not found.')
        last_date = datetime.datetime.strptime(stime, '%Y-%m-%d').date()
        tdays = self.get_trade_days(end_date=last_date, count=1)
        if not tdays:
            raise Exception('trade-days is empty.')
        return tdays[0]

    @assert_quote_init
    def get_trade_days(self, start_date=None, end_date=None, count=None) -> list:
        """获取交易日列表

        参数:
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            交易日列表；类型 [datetime.date]

        """

        start_date = formatter_st(start_date) if start_date else None
        end_date = formatter_st(end_date) if end_date else None
        dt_start = np.datetime64(
            datetime.datetime.fromtimestamp(time.mktime(start_date))) if start_date else None
        dt_end = np.datetime64(datetime.datetime.fromtimestamp(time.mktime(end_date))) if end_date else None

        filename = 'quote-tdays.csv'
        df = self._fetch_data(filename, date_columns='date')
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)

        result = df['date'].values
        if dt_start or dt_end or count:
            if not dt_end:
                dt_end = np.datetime64(datetime.date.today())
            if dt_start:
                result = result[np.where(result >= dt_start)]
            if dt_end:
                result = result[np.where(result <= dt_end)]
            if count and count > 0:
                result = result[-count:]
        result = [datetime.date.fromtimestamp(x.astype(datetime.datetime) / 1e9) for x in result]
        return result

    @assert_quote_init
    def get_security_info(self, security=None, fields=None, types=None) -> pd.DataFrame:
        """获取证券信息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
            types: 获取证券类型；类型 字符串 list；默认值 stock；
                   可选值: 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof' 等；

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                display_name：中文名称
                name：缩写简称
                start_date：上市日期；类型 datetime.date
                end_date: 退市日期；类型 datetime.date；如没有退市为 2200-01-01
                type：证券类型；stock（股票）, index（指数），etf（ETF基金），fja（分级A），fjb（分级B）

        """
        security = formatter_list(security)
        fields = formatter_list(fields)
        types = formatter_list(types, 'stock')

        result = pd.DataFrame()
        filename = 'quote-ctb.csv'
        df = self._fetch_data(filename, date_columns=('start_date', 'end_date'))
        df = df.copy()
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        if types:
            df = df[df['type'].isin(types)]
        if security:
            df = df[df['code'].isin(security)]
        if fields:
            cols_retain = ['code'] + fields
            cols_all = list(df.columns)
            cols_drop = [x for x in cols_all if x not in cols_retain]
            df.drop(columns=cols_drop, inplace=True)
        result = pd.concat([result, df], sort=False, ignore_index=True)
        result.set_index('code', inplace=True)
        return result

    @assert_quote_init
    def get_security_xrxd(self, security, start_date=None, end_date=None, count=None) -> pd.DataFrame:
        """获取证券除权除息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            DataFrame 对象，包含字段：
                date: 实施日期
                code：证券代码
                dividend_ratio：送股比例，每 10 股送 X 股
                transfer_ratio：转赠比例，每 10 股转增 X 股
                bonus_ratio：派息比例，每 10 股派 X 元

        """
        security = formatter_list(security)
        if not security:
            raise ValueError('security need be provided.')

        filename = 'quote-xrxd.csv'
        df = self._fetch_data(filename, date_columns='date')
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        df = df.copy()
        df = df[df['code'].isin(security)]
        tdays = self.get_trade_days(start_date, end_date, count)
        df = df[df['date'].isin(tdays)]
        df.sort_values(['code', 'date'], axis=0, ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    @assert_quote_init
    def get_quote_static(self, date=None, fields=None, exch=None) -> pd.DataFrame:
        """获取静态行情数据

        参数:
            date: 行情日期；类型 str/struct_time/datetime.date/datetime.datetime; 默认值：最新行情日
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money','high_limit','low_limit','pre_close','paused'
            exch: 交易所；默认值 ['SH', 'SZ']

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                datetime: 行情时间
                code：证券代码
                open：开盘价
                close：收盘价
                high：最高价
                low：最低价
                volume：成交量
                money：成交额
                high_limit：涨停价
                low_limit：跌停价
                pre_close：昨日收盘价
                paused：停牌标记

        """
        fields = formatter_list(fields)
        exch = formatter_list(exch, ['SH', 'SZ'])
        curr_date = formatter_st(date, self.get_quote_date())
        result = pd.DataFrame()
        for x in exch:
            filename = os.path.join('static', x, time.strftime('%Y', curr_date),
                                    x + '_STATIC_' + time.strftime('%Y%m%d', curr_date) + '.csv')
            df = self._fetch_data(filename, date_columns='datetime')
            if df is None:
                continue
            df = df.copy()
            df['code'] = df['code'] + '.' + x
            df['paused'] = df['paused'].astype('int')
            if fields:
                cols_retain = ['datetime', 'code'] + fields
                cols_all = list(df.columns)
                cols_drop = [x for x in cols_all if x not in cols_retain]
                df.drop(columns=cols_drop, inplace=True)
            result = pd.concat([result, df], sort=False, ignore_index=True)
        return result

    @assert_quote_init
    def get_quote_kdata(self, security, period='day', fq='pre', fq_vol=False, fields=None,
                        start_date=None, end_date=None, count=None, skip_paused=False):
        """获取K线数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            period: 周期，默认值 day，支持 day, daily, 1d, week, 1w, mon, month, 1M, season, year, mnX, Xm
                    mnX 或 Xm 代表 X 分钟K线数据，如 mn1 mn5 mn15 mn30 mn60 或 1m 5m 15m 30m 60m 等
            fq: 复权方式；默认值 'pre'；'pre' 前复权, 'post' 后复权，None 不复权，或 复权参考日
            fq_vol: 是否复权成交量：默认值 False
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money'
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一
            skip_paused: 是否跳过停牌：默认值 False

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                datetime: 行情时间
                code：证券代码
                open：开盘价
                close：收盘价
                high：最高价
                low：最低价
                volume：成交量
                money：成交额

        """

        # 参数格式标准化
        security = formatter_list(security)
        fields = formatter_list(fields, ['open', 'close', 'high', 'low', 'volume', 'money'])
        start_date = formatter_st(start_date) if start_date else None
        end_date = formatter_st(end_date, self.get_quote_date())
        if not start_date and not count:
            raise ValueError('start_date or count must to be set.')
        elif start_date and count:
            raise ValueError('start_date and count cannot be set both.')

        # 对周期进行分析，获得周期类型与间隔，day / mn1
        period_type, period_step = self._parse_period_str(period)

        # 针对设置 count，且周期基类为 day 的非单日周期，将 count 转换为 start_date 处理
        if count and period_type == 'day' and period not in ['day', 'daily', '1d']:
            start_date = self._parse_period_start(period, end_date, count)
            count = None

        # 需保留的列清单
        cols_retain = ['datetime', 'code'] + fields

        # 获取模式分析：是否从静态数据合成 mode_static
        mode_static = False
        prep_count = None
        if count:
            if period in ['day', 'daily']:
                prep_count = count
            elif period_type == 'mn1':
                prep_count = count * period_step
        if period_type == 'day':
            if prep_count:
                evaluate_days = prep_count
            elif start_date:
                evaluate_days = int((time.mktime(end_date) - time.mktime(start_date)) / 86400 * 5 / 7)
            else:
                evaluate_days = None
            if evaluate_days < len(security):
                mode_static = True
        result = pd.DataFrame()
        if mode_static:
            # 从静态文件获取数据
            check_security_count = count and skip_paused
            if check_security_count:
                sec_num = dict(zip(security, [0 for i in range(len(security))]))
            sec_list = security
            trade_list = self.get_trade_days(end_date=end_date)
            for i in range(len(trade_list)):
                dt = trade_list[-i - 1]
                df = self.get_quote_static(dt)
                # df = df.copy()
                df = df[df['code'].isin(sec_list)]
                if skip_paused:
                    df = df[df['paused'] == 0]
                if check_security_count:
                    for c in df['code'].tolist():
                        if c not in sec_num:
                            continue
                        sec_num[c] += 1
                        if sec_num[c] < count:
                            continue
                        if c in sec_list:
                            sec_list.remove(c)
                # self.execute_rehabilitation(df, fq, fq_vol, columns=cols_retain, inplace=True)
                result = pd.concat([result, df], sort=False, ignore_index=True)
                if check_security_count:
                    if not sec_list:
                        break
                else:
                    if count and i + 1 >= count:
                        break
                if start_date and dt.timetuple() <= start_date:
                    break
            cols_all = list(result.columns)
            cols_all.insert(0, cols_all.pop(cols_all.index('code')))
            result = result[cols_all]
            result.sort_values(['code', 'datetime'], axis=0, ascending=True, inplace=True)
            result.reset_index(drop=True, inplace=True)
        else:
            # 从K线文件获取数据
            dt_start = np.datetime64(
                datetime.datetime.fromtimestamp(time.mktime(start_date))) if start_date else None
            dt_end = np.datetime64(datetime.datetime.fromtimestamp(time.mktime(end_date)))
            append_paused = 'paused' in fields or skip_paused
            for c in security:
                p = c.find('.')
                if p < 0:
                    continue
                sec_code = c[0:p]
                exc_code = c[p + 1:]
                filename = os.path.join(period_type, exc_code, exc_code + '_' + period_type.upper()
                                        + '_' + sec_code + '.csv')
                df = self._fetch_data(filename, date_columns='datetime')
                if df is None:
                    continue
                df = df.copy()
                if append_paused:
                    if period_type == 'day':
                        df['paused'] = df.apply(lambda x: 1 if x['volume'] == 0 and x['money'] == 0 else 0, axis=1)
                    elif period_type == 'mn1':
                        c_period = 'day'
                        c_file = os.path.join(c_period, exc_code, exc_code + '_' + c_period.upper()
                                              + '_' + sec_code + '.csv')
                        c_df = self._fetch_data(c_file, date_columns='datetime')
                        c_skip_days = c_df[(c_df['volume'] == 0) & (c_df['money'] == 0)]['datetime'].tolist()
                        df['paused'] = df['datetime'].apply(
                            lambda x: 1 if x.astype('datetime64[D]').isin(c_skip_days) else 0)
                if skip_paused:
                    df = df[df['paused'] == 0]
                if not prep_count:
                    df = df[(df['datetime'] >= dt_start) & (df['datetime'] <= dt_end)]
                else:
                    df = df[df['datetime'] <= dt_end][-prep_count:]
                df.insert(loc=0, column='code', value=sec_code + '.' + exc_code)
                # self.execute_rehabilitation(df, fq, fq_vol, columns=cols_retain, inplace=True)
                result = pd.concat([result, df], sort=False, ignore_index=True)

        # 多周期分组聚合
        agg_need = True
        if period == 'year':
            result['period'] = result['datetime'].apply(lambda x: x.year)
        elif period == 'season':
            result['period'] = result['datetime'].apply(lambda x: '%dq%d' % (x.year, (x.month - 1) // 3 + 1))
        elif period == 'mon':
            result['period'] = result['datetime'].apply(lambda x: x.year * 100 + x.month)
        elif period == 'week':
            result['period'] = result['datetime'].apply(lambda x: '%dw%02d' % x.isocalendar()[:2])
        elif period_type == 'mn1' and period != 'mn1':
            m = [570, 660]
            n = period_step
            result['period'] = result['datetime'].apply(lambda x: '%d%02d%02dt%04d' % (
                x.year, x.month, x.day, ((x.hour * 60 + x.minute - 1 - m[0 if x.hour < 12 else 1]) // n + 1) * n))
        else:
            agg_need = False
        if agg_need:
            agg_dict = {'datetime': 'last', 'open': 'first', 'close': 'last', 'high': 'max', 'low': 'min',
                        'volume': 'sum', 'money': 'sum', 'paused': 'min'}
            for k in [x for x in agg_dict.keys() if x not in cols_retain]:
                del agg_dict[k]
            result = result.groupby(by=['code', 'period']).agg(agg_dict)
            result.reset_index(inplace=True)
            result.drop(columns='period', inplace=True)

        # 移除非选定列
        cols_all = list(result.columns)
        cols_drop = [x for x in cols_all if x not in cols_retain]
        if cols_drop:
            result.drop(columns=cols_drop, inplace=True)

        # 重建索引
        result.reset_index(drop=True, inplace=True)

        # 复权处理
        self.execute_rehabilitation(result, fq, fq_vol, inplace=True, skip_sort=True)

        return result

    def get_technical_analysis(self, security, indications, period='day', fq='pre', fq_vol=False, fields=None,
                               start_date=None, end_date=None, count=None, skip_paused=False, keep_quote=False):
        """获取技术指标

        参数:
            security: 一支股票代码或者一个股票代码的 list
            indications: 技术指标及参与，单个或List
                         单个指标：（'MA', 5)，
                         多个指标：[('MA', 5), ('KDJ', 9, 3, 3)]
                         可省略参数：['MA', 'KDJ']
            period: 周期，默认值 day，支持 day, daily, 1d, week, 1w, mon, month, 1M, season, year, mnX, Xm
                    mnX 或 Xm 代表 X 分钟K线数据，如 mn1 mn5 mn15 mn30 mn60 或 1m 5m 15m 30m 60m 等
            fq: 复权方式；默认值 'pre'；'pre' 前复权, 'post' 后复权，None 不复权，或 复权参考日
            fq_vol: 是否复权成交量：默认值 False
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money'
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一
            skip_paused: 是否跳过停牌：默认值 False
            keep_quote: 是否保留行情字段；默认值 False

        返回值:
            DataFrame 对象，字段为指标名称

        """

        # 计算时需要预加载的数量
        refer_num = self._options.get('refer_num', 0)
        start_date = formatter_st(start_date) if start_date else None
        end_date = formatter_st(end_date, self.get_quote_date())
        if not start_date and not count:
            raise ValueError('start_date or count must to be set.')
        elif start_date and count:
            raise ValueError('start_date and count cannot be set both.')
        prep_start = None
        prep_count = None
        if start_date:
            prep_start = self._parse_period_start(period, start_date, refer_num)
        elif count:
            prep_count = count + refer_num

        cols_quote = ['open', 'close', 'high', 'low', 'volume', 'money', 'paused']
        fields = formatter_list(fields, cols_quote)
        df = self.get_quote_kdata(security, period=period, fq=fq, fq_vol=True, fields=cols_quote
                                  , start_date=prep_start, end_date=end_date, count=prep_count)

        self.execute_technical_analysis(df, indications, inplace=True, skip_sort=True)

        # 跳过停牌
        if skip_paused:
            df = df[df['paused'] == 0]

        # 结果集数量显示
        result = pd.DataFrame()
        if not count:
            dt_start = np.datetime64(
                datetime.datetime.fromtimestamp(time.mktime(start_date))) if start_date else None
            dt_end = np.datetime64(datetime.datetime.fromtimestamp(time.mktime(end_date)))
            result = pd.concat([result, df[(df['datetime'] >= dt_start) & (df['datetime'] <= dt_end)]],
                               sort=False, ignore_index=True)
        else:
            for x, y in df.groupby(by='code'):
                result = pd.concat([result, y.iloc[-count:]], sort=False, ignore_index=True)
        result.reset_index(drop=True, inplace=True)

        # 是否保留行情字段
        cols_drop = []
        if not keep_quote:
            cols_drop = cols_quote
        elif type(keep_quote) is str:
            cols_drop = [x for x in cols_quote if x != keep_quote]
        elif type(keep_quote) is list:
            cols_drop = [x for x in cols_quote if x not in keep_quote]
        elif keep_quote:
            cols_drop = [x for x in cols_quote if x not in fields]
        cols_drop = list(set(cols_drop).intersection(set(result.columns)))
        if cols_drop:
            result.drop(columns=cols_drop, inplace=True)

        return result
