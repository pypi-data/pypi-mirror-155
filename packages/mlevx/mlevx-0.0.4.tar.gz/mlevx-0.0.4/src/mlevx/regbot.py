#!/usr/bin/env python3
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire, warnings
from datetime import datetime

class Regbot:
  reg_model_path = resource_filename(__name__, 'finalized_model.h5') 
  model_scaler_path = resource_filename(__name__, 'logscaler.gz') 


  def __init__(self,*args):
  	pass



  @classmethod  
  def loadmodel(cls):
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      loaded_model = joblib.load(open(f'{cls.reg_model_path}', 'rb'))
      return loaded_model
  @classmethod
  def getWeekDay(cls,utcdatetime):
      date = datetime.fromisoformat(utcdatetime)
      day = date.isoweekday()
      return day

  @classmethod  
  def prepareInput(cls,opening,closing,utctime):
    avr = closing/(opening + closing)
    bvr = opening/(opening + closing)
    time = int(str(utctime).split(' ')[1].split(':')[0])
    day = cls.getWeekDay(utctime)  
    testdata = np.array([[avr,bvr,time,day]])
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      scaler = joblib.load(f'{cls.model_scaler_path}')
      testdata = scaler.transform(testdata)

      return testdata


  @classmethod
  def buySignalGenerator(cls,opening,closing,utctime):
    scalledInput = cls.prepareInput(opening,closing,utctime)
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      return (cls.loadmodel().predict_proba(scalledInput)[:,1] > 0.60).astype(int)[0]
    
  @classmethod
  def sellSignalGenerator(cls,opening,closing,utctime):
    scalledInput = cls.prepareInput(opening,closing,utctime)
    with warnings.catch_warnings():
      warnings.filterwarnings("ignore")
      return (cls.loadmodel().predict_proba(scalledInput)[:,1] <= 0.60).astype(int)[0]




def signal(opening,closing,utctime,dir):
  if dir == 'long':
    try:
      return Regbot.buySignalGenerator(opening,closing,utctime)
    except Exception as e:
      print(e)
  if dir == 'short':
    try:
      return Regbot.sellSignalGenerator(opening,closing,utctime)
    except Exception as e:
      print(e)
  else:
    print(f'{dir} is not a valid direction')
    return

if __name__ == '__main__':
  fire.Fire(signal)
