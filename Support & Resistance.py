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

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2020, 1, 1)    #Set Start Date
        #self.SetEndDate(2021, 5, 17)      #Set End Date
        self.SetCash(100000)             #Set Strategy Cash
        #self.SetBrokerageModel(BrokerageName.AlphaStreams)

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
        


    def OnData(self, data):
        
        
        self.secClose = data[self.sec].Close
        
        return self.secClose

          

        
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''


    
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
        

        #ordering
        
    
        
        if len(self.bdf) != 0:
 
            if self.Portfolio[self.sec].IsLong:
                #self.Debug("already long")
                pass
                    
            else:
                
                for d in range(len(self.bdf.l_pct_change)):
                    
                    
                    
                    if (0 < self.bdf.l_pct_change[d] < 0.05): #& (self.secClose > self.emaI.Current.Value):
                        #self.Debug(f" bdf pct: {self.bdf.l_pct_change[d]} ds: {self.engulfingI.Current.Value}  e: {self.DojiStarI.Current.Value } day: {self.Time}")
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
        
        
        
        if len(self.hdf) != 0:            
            
            if self.Portfolio[self.sec].Invested:
                
                
            
                for h in range(len(self.hdf.h_pct_change)):
                    
                    
                    
                    
                    if (-0.05< self.hdf.h_pct_change[h] < 0): #or (self.secClose > self.emaI.Current.Value):
                        #self.Debug(f" hdf pct: {self.hdf.h_pct_change[h]} ds: {self.DojiStarI.Current.Value}  e: {self.engulfingI.Current.Value  } day: {self.Time}")
                        if (self.engulfingI.Current.Value == -1.0) or (self.DojiStarI.Current.Value == -1.0) or (self.DojiI.Current.Value == 1.0):
                            self.SetHoldings(self.sec, 0.0)
                            #self.Debug(f"sold {self.Time}")
                            return
            else:
                pass
                    
        else:
            self.Debug("no hdf")
                    

                        
        
