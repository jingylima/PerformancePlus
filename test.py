import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import matplotlib.pyplot as plt
import numpy
from flask import Flask


CLIENT_ID = '22BCNW'
CLIENT_SECRET = 'd837c8ae2b4b0c84cd42123eee101ec8'
'''
CLIENT_ID = '22B5HP'
CLIENT_SECRET = 'ab8e456b16023674bb774354c780fc60'
'''
  
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))
today2 = str(datetime.datetime.now().strftime("%Y-%m-%d"))

fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=today2, detail_level='1sec')

time_list = []
val_list = []


for i in fit_statsHR['activities-heart-intraday']['dataset']:
  val_list.append(i['value'])
  time_list.append(i['time'])
  
val_list = val_list[-360:]

avg = numpy.mean(val_list)


app = Flask(__name__)

@app.route("/")
def hello():
  return {'avg_heart_rate' : avg}

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8888)