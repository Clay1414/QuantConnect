from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Indicators")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from datetime import *
import pandas as pd
from Risk.MaximumDrawdownPercentPerSecurity import MaximumDrawdownPercentPerSecurity

import numpy as np
import statistics


class stoch(QCAlgorithm):

    #Algo constructor called once
    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2020, 1, 1)    #Set Start Date
        
        self.SetCash(100000)             #Set Strategy Cash
        self.sec = "ETHUSD"
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.05))
        self.SetBrokerageModel(BrokerageName.Bitfinex, AccountType.Cash) 
        self.period = 1000
        self.AddCrypto(self.sec, Resolution.Daily)
        self.engulfingI = self.CandlestickPatterns.Engulfing(self.Symbol(self.sec), Resolution.Daily)
        self.DojiStarI = self.CandlestickPatterns.DojiStar(self.Symbol(self.sec), Resolution.Daily)
        self.DojiI = self.CandlestickPatterns.Doji(self.Symbol(self.sec), Resolution.Daily)
        #self.emaI = self.EMA(self.sec, 30, Resolution.Daily)
        self.SetWarmup(self.period, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay(self.sec), 
                 self.TimeRules.At(12,00),
                 self.T_and_B)
        
        #self.Schedule.On(self.DateRules.EveryDay(self.sec), 
                 #self.TimeRules.Every(TimeSpan.FromMinutes(60)),
                 #self.ordering)
        

    #Data pipeline
    def OnData(self, data):
        
        
        self.secClose = data[self.sec].Close
        
        return self.secClose

          

        
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''


    # Detection of support and resistance using historical prices
    def T_and_B(self):
        
        self.hist = self.History(self.Symbol(self.sec), self.period, Resolution.Daily).reset_index(level=0)

        self.df1= self.hist[['low','high','close','open']].copy()

        #self.df1['e'] = self.engulfingI
        #self.df1['ds']= self.DojiStarI
        
        
        
        #self.df1['e'] = self.Indicator(self.E, self.sec, self.period, Resolution.Daily)
        #self.df1['ds']= self.Indicator(self.DS, self.sec, self.period, Resolution.Daily)
        
        
        self.low= self.df1.low
        self.high = self.df1.high

        self.df1['bottom'] = " "
        self.df1['top']=" "

    # Create dataFrames of tops and bottoms
        for i in range(len(self.df1)):
            try:
        
                if (self.low[i] < self.low[i-1]) and (self.low[i] < self.low[i-2]) and (self.low[i] < self.low[i+1]) and (self.low[i] < self.low[i+2]) :
                    self.df1['bottom'][i] = 1
        
                elif (self.high[i] > self.high[i-1]) and (self.high[i] > self.high[i-2]) and (self.high[i] > self.high[i+1]) and (self.high[i] > self.high[i+2]):
        
                    self.df1['top'][i] = 1
    
                else:
                    self.df1['top'][i] = 0
                    self.df1['bottom'][i] = 0
    
            except:  
                 pass
        
        self.df1['l_pct_change']= (self.secClose-self.df1.low)/self.df1.low
        self.df1['h_pct_change'] = (self.secClose-self.df1.high)/self.df1.high
        
        
        self.hdf =  self.df1[self.df1['top'] == 1] 
        self.bdf = self.df1[self.df1['bottom'] == 1]
        
       
        #Make sure there is data in DF
        if len(self.bdf) != 0:
 
            if self.Portfolio[self.sec].IsLong:
                pass
                    
            else:
                #if price is within 5% of support and there is a bullish doji or engulfing BUY!
                for d in range(len(self.bdf.l_pct_change)):
                    
                    if (0 < self.bdf.l_pct_change[d] < 0.05): 
                      
                        if (self.engulfingI.Current.Value == 1.0) or (self.DojiStarI.Current.Value == 1.0) or (self.DojiI.Current.Value == 1.0):
                            self.SetHoldings(self.sec, 1.0)
                            #self.Debug(f"bought {self.Time}")
                            return
                        
                        else:
                            pass
                    else:
                        pass
          else:
            self.Debug("no bdf")
        
        #check for top dataframe values
        if len(self.hdf) != 0:            
            
            if self.Portfolio[self.sec].Invested:
                
                
            #If price is within 5% of a resistance level and bearish Doji or engulfing than SELL
                for h in range(len(self.hdf.h_pct_change)):
                
                    if (-0.05< self.hdf.h_pct_change[h] < 0): 
                        
                        if (self.engulfingI.Current.Value == -1.0) or (self.DojiStarI.Current.Value == -1.0) or (self.DojiI.Current.Value == 1.0):
                            self.SetHoldings(self.sec, 0.0)
                            #self.Debug(f"sold {self.Time}")
                            return
            else:
                pass
                    
        else:
            self.Debug("no hdf")
                    

                        
        
