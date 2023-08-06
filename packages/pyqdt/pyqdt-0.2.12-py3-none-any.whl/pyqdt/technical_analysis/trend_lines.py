# -*- coding: utf-8 -*-
# 趋势指标
from .arithmetic import *


@arithmetic_wrapper
def MACD(X=CLOSE, SHORT=12, LONG=26, MID=9):
    """平滑异同平均

    公式：
        DIF:EMA(CLOSE,SHORT)-EMA(CLOSE,LONG);
        DEA:EMA(DIF,MID);
        MACD:(DIF-DEA)*2,COLORSTICK;
    输入：
        SHORT：统计的周期数 SHORT
        LONG：统计的周期数 LONG
        MID：统计的周期数 MID
    输出：
        DIF: DIF值
        DEA: DIF的MID周期移动平均
        MACD: MACD值
    定义：
        RETURNS=(DIF, DEA, MACD)
    """
    DIF = EMA(X, SHORT) - EMA(X, LONG)
    DEA = EMA(DIF, MID)
    MACD = (DIF - DEA) * 2
    return DIF, DEA, MACD


@arithmetic_wrapper
def VMACD(SHORT=12, LONG=26, MID=9):
    """量平滑异同平均

    公式：
        DIF:EMA(VOL,SHORT)-EMA(VOL,LONG);
        DEA:EMA(DIF,MID);
        MACD:DIF-DEA,COLORSTICK;
    输入：
        SHORT：统计的周期数 SHORT
        LONG：统计的周期数 LONG
        MID：统计的周期数 MID
    输出：
        DIF: DIF值
        DEA: DIF的MID周期移动平均
        MACD: MACD值
    定义：
        RETURNS=(VDIF, VDEA, VMACD)
    """
    DIF = EMA(VOL, SHORT) - EMA(VOL, LONG)
    DEA = EMA(DIF, MID)
    MACD = DIF - DEA
    return DIF, DEA, MACD


@arithmetic_wrapper
def QACD(N1=12, N2=26, M=9):
    """快速异同平均

    公式：
        DIF:EMA(CLOSE,N1)-EMA(CLOSE,N2);
        MACD:EMA(DIF,M);
        DDIF:DIF-MACD;
    输入：
        N1：统计的周期数 N1
        N2：统计的周期数 N2
        M：统计的周期数 M
    输出：
        DIF: DIF值
        MACD: DIF的M日移动平均
        DDIF: DDIF值
    定义：
        RETURNS=(QDIF, QMACD, QACD)
    """
    DIF = EMA(CLOSE, N1) - EMA(CLOSE, N2)
    MACD = EMA(DIF, M)
    DDIF = DIF - MACD
    return DIF, MACD, DDIF
