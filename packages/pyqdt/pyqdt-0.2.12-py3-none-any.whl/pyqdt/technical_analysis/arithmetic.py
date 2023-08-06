# -*- coding: utf-8 -*-

import threading
from functools import wraps

import numpy as np
import pandas as pd


class ArithmeticQuoteValue(object):
    def __init__(self, label=None):
        self._label = label

    @property
    def label(self):
        return self._label

    @property
    def value(self):
        return ArithmeticContainer().ref(self._label)

    def _f(self, val):
        return float(val) if val else 0

    def __get__(self, instance, owner):
        return self.value

    def __str__(self):
        return self.label

    def __float__(self):
        return self._f(self.value)

    def __add__(self, other):
        return self.value + self._f(other)

    def __radd__(self, other):
        return self._f(other) + self.value

    def __sub__(self, other):
        return self.value - self._f(other)

    def __rsub__(self, other):
        return self._f(other) - self.value

    def __mul__(self, other):
        return self.value * self._f(other)

    def __rmul__(self, other):
        return self._f(other) * self.value

    def __truediv__(self, other):
        return self.value / self._f(other)

    def __rtruediv__(self, other):
        return self._f(other) / self.value

    def __floordiv__(self, other):
        return self.value / self._f(other)

    def __rfloordiv__(self, other):
        return self._f(other) / self.value

    def __mod__(self, other):
        return self.value % self._f(other)

    def __rmod__(self, other):
        return self._f(other) / self.value

    def __pow__(self, power, modulo=None):
        return pow(self.value, power, modulo)

    def __rpow__(self, other):
        return pow(self._f(other), self.value)

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return self.value

    def __lt__(self, other):
        return self.value < self._f(other)

    def __gt__(self, other):
        return self.value > self._f(other)

    def __le__(self, other):
        return self.value <= self._f(other)

    def __ge__(self, other):
        return self.value >= self._f(other)

    def __eq__(self, other):
        return self.value == self._f(other)

    def __ne__(self, other):
        return self.value != self._f(other)


class ArithmeticContainer(object):
    """计算容器"""
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """单例模式-线程保护"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_security'):
            self._security = None
        if not hasattr(self, '_operator'):
            self._operator = None
        if not hasattr(self, '_result'):
            self._result = None

    def reset(self, security=None):
        if self._security == security:
            return
        if not security:
            self._security = None
            self._operator = None
            self._result = None
        else:
            # trace('new operator', security)
            self._security = security
            self._result = None
            self._operator = ArithmeticOperator()

    def update(self, data):
        if self._operator:
            self._operator.update(data)

    def __setattr__(self, key, value):
        if key == 'result':
            self._result = value
            return
        self.__dict__[key] = value

    def __getattr__(self, item):
        if item == 'result':
            return self._result

        if item.lower() in ['ref', 'std', 'abs', 'max', 'min', 'count', 'sum',
                            'ma', 'ema', 'mema', 'sma', 'hhv', 'llv']:
            if self._operator:
                return getattr(self._operator, item.lower())


class ArithmeticOperator(object):
    def __init__(self):
        self._data = pd.DataFrame()
        self._stats = []
        self._index = 0

    def _fetch_stat(self):
        if self._index <= len(self._stats):
            self._stats.append(ArithmeticStatistics())
        # print('current stats [%d]' % (self._index))
        stat = self._stats[self._index]
        self._index += 1
        return stat

    def update(self, data):
        df = pd.DataFrame([data.values], columns=data.index)
        df = df[['open', 'close', 'high', 'low', 'volume', 'money']]
        self._data = pd.concat([self._data, df], sort=False)
        self._index = 0

    def ref(self, x, n=0):
        label = None
        if type(x) is ArithmeticQuoteValue:
            label = x.label
        elif type(x) is str:
            label = x
        if label:
            if n >= len(self._data):
                n = -1
            print(type(self._data), self._data, n, label)
            r = self._data.iloc[-n - 1][label]
            if label == 'volume':
                r = r / 100
            return r
        else:
            stat = self._fetch_stat()
            # print('ref', x, n)
            return stat.ref(x, n)

    def abs(self, x):
        return abs(float(x))

    def max(self, *args):
        return max(args)

    def min(self, *args):
        return min(args)

    def __getattr__(self, item):
        if item in ['open', 'close', 'high', 'low', 'volume', 'money']:
            return self.ref(item)
        elif item in ['count', 'std', 'sum', 'ma', 'ema', 'mema', 'sma', 'hhv', 'llv']:
            stat = self._fetch_stat()
            return getattr(stat, item)


class ArithmeticStatistics(object):
    def __init__(self):
        self._data = []
        self._result = None

    @staticmethod
    def _val(x):
        # return x.value if type(x) is ArithmeticQuoteValue else None\
        #     if x is None or x == np.nan or x == float('inf') else x
        return x.value if type(x) is ArithmeticQuoteValue else 0 if x is None or x == np.nan or x == float('inf') else x

    @property
    def result(self):
        return self._result

    def _update(self, x, n):
        self._data.append(x)
        while 0 < n < len(self._data):
            self._data.pop(0)
        # print(self._data)

    def ref(self, x, n):
        x = self._val(x)
        self._update(x, n + 1)
        self._result = self._data[-n - 1] if len(self._data) > n else self._data[0]
        return self._result

    '''
    def max(self, x):
        self.hhv(x, 0)

    def min(self, x):
        self.llv(x, 0)
    '''

    def count(self, x, n):
        x = self._val(x)
        self._update(x, n)
        num = 0
        for v in self._data[-n:]:
            if v:
                num += 1
        self._result = num
        return self._result

    def std(self, x, n):
        x = self._val(x)
        self._update(x, n)
        if len(self._data[-n:]) > 1:
            self._result = float(np.std(self._data[-n:], ddof=1))
        #self._result = float(np.std(self._data[-n:]))
        return self._result

    def sum(self, x, n=0):
        x = self._val(x)
        self._update(x, n)
        self._result = float(np.sum(self._data[-n:]))
        return self._result

    def ma(self, x, n):
        x = self._val(x)
        self._update(x, n)
        self._result = float(np.mean(self._data[-n:])) if len(self._data) >= n else None
        return self._result

    def ema(self, x, n):
        x = self._val(x)
        return self.sma(x, n + 1, 2)

    def mema(self, x, n):
        x = self._val(x)
        return self.sma(x, n, 1)

    def sma(self, x, n, m):
        x = self._val(x)
        if self._result is None:
            self._result = x
            return 0
        else:
            self._result = (m * x + (n - m) * self._result) / n
            return self._result

    def hhv(self, x, n):
        x = self._val(x)
        self._update(x, n)
        self._result = float(np.max(self._data[-n:]))
        return self._result

    def llv(self, x, n):
        x = self._val(x)
        self._update(x, n)
        self._result = float(np.min(self._data[-n:]))
        return self._result


def arithmetic_wrapper(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if args and type(args[0]) is pd.Series:
            data = args[0]
            arith = ArithmeticContainer()
            arith.reset(data['code'])
            arith.update(data)
            if data['paused'] == 1:
                return arith.result
            if 'X' in kwargs:
                kwargs['X'] = eval(kwargs['X'].upper())

            # arith.result = func(*args[1:], **kwargs)
            try:
                result = func(*args[1:], **kwargs)
                if type(result) is tuple:
                    result = tuple([np.nan if x == float('inf') else x for x in result])
                elif result == float('inf'):
                    result = np.nan
                arith.result = result
            except (TypeError, ZeroDivisionError):
                returns = arithmetic_returns(func)
                if type(returns) is list:
                    arith.result = tuple([np.nan for i in range(len(returns))])
                else:
                    arith.result = np.nan
            return arith.result
        else:
            return func(*args, **kwargs)

    return _wrapper


def arithmetic_reset():
    ArithmeticContainer().reset()


def arithmetic_returns(func, args=None):
    result = func.__code__.co_name

    # get result from RETURNS
    if len(func.__code__.co_consts) > 0 and func.__code__.co_consts[0]:
        for x in func.__code__.co_consts[0].splitlines():
            p = x.find('=')
            if p >= 0 and x[0:p].strip() == 'RETURNS':
                result = x[p + 1:].strip()

    p = 0
    args_maps = {}
    args = args if args else []
    args_name = [x for x in func.__code__.co_varnames[:func.__code__.co_argcount]]
    args_default = getattr(func, '__defaults__')
    if not args_default:
        args_default = []
    num_nodefault = len(args_name) - len(args_default)
    for i in range(len(args_name)):
        if i < num_nodefault:
            if p >= len(args):
                raise Exception('too more args.')
            args_maps[args_name[i]] = args[p]
            p += 1
        else:
            if p >= len(args):
                args_maps[args_name[i]] = args_default[i - num_nodefault]
            elif i == 0 and args_name[i] == 'X' and type(args[p]) is not str:
                args_maps[args_name[i]] = args_default[i - num_nodefault]
            else:
                args_maps[args_name[i]] = args[p]
                p += 1

    if len(result) > 2 and result[0] == '(' and result[-1] == ')':
        arr = result[1:-1].split(',')
        result = []
        for x in arr:
            x = x.strip()
            for k, v in args_maps.items():
                x = x.replace('{' + k + '}', str(v))
            result.append(x)
    else:
        for k, v in args_maps.items():
            result = result.replace('{' + k + '}', str(v))
    return result


OPEN = ArithmeticQuoteValue('open')
CLOSE = ArithmeticQuoteValue('close')
HIGH = ArithmeticQuoteValue('high')
LOW = ArithmeticQuoteValue('low')
VOL = ArithmeticQuoteValue('volume')
MONEY = ArithmeticQuoteValue('money')


def IF(C, T, F):
    return float(T) if C else float(F)


def ABS(X):
    """绝对值"""
    return ArithmeticContainer().abs(X)


def MAX(*args):
    """最大值"""
    return ArithmeticContainer().max(*args)


def MIN(*args):
    """最小值"""
    return ArithmeticContainer().min(*args)


def POW(X, Y):
    """求幂值"""
    return pow(X, Y)


def COUNT(C, N):
    """次数"""
    return ArithmeticContainer().count(C, N)


@arithmetic_wrapper
def SUM(X=CLOSE, N=5):
    """汇总

    输入:
        X: 数值或行情类型 [OPEN， CLOSE, HIGH, LOW, VOL, MONEY]
        N: 统计的周期数

    输出：
        N周期的汇总数值
    定义：
        RETURNS={X}_SUM

    """
    return ArithmeticContainer().sum(X, N)


@arithmetic_wrapper
def STD(X=CLOSE, N=0):
    """标准差

    输入:
        X: 数值或行情类型 [OPEN， CLOSE, HIGH, LOW, VOL, MONEY]
        N: 统计的周期数

    输出:
        N周期的标准差
    定义：
        RETURNS={X}_STD

    """
    return ArithmeticContainer().std(X, N)


@arithmetic_wrapper
def REF(X=CLOSE, N=0):
    """参考数据

    输入:
        X: 数值或行情类型 [OPEN， CLOSE, HIGH, LOW, VOL, MONEY]
        N: 统计的周期数

    输出:
        前N周期的行情数值，不包括当前周期
    定义：
        RETURNS={X}_R{N}

    """
    return ArithmeticContainer().ref(X, N)


@arithmetic_wrapper
def HHV(X=HIGH, N=5):
    """最大值

    输入:
        X: 数值或行情类型 [OPEN， CLOSE, HIGH, LOW, VOL, MONEY]
        N: 统计的周期数

    输出:
        N周期的最大值

    """
    return ArithmeticContainer().hhv(X, N)


@arithmetic_wrapper
def LLV(X=LOW, N=5):
    """最小值

    输入:
        X: 数值或行情类型 [OPEN， CLOSE, HIGH, LOW, VOL, MONEY]
        N: 统计的周期数

    输出:
        N周期的最小值

    """
    return ArithmeticContainer().llv(X, N)


@arithmetic_wrapper
def MA(X=CLOSE, N=5):
    """均线

    公式：
        MA1:MA(CLOSE,N);
    输入：
        N: 统计的周期数
    输出：
        MA: 移动平均
    定义：
        RETURNS=MA{N}

    """
    return ArithmeticContainer().ma(X, N)


@arithmetic_wrapper
def EMA(X=CLOSE, N=30):
    """指数移动平均

    公式：
        Y=(2*X+(N-1)*Y')/(N+1); Y'为上一周期值
    输入：
        N:统计的周期数
    输出：
        EMA:指数移动平均
    定义：
        RETURNS=EMA{N}

    """
    return ArithmeticContainer().ema(X, N)


@arithmetic_wrapper
def MEMA(X=CLOSE, N=5):
    """平滑移动平均

    公式：
        Y=(X+(N-1)*Y')/N; Y'为上一周期值
    输入：
        N: 统计的周期数
    输出：
        MEMA: 指数移动平均
    定义：
        RETURNS=MEMA{N}

    """
    return ArithmeticContainer().mema(X, N)


@arithmetic_wrapper
def SMA(X=CLOSE, N=7, M=1):
    """简单移动平均

    公式：
        Y=(M*X+(N-M)*Y')/N; Y'为上一周期值
    输入：
        N: 统计的周期数 N
        M: 权重 M
    输出：
        SMA: 简单移动平均
    定义：
        RETURNS=SMA{N}{M}

    """
    return ArithmeticContainer().sma(X, N, M)
