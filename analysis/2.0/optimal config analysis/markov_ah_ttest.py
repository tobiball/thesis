# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:55:27 2022

@author: tobiball
"""

def markov(df,arro):
    lPp = arro
    iCases = len(lPp)

    # expected mg value of trial 4
    def mgValue4(v):
        value = 0
        for pp in lPp:
                value += (v*pp[1]<pp[0])*(pp[0]-v*pp[1])/iCases
        return value

    # expected mg value of trial 3
    def mgValue3(v):
        value = 0
        for pp in lPp:
                deltaV = (pp[0]-v*pp[1]+(1-pp[1]-pp[0])*mgValue4(v)+pp[0]*mgValue4(v+1))
                value +=(deltaV>0)*deltaV/iCases
        return value

    # expected mg value of trial 2
    def mgValue2(v):
        value = 0
        for pp in lPp:
                deltaV = (pp[0]-v*pp[1]+(1-pp[1]-pp[0])*mgValue3(v)+pp[0]*mgValue3(v+1))
                value +=(deltaV>0)*deltaV/iCases
        return value

    # Returns the expected marginal expected value depending on the trial
    def mgValue(v,trial):
        switcher = {
            1: mgValue2(v),
            2: mgValue3(v),
            3: mgValue4(v),
            4: 0,
        }
        return switcher.get(trial,"invalid trial")

    def forageOpt(v,t,pT,pG):
        deltaV = (pG-v*pT+(1-pT-pG)*mgValue(v,t)+pG*mgValue(v+1,t))
        return int(deltaV>=0)

    def forage_keep_wealth(v,t,pT,pG):
        deltaV = (pG-v*pT)
        return int(deltaV>=0)

    def aver(arro):
        sum = 0
        count = 0
        for prob_pair in arro:
            for prob in prob_pair:
                sum += prob
                count += 1
        return (sum/count)

    av = aver(arro)

    lForageOpt      = [forageOpt(row.wealth,int(row.tri),row.pT,row.pG) for index,row in df.iterrows()]
    lForageKeepWealth   = [forage_keep_wealth(row.wealth,int(row.tri),row.pT,row.pG) for index,row in df.iterrows()]
    df = df.assign(s_opt = lForageOpt,
                   s_gain = df.pG > av,
                   s_loss = df.pG < av,
                   s_naive = (df.pT<df.pG).apply(int),
                   s_wealth = lForageKeepWealth)

    return ([sum(df.s_opt == df.s_naive), sum(df.s_opt == df.s_gain), sum(df.s_opt == df.s_loss),sum(df.s_opt == df.s_wealth)])