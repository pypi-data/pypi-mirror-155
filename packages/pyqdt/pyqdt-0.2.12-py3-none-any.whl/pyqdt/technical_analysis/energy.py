# -*- coding: utf-8 -*-
# 能量指标

from .arithmetic import *

@arithmetic_wrapper
def VR(N=26, M=6):
    """成交量变异率

    公式：
        TH:=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N);
        TL:=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N);
        TQ:=SUM(IF(CLOSE=REF(CLOSE,1),VOL,0),N);
        VR:100*(TH*2+TQ)/(TL*2+TQ);
        MAVR:MA(VR,M);
    输入：
        N：统计周期数 N
        M：统计周期数 M
    输出：
        VR: 成交量变动率
        MAVR：成交量变动率的M周期平均
    定义：
        RETURNS=(VR, MAVR)

    """
    TH = SUM(IF(CLOSE > REF(CLOSE, 1), VOL, 0), N)
    TL = SUM(IF(CLOSE < REF(CLOSE, 1), VOL, 0), N)
    TQ = SUM(IF(CLOSE == REF(CLOSE, 1), VOL, 0), N)
    VR = 100 * (TH * 2 + TQ) / (TL * 2 + TQ)
    MAVR = MA(VR, M)
    return VR, MAVR


@arithmetic_wrapper
def PSY(N=12, M=6):
    """
    公式：
        PSY:COUNT(CLOSE>REF(CLOSE,1),N)/N*100;
        MAPSY:MA(PSY,M);
    输入：
        N：统计的天数 N
    输出：
        PSY: N周期的PSY值
        MAPSY: PSY的M周期移动平均
    定义：
        RETURNS=(PSY, MAPSY)
    """
    PSY = COUNT(CLOSE > REF(CLOSE, 1), N) / N * 100
    MAPSY = MA(PSY, M)
    return PSY, MAPSY