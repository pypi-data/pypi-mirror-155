# -*- coding: utf-8 -*-
# 路径型指标
from .arithmetic import *

@arithmetic_wrapper
def BOLL(M=20, B=2):
    """布林线

    公式：
        MB:MA(CLOSE,M);
        UB:MID+N*STD(CLOSE,M);
        LB:MID-N*STD(CLOSE,M);
    输入：
        M：统计的天数 M
        B：布林带宽度 B
    输出：
        中轨线BOLL，上轨线UB、下轨线LB
    定义：
        RETURNS=(BOLL, UB, LB)

    """
    MB = MA(CLOSE, M)
    UB = MB + B * STD(CLOSE, M)
    LB = MB - B * STD(CLOSE, M)
    return MB, UB, LB

'''
@arithmetic_wrapper
def BBIBOLL(M=11, B=6):
    """多空布林线

    公式：
        CV:=CLOSE;
        BBIBOLL:(MA(CV,3)+MA(CV,6)+MA(CV,12)+MA(CV,24))/4;
        UB:BBIBOLL+M*STD(BBIBOLL,N);
        LB:BBIBOLL-M*STD(BBIBOLL,N);
    输入：
        M：统计的天数 M
        B：布林带宽度 B
    输出：
        中轨线BOLL，上轨线UB、下轨线LB
    定义：
        RETURNS=(BBIBOLL, BBIUB, BBILB)

    """
    #MB = (MA(CLOSE, 3) + MA(CLOSE, 6) + MA(CLOSE, 12) + MA(CLOSE, 24)) / 4
    #UB = MB + B * STD(MB, M)
    #LB = MB - B * STD(MB, M)
    return MB, UB, LB
'''