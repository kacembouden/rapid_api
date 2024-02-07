from flask import Flask ,jsonify, request
import MetaTrader5 as mt5
from json import loads, dumps
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return 'working'

@app.route("/api/ohlc/<symbol>/<timeframe>" , methods = ['GET'])
def ohlc(symbol,timeframe):
    tf = {'MN1': mt5.TIMEFRAME_MN1,'W1': mt5.TIMEFRAME_W1,'D1': mt5.TIMEFRAME_D1,'H4': mt5.TIMEFRAME_H4,
          'H1': mt5.TIMEFRAME_H1,'M30': mt5.TIMEFRAME_M30,'M15': mt5.TIMEFRAME_M15,'M5': mt5.TIMEFRAME_M5,
          'M2': mt5.TIMEFRAME_M2 ,'M1': mt5.TIMEFRAME_M1,}

    # connect to MetaTrader 5
    if not mt5.initialize():
        mt5.shutdown()

    last = request.args.get('last', type=int)
    fromm = request.args.get('from', type=str)
    to = request.args.get('to', type=str)

    if last != None:  
        btc_rates = mt5.copy_rates_from_pos(symbol, tf[timeframe], 0, last)
    elif fromm :
        fromm = fromm.split('-')
        to = to.split('-')
        year_f, month_f, day_f, hour_f = fromm[0], fromm[1],fromm[2],fromm[3]
        year_t, month_t, day_t, hour_t = to[0] , to[1], to[2], to[3]
        btc_rates = mt5.copy_rates_range(symbol, tf[timeframe], datetime(int(year_f),int(month_f),int(day_f),int(hour_f)),
                                        datetime(int(year_t),int(month_t),int(day_t),int(hour_t)))

    rates_frame = pd.DataFrame(btc_rates)

    result = rates_frame.to_json(orient="split")
    parsed = loads(result)


    return dumps(parsed, indent=4)



@app.route("/api/tick/<symbol>" , methods = ['GET'])
def tick(symbol):

    # connect to MetaTrader 5
    if not mt5.initialize():
        mt5.shutdown()

    last = request.args.get('last', type=int)
    fromm = request.args.get('from', type=str)
    to = request.args.get('to', type=str)


    if last != None: 
        btc_rates = mt5.copy_ticks_from(symbol, datetime(2025, 2, 6), last, mt5.COPY_TICKS_ALL) 
    elif fromm :
        fromm = fromm.split('-')
        to = to.split('-')
        year_f, month_f, day_f, hour_f = fromm[0], fromm[1],fromm[2],fromm[3]
        year_t, month_t, day_t, hour_t = to[0] , to[1], to[2], to[3]
        btc_rates = mt5.copy_ticks_range(symbol, datetime(int(year_f),int(month_f),int(day_f),int(hour_f)),
                                        datetime(int(year_t),int(month_t),int(day_t),int(hour_t)) , mt5.COPY_TICKS_ALL)


    rates_frame = pd.DataFrame(btc_rates)

    result = rates_frame.to_json(orient="split")
    parsed = loads(result)


    return dumps(parsed, indent=4)










if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
