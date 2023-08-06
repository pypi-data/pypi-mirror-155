# Machine Learning MlEvx

This is a simplified version of [regpredict](https://pypi.org/project/regpredict/) package used to generate buy and sell signals for crypto and conventional stock markets based on the excess volume indicator(EVX). EVX is a concept where the bid-ask spread is estimated inherently from current market prices. 

You can read more about Evx in the whitepaper [here](https://www.researchgate.net/publication/345313655_DeFiPaper)  
# Installation
Install mlevx with `python3 -m pip install mlevx`  
# Usage

In your python script simply import the module and use as follows:

```  
from mlevx.regbot import signal
print(signal(20,65,utcdatetime,'long'))
```
The above methods take an assets opening and closing prices of the asset based on the time interval you have chosen. The third option is the datetime in utc as a string, and the last option is the decision to long or short the trade. A zero classification output would instruct the user to sell, while one output means don't sell or buy if the asset  is not already present in the orders.  

NB: The arguments can only be one between 'enter' or exit.  

# Testing an entire dataframe
Testing of a dataframe for correct buy, sell signals is as simple as applying the function as follows:  

```
import pandas as pd
from mlevx.regbot import signal, Regbot

df = pd.read_csv('../../../path/to/your/csvfile.csv')

y_pred = []
def getSignal(open,close,utctime,dir):
    return signal(open,close,utctime,dir)

df['weekday'] = df['date'].apply(lambda x: Regbot.getWeekDay(x))


df = df[df['enter_short'] == 0]
print(df.head())


#df['enter_long_pred'] = df.apply(lambda row: getSignal(row['open'], row['close'], str(row['date']),'long'), axis=1)
df['enter_short_pred'] = df.apply(lambda row: getSignal(row['open'], row['close'], str(row['date']),'short'), axis=1)

print(df.tail(20))

#print(len(df[df['enter_long_pred'] == df['enter_long']]), len(df))
print(len(df[df['enter_short_pred'] == df['enter_short']]), len(df))

```

Your original data must already have some presumed 'long' or 'short' signal.

# Warning
This is not financial advise. MlEVX is entirely on its preliminary stages. Use it at your own risk.