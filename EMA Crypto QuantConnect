from Alphas.MacdAlphaModel import MacdAlphaModel
from Risk.MaximumDrawdownPercentPerSecurity import MaximumDrawdownPercentPerSecurity
from QuantConnect.Indicators import *

class PensiveGreenFly(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  
        self.SetCash(10000)  
        self.security = "ETHUSD"
        self.AddCrypto(self.security,Resolution.Daily,Market.Bitfinex)
       
        
        #self.AddAlpha(MacdAlphaModel(12, 26, 9, MovingAverageType.Exponential, Resolution.Daily))
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.05))
        self.SetBrokerageModel(BrokerageName.Bitfinex, AccountType.Cash) 
        #self.SetBrokerageModel(BrokerageName.AlphaStreams)
        #self.macdI = self.MACD(self.security, 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily)
        self.emaI = self.EMA(self.security, 30, Resolution.Daily)
        self.SetWarmUp(30, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.security),
        self.TimeRules.Every(timedelta(hours=12)),
                 self.ordering)
    
    def OnData(self, data):
        self.close = data[self.security].Close
        
        pass

        
    def ordering(self):
        
        if not self.emaI.IsReady:
            return
        
        
    
        
        if (self.Portfolio[self.security].Quantity < 0.0001) :
            #if self.Portfolio.CashBook["USD"].Amount > 0:
            if self.Securities[self.security].Price > self.emaI.Current.Value:
                self.Debug("Holdings:  " + str(self.Portfolio[self.security].Quantity))
            
                    
           
                self.SetHoldings(self.security, 1.0)
                
                self.Debug("bought:  " + str(self.Time) + " price:  " + str(self.close) + " EMA: " + str(self.emaI.Current.Value))  
                
    
        
        if (self.Portfolio[self.security].Quantity > 0.0001) :
            
            if self.Securities[self.security].Price < self.emaI.Current.Value:
                self.Debug("Holdings:  " + str(self.Portfolio[self.security].Quantity))
                
                self.SetHoldings(self.security, 0.0)
                self.Debug("sold:  " + str(self.Time) + " price:  " + str(self.close )+ " EMA: " + str(self.emaI.Current.Value))
                
            
                
           
                
                

            

            

            
  
        
