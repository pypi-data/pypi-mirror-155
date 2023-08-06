# -*- coding: utf-8 -*-
# 超买超卖

from .arithmetic import *

'''
@arithmetic_wrapper
def ACCER(N=8):
    """幅度涨速

    公式：
        ACCER:SLOPE(CLOSE,N)/CLOSE;
        输出幅度涨速:收盘价的N日线性回归斜率/收盘价
    输入：
        N：统计的周期数 N
    输出：
        ACCER 的值。

    """
    return SLOPE(CLOSE,N)/CLOSE
'''


@arithmetic_wrapper
def ADTM(N=23, M=8):
    """动态买卖气指标

    公式：
        DTM:=IF(OPEN<=REF(OPEN,1),0,MAX((HIGH-OPEN),(OPEN-REF(OPEN,1))));
        DBM:=IF(OPEN>=REF(OPEN,1),0,MAX((OPEN-LOW),(OPEN-REF(OPEN,1))));
        STM:=SUM(DTM,N);
        SBM:=SUM(DBM,N);
        ADTM:IF(STM>SBM,(STM-SBM)/STM,IF(STM=SBM,0,(STM-SBM)/SBM));
        MAADTM:MA(ADTM,M);
    输入：
        N：统计的周期数 N
        M：统计的周期数 M
    输出：
        ADTM: ADTM值
        MAADTM: ADTM的M周期移动平均
    定义：
        RETURNS=(ADTM, MAADTM)

    """
    DTM = IF(OPEN <= REF(OPEN, 1), 0, MAX((HIGH - OPEN), (OPEN - REF(OPEN, 1))))
    DBM = IF(OPEN >= REF(OPEN, 1), 0, MAX((OPEN - LOW), (OPEN - REF(OPEN, 1))))
    STM = SUM(DTM, N)
    SBM = SUM(DBM, N)
    ADTM = IF(STM > SBM, (STM - SBM) / STM, IF(STM == SBM, 0, (STM - SBM) / SBM))
    MAADTM = MA(ADTM, M)
    return ADTM, MAADTM


@arithmetic_wrapper
def ATR(N=14):
    """真实波幅

    公式：
        MTR:MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
        ATR:MA(MTR,N);
    输入：
        N：统计的周期数
    输出：
        MTR: MTR值
        ATR: MTR的N周期移动平均
    定义：
        RETURNS=(MTR, ATR)

    """
    MTR = MAX(MAX((HIGH - LOW), ABS(REF(CLOSE, 1) - HIGH)), ABS(REF(CLOSE, 1) - LOW))
    ATR = MA(MTR, N)
    return MTR, ATR


@arithmetic_wrapper
def BIAS(N1=6, N2=12, N3=24):
    """乖离率

    公式：
        BIAS1 :(CLOSE-MA(CLOSE,N1))/MA(CLOSE,N1)*100;
        BIAS2 :(CLOSE-MA(CLOSE,N2))/MA(CLOSE,N2)*100;
        BIAS3 :(CLOSE-MA(CLOSE,N3))/MA(CLOSE,N3)*100;
    输入：
        N1: 统计的周期数 N1
        N2: 统计的周期数 N2
        N3: 统计的周期数 N3
    输出：
        BIAS1: N1周期的BIAS值
        BIAS2: N2周期的BIAS值
        BIAS3: N3周期的BIAS值
    定义：
        RETURNS=(BIAS{N1}, BIAS{N2}, BIAS{N3})

    """
    BIAS1 = (CLOSE - MA(CLOSE, N1)) / MA(CLOSE, N1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, N2)) / MA(CLOSE, N2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, N3)) / MA(CLOSE, N3) * 100
    return BIAS1, BIAS2, BIAS3


@arithmetic_wrapper
def BIAS_QL(N=6, M=6):
    """乖离率-传统版

    公式：
        BIAS :(CLOSE-MA(CLOSE,N))/MA(CLOSE,N)*100;
        BIASMA :MA(BIAS,M);
        输出乖离率BIAS :(收盘价-收盘价的N日简单移动平均)/收盘价的N日简单移动平均*100
        输出BIASMA :乖离率的M日简单移动平均
    输入：
        N：统计的周期数 N
        M：统计的周期数 M
    输出：
        BIAS: N周期的BIAS值
        MABIAS: BIAS的M周期移动平均
    定义：
        RETURNS=(BIAS, MABIAS)

    """
    BIAS = (CLOSE - MA(CLOSE, N)) / MA(CLOSE, N) * 100
    MABIAS = MA(BIAS, M)
    return BIAS, MABIAS


@arithmetic_wrapper
def BIAS_36(M=6):
    """三六乖离

    公式：
        BIAS36:MA(CLOSE,3)-MA(CLOSE,6);
        BIAS612:MA(CLOSE,6)-MA(CLOSE,12);
        MABIAS:MA(BIAS36,M);
    输入：
        M：统计的周期数 M
    输出：
        BIAS36: 36乖离值
        BIAS612: 612乖离值
        MABIAS36：36乖离的M周期移动平均
    定义：
        RETURNS=(BIAS36, BIAS612, MABIAS)

    """
    BIAS36 = MA(CLOSE, 3) - MA(CLOSE, 6)
    BIAS612 = MA(CLOSE, 6) - MA(CLOSE, 12)
    MABIAS36 = MA(BIAS36, M)
    return BIAS36, BIAS612, MABIAS36

'''
@arithmetic_wrapper
def CCI(N=14):
    """商品路径指标

    公式：
        TYP:=(HIGH+LOW+CLOSE)/3;
        CCI:(TYP-MA(TYP,N))/(0.015*AVEDEV(TYP,N));
        TYP赋值:(最高价+最低价+收盘价)/3
        输出CCI = (TYP-TYP的N日简单移动平均)/(0.015*TYP的N日平均绝对偏差)
        其中，绝对平均偏差= 1/n * (SUM(|xi-x均|), i=1,2,3...n)
    输入：
        N：统计的周期数 N
    输出：
        CCI 的值。

    """
    TYP = (HIGH + LOW + CLOSE) / 3
    CCI = (TYP - MA(TYP, N)) / (0.015 * AVEDEV(TYP, N))
    return CCI
'''

'''
@arithmetic_wrapper
def CYF(N=21):
    """市场能量

    公式：
        CYF:100-100/(1+EMA(HSL,N));
        输出市场能量:100-100/(1+换手线的N日指数移动平均)
    输入：
        N：统计的周期数 N
    输出：
        CYF 的值。

    """
    return 100-100/(1+EMA(HSL,N))
'''

@arithmetic_wrapper
def DKX(M=10):
    """多空线

    公式：
        MID:=(3*CLOSE+LOW+OPEN+HIGH)/6;
        DKX:(20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+
        16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+
        13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+
        10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+
        7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+
        4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210;
        MADKX:MA(DKX,M);
    输入：
        M：统计的周期数 M
    输出：
        DKX: DKX值
        MADKX: DKX的M周期移动平均
    定义：
        RETURNS=(DKX, MADKX)

    """
    MID = (3 * CLOSE + LOW + OPEN + HIGH) / 6
    DKX = (20 * MID + 19 * REF(MID, 1) + 18 * REF(MID, 2) + 17 * REF(MID, 3) +
          16 * REF(MID, 4) + 15 * REF(MID, 5) + 14 * REF(MID, 6) +
          13 * REF(MID, 7) + 12 * REF(MID, 8) + 11 * REF(MID, 9) +
          10 * REF(MID, 10) + 9 * REF(MID, 11) + 8 * REF(MID, 12) +
          7 * REF(MID, 13) + 6 * REF(MID, 14) + 5 * REF(MID, 15) +
          4 * REF(MID, 16) + 3 * REF(MID, 17) + 2 * REF(MID, 18) + REF(MID, 20)) / 210
    MADKX = MA(DKX, M)    
    return DKX, MADKX

@arithmetic_wrapper
def KD(N=9, M1=3, M2=3):
    """DK随机指标

    公式：
        RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
        K:SMA(RSV,M1,1);
        D:SMA(K,M2,1);
    输入：
        N：统计的周期数 N
        M1：统计的周期数 M1
        M2：统计的周期数 M2
    输出：
        K: K值
        D: D值
    定义：
        RETURNS=(K, D)
    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV, M1, 1)
    D = SMA(K, M2, 1)
    return K, D


@arithmetic_wrapper
def KDJ(N=9, M1=3, M2=3):
    """随机指标

    公式：
        RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
        K:SMA(RSV,M1,1);
        D:SMA(K,M2,1);
        J:3*K-2*D;
    输入：
        N：统计的周期数 N
        M1：统计的周期数 M1
        M2：统计的周期数 M2
    输出：
        K: K值
        D: D值
        J: J值
    定义：
        RETURNS=(K,D,J)

    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = SMA(RSV, M1, 1)
    D = SMA(K, M2, 1)
    J = 3 * K - 2 * D
    return K, D, J


@arithmetic_wrapper
def SKDJ(N=9, M=3):
    """慢速随机指标

    公式：
        LOWV:=LLV(LOW,N);
        HIGHV:=HHV(HIGH,N);
        RSV:=EMA((CLOSE-LOWV)/(HIGHV-LOWV)*100,M);
        K:EMA(RSV,M);
        D:MA(K,M);
    输入：
        N：统计的周期数 N
        M：统计的周期数 M
    输出：
        K: K值
        D: D值
    定义：
        RETURNS=(K, D)
    """
    LOWV = LLV(LOW, N)
    HIGHV = HHV(HIGH, N)
    RSV = EMA((CLOSE - LOWV) / (HIGHV - LOWV) * 100, M)
    K = EMA(RSV, M)
    D = MA(K, M)
    return K, D


@arithmetic_wrapper
def MFI(N=14):
    """资金流动指标

    公式：
        TYP := (HIGH + LOW + CLOSE)/3;
        V1:=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N);
        MFI:100-(100/(1+V1));
    输入：
        N：统计的周期数 N
    输出：
        MFI值

    """
    TYP = (HIGH + LOW + CLOSE) / 3
    V1 = SUM(IF(TYP > REF(TYP, 1), TYP * VOL, 0), N) / SUM(IF(TYP < REF(TYP, 1), TYP * VOL, 0), N)
    MFI = 100 - (100 / (1 + V1))
    return MFI


@arithmetic_wrapper
def MTM(N=12, M=6):
    """动量线

    公式：
        MTM:CLOSE-REF(CLOSE,N);
        MAMTM:MA(MTM,M);
    输入：
        N：统计的周期数 N
    输出：
        MTM: MTM值
        MAMTM: MTM的M周期移动平均
    定义：
        RETURNS=(MTM, MTMMA)
    """
    MTM = CLOSE - REF(CLOSE, N)
    MAMTM = MA(MTM, M)
    return MTM, MAMTM


@arithmetic_wrapper
def ROC(N=12, M=6):
    """变动率

    公式：
        ROC:100*(CLOSE-REF(CLOSE,N))/REF(CLOSE,N);
        MAROC:MA(ROC,M);
    输入：
        N：统计的周期数 N
    输出：
        ROC: ROC值
        MAROC: ROC的M周期移动平均
    定义：
        RETURNS=(ROC, MAROC)

    """
    ROC = 100 * (CLOSE - REF(CLOSE, N)) / REF(CLOSE, N)
    MAROC = MA(ROC, M)
    return ROC, MAROC


@arithmetic_wrapper
def RSI(N1=6,N2=12,N3=24):
    """相对强弱指标

    公式：
        LC:=REF(CLOSE,1);
        RSI:SMA(MAX(CLOSE-LC,0),N,1)/SMA(ABS(CLOSE-LC),N,1)*100;
    输入：
        N1：统计的周期数 N1
        N2：统计的周期数 N2
        N3：统计的周期数 N3
    输出：
        RSI值
    定义：
        RETURNS=(RSI{N1}, RSI{N2}, RSI{N3})

    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100
    return RSI1, RSI2, RSI3


@arithmetic_wrapper
def MARSI(M1=10, M2=6):
    """相对强弱平均线

    公式：
        DIF:=CLOSE-REF(CLOSE,1);
        VU:=IF(DIF>=0,DIF,0);
        VD:=IF(DIF<0,-DIF,0);
        MAU1:=MEMA(VU,M1);
        MAD1:=MEMA(VD,M1);
        MAU2:=MEMA(VU,M2);
        MAD2:=MEMA(VD,M2);
        # MEMA(X, N)相当于SMA(X, N, 1)
        RSI10:MA(100*MAU1/(MAU1+MAD1),M1);
        RSI6:MA(100*MAU2/(MAU2+MAD2),M2);
    输入：
        M1：统计的周期数 M1
        M2：统计的周期数 M2
    输出：
        RSI1: M1周期的RSI值
        RSI2: M2周期的RSI值
    定义：
        RETURNS=(MARSI{M1}, MARSI{M2})

    """
    DIF = CLOSE - REF(CLOSE, 1)
    VU = IF(DIF >= 0, DIF, 0)
    VD = IF(DIF < 0, -DIF, 0)
    MAU1 = MEMA(VU, M1)
    MAD1 = MEMA(VD, M1)
    MAU2 = MEMA(VU, M2)
    MAD2 = MEMA(VD, M2)
    RSI1 = MA(100 * MAU1 / (MAU1 + MAD1), M1)
    RSI2 = MA(100 * MAU2 / (MAU2 + MAD2), M2)
    return RSI1, RSI2

'''
@arithmetic_wrapper
def OSC(N=20, M=6):
    """
    公式：
        OSC:100*(CLOSE-MA(CLOSE,N));
        MAOSC:EXPMEMA(OSC,M);
        输出变动速率线OSC = 100*(收盘价-收盘价的N日简单移动平均)
        输出MAOSC = OSC的M日指数平滑移动平均
    输入：
        N：统计的周期数 N
        M：统计的周期数 M
    输出：
        RETURNS=(OSC, MAOSC)

    """
    OSC = 100 * (CLOSE - MA(CLOSE, N))
    MAOSC = EXPMEMA(OSC, M)
    return OSC, MAOSC
'''

@arithmetic_wrapper
def UDL(N1=3, N2=5, N3=10, N4=20, M=6):
    """
    公式：
        UDL:(MA(CLOSE,N1)+MA(CLOSE,N2)+MA(CLOSE,N3)+MA(CLOSE,N4))/4;
        MAUDL:MA(UDL,M);
    输入：
        N1：统计的周期数 N1
        N2：统计的周期数 N2
        N3：统计的周期数 N3
        N4：统计的周期数 N4
        M：统计的周期数 M
    输出：
        UDL: UDL值
        MAUDL: UDL的M周期移动平均
    定义：
        RETURNS=(UDL, MAUDL)

    """
    UDL = (MA(CLOSE, N1) + MA(CLOSE, N2) + MA(CLOSE, N3) + MA(CLOSE, N4)) / 4
    MAUDL = MA(UDL, M)
    return UDL, MAUDL

@arithmetic_wrapper
def WR(N1=10, N2=6):
    """威廉指标

    公式：
        WR1: (HHV(HIGH,N1)-CLOSE)/(HHV(HIGH,N1)-LLV(LOW,N1)) * 100;
        WR2: (HHV(HIGH,N2)-CLOSE)/(HHV(HIGH,N2)-LLV(LOW,N2)) * 100;
        输出WR1:100*(N1日内最高价的最高值-收盘价)/(N1日内最高价的最高值-N1日内最低价的最低值)
        输出WR2:100*(N2日内最高价的最高值-收盘价)/(N2日内最高价的最高值-N2日内最低价的最低值)
    输入：
        N1：统计的周期数 N1
        N2：统计的周期数 N2
    输出：
        WR1: N1周期的WR值
        WR2: N2周期的WR值
    定义：
        RETURNS=(WR{N1}, WR{N2})
    """
    WR1 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100
    WR2 = (HHV(HIGH, N2) - CLOSE) / (HHV(HIGH, N2) - LLV(LOW, N2)) * 100
    return WR1, WR2


@arithmetic_wrapper
def LWR(N=9, M1=3, M2=3):
    """LWR威廉指标

    公式：
        RSV:= (HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N))*100;
        LWR1:SMA(RSV,M1,1);
        LWR2:SMA(LWR1,M2,1);
        RSV赋值: (N日内最高价的最高值-收盘价)/(N日内最高价的最高值-N日内最低价的最低值)*100
        输出LWR1:RSV的M1日[1日权重]移动平均
        输出LWR2:LWR1的M2日[1日权重]移动平均
    输入：
        N：统计的周期数 N
        M1：统计的周期数 M1
        M2：统计的周期数 M2
    输出：
        LWR1: N1周期的WR值
        LWR2: N2周期的WR值
    定义：
        RETURNS=(LWR, MALWR)
    """
    RSV = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    LWR1 = SMA(RSV, M1, 1)
    LWR2 = SMA(LWR1, M2, 1)
    return LWR1, LWR2

'''
@arithmetic_wrapper
def FSL(data):
    """分水岭
    
    公式：
        SWL:(EMA(CLOSE,5)*7+EMA(CLOSE,10)*3)/10;
        SWS:DMA(EMA(CLOSE,12),MAX(1,100*(SUM(VOL,5)/(3*CAPITAL))));
        输出SWL:(收盘价的5日指数移动平均*7+收盘价的10日指数移动平均*3)/10+移动平均
        输出SWS:以1和100*(成交量(手)的5日累和/(3*当前流通股本(手)))的较大值为权重收盘价的12日指数移动平均的动态移动平均
    输入：
    输出：
        RETURN(SWL, SWS)

    """
    SWL = (EMA(CLOSE, 5) * 7 + EMA(CLOSE, 10) * 3) / 10
    SWS = DMA(EMA(CLOSE, 12), MAX(1, 100 * (SUM(VOL, 5) / (3 * CAPITAL))))
    return SWL, SWS
'''

'''
@arithmetic_wrapper
def TAPI(index_stock, M=6):
    """加权指数成交值
    
    公式：
        TAPI:AMOUNT/INDEXC;
        MATAPI:MA(TAPI,M);
        输出加权指数成交值(需下载日线):成交额(元)/大盘的收盘价
        输出MATAIP:TAPI的M日简单移动平均
    输入：
        M：统计的周期数 M
    输出：
        RETURNS=(TAPI, MATAPI)
        
    """
    TAPI:AMOUNT/INDEXC;
    MATAPI:MA(TAPI,M);
    return TAPI, MATAPI
'''