# -*- coding: utf-8 -*-
"""
Created on Thursday Jun 15 2022

@author: RobWen
Version: 0.2.9
"""
import pandas as pd
import numpy as np
from StockHero import Ticker

###############################################################################
###############################################################################


    ############################
    ###                      ###
    ###  Screener Summary    ###
    ###  under construction  ###
    ###                      ###
    ############################
    
# Basis
class StockValuation:

    def __init__(self, ticker):
        self.ticker = ticker
        
    def __repr__(self):
        return(self.ticker)
        
    def __str__(self):
        return(self.ticker)
    
    @property
    def valuation(self):
        return self.__df_valuation()
    
    def __df_valuation(self):
        
        arrays = [
            np.array([  "Fundamental"
                      , "Valuation Ratio"
                      , "Valuation Ratio"
                      , "Valuation Ratio"
                      , "Profitability"
                      , "Price"
                      , "Dividends"
                      , "Income Statement"
                      , "Income Statement"
                      , "Balance Sheet"
                      , "Cashflow Statement"
                      , "Technical Indicator"
                      ]),
            
            np.array([  "5-Year EBITDA Growth Rate"
                      , "Debt-to-EBITDA"
                      , "PE-Ratio (TTM)"
                      , "PE-Ratio (Forward)"
                      , "FCF Margin %"
                      , "Beta"
                      , "3-Year Dividend Growth Rate"
                      , "EBIT"
                      , "EBITDA"
                      , "Long-Term Debt"
                      , "Free Cash Flow"
                      , "50-Day SMA"
                      ])]
        
        # Yahoo Finanance # Morningstar # NASDAQ
        array_table = [
                        # Fundamental / 5-Year EBITDA Growth Rate
                        [np.nan
                       , np.nan
                       , np.nan]                              
                       # Valuation Ratio / Debt-to-EBITDA
                       , [self.debt_to_ebitda_yahoo()
                       , np.nan
                       , np.nan]
                       # Valuation Ratio / PE-Ratio (TTM)
                       , [Ticker(self.ticker).yahoo_statistics_p.iloc[2,0]
                       , np.nan
                       , np.nan]
                       # Valuation Ratio / PE-Ratio (Forward)
                       , [Ticker(self.ticker).yahoo_statistics_p.iloc[3,0]
                       , np.nan
                       , np.nan]
                       # Profitability / FCF Margin %
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Price / Beta
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Dividends / 3-Year Dividend Growth Rate
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Income Statement / EBIT
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Income Statement / EBITDA
                       , [Ticker(self.ticker).yahoo_statistics_p.iloc[48,0]
                       , np.nan
                       , np.nan]
                       # Balance Sheet / Long-Term Debt
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Cashflow Statement / Free Cash Flow
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Technical Indicator / 50-Day SMA
                       , [np.nan
                       , np.nan
                       , np.nan]
                       ]
            
        self.valuation_df = pd.DataFrame(array_table , index=arrays, columns = ['Yahoo Finance', 'Morningstar', 'NASDAQ'])
        
        return self.valuation_df
    
    def debt_to_ebitda_yahoo(self):
        
        ebitda = Ticker(self.ticker).yahoo_statistics_p.iloc[48,0]
        debt = Ticker(self.ticker).yahoo_statistics_p.iloc[54,0]
        
        debt_to_ebitda_yahoo_float = debt/ebitda
        
        return debt_to_ebitda_yahoo_float
    
###############################################################################
###############################################################################
    
    
    
    
    
    
    
    
    
    