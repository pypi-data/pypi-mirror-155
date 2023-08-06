# -*- coding: utf-8 -*-
# 均线指标

from .arithmetic import *


@arithmetic_wrapper
def HMA(N=12):
    """高价平均线

    公式：
        HMA:MA(HIGH, N);
    输入：
        N：统计的周期数
    输出：
        HMA: 最高价的N日移动平均

    """
    return MA(HIGH, N)


@arithmetic_wrapper
def LMA(N=12):
    """低价平均线

    公式：
        LMA:MA(LOW, N);
    输入：
        N：统计的周期数
    输出:
        LMA: 最低价的N日移动平均

    """
    return MA(LOW, N)


@arithmetic_wrapper
def VMA(N=12):
    """变异平均线

    公式：
        V:=(HIGH+OPEN+LOW+CLOSE)/4;
        VMA:MA(VV,N);
    输入：
        N：统计的周期数
    输出：
        VMA: VV的N日移动平均

    """
    V = (HIGH + OPEN + LOW + CLOSE) / 4
    return MA(V, N)


@arithmetic_wrapper
def EXPMA(N=12):
    """指数平均线

    公式：
        EXPMA:EMA(CLOSE,N);
    输入：
        N：统计的周期数
    输出：
        EXPMA

    """
    return EMA(**locals())


@arithmetic_wrapper
def BBI(N1=3, N2=6, N3=12, N4=24):
    """多空均线

    公式：
        BBI:(MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4;
    输入：
        N1：统计的天数 N1
        N2：统计的天数 N2
        N3：统计的天数 N3
        N4：统计的天数 N4
    输出：
        BBI的值

    """
    BBI = (MA(CLOSE,N1)+MA(CLOSE,N2)+MA(CLOSE,N3)+MA(CLOSE,N4))/4
    return BBI
