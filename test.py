import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
from flask import Flask
import docusign_envelope
import matplotlib.pyplot as plt

#docusign_envelope.send_document_for_signing()

CLIENT_ID = '22BCNW'
CLIENT_SECRET = 'd837c8ae2b4b0c84cd42123eee101ec8'
'''
CLIENT_ID = '22B5HP'
CLIENT_SECRET = 'ab8e456b16023674bb774354c780fc60'
'''

ACCESS_TOKEN = open('access_token').read()
REFRESH_TOKEN = open('refresh_token').read()

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))
today2 = str(datetime.datetime.now().strftime("%Y-%m-%d"))

fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=yesterday2, detail_level='1sec')
fit_statsSl = auth2_client.sleep(date = yesterday)
    
if fit_statsSl['sleep'][0]['minuteData'][-1]['value'] > '1':
  restless = True
else:
  restless = False

avg_hour_lst = []
avg_days_lst = []
time_lst = []


for i in fit_statsHR['activities-heart-intraday']['dataset']:
  avg_days_lst.append(i['value'])
  time_lst.append(i['time'])
  '''
heartdf = pd.DataFrame({'Heart Rate':avg_days_lst,'Time':time_lst})
heartdf.plot(kind = 'line', x = 'Time', y = 'Heart Rate')
plt.show()
'''
avg_hour_lst = avg_days_lst[-90:]

avg_hour = sum(avg_hour_lst)/90
avg_day = sum(avg_days_lst)/len(avg_days_lst)
ran_hour = max(avg_hour_lst) - min(avg_hour_lst)

if ran_hour > 35:
  mood = 'Take a deep breath. Relax.'
elif avg_hour > 100:
  mood = 'So much energy, go for a run!'
elif avg_hour < 60:
  mood = 'Get some rest, you deserve it.'
else:
  mood = "Alert, yet calm. You're all set!"

active_lst = []
normal_lst = []
sleepy_lst = []
for x in range(len(avg_days_lst)):
  hr = avg_days_lst[x]
  time = time_lst[x]
  #(intent was to remove sleeping time, better to do that in app) if datetime.strptime(time, '%H:%M:%S') #NOTE: might need changing to 12-hour time

  if hr > 95:
    active_lst.append(time)
  elif hr < 60:
    sleepy_lst.append(time)
  else:
    normal_lst.append(time)
    
active_time = []
normal_time = []
sleepy_time = []


'''
print('active')
for x in active_lst:
  print(x)
  
print('normal')
for x in normal_lst:
  print(x)
  
print('sleepy')
for x in sleepy_lst:
  print(x)
  '''
starttime = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
endtime = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
for x in active_lst:
  if datetime.datetime.strptime(x, '%H:%M:%S') - endtime > datetime.timedelta(minutes = 60):
    active_time.append([starttime.strftime('%H:%M:%S'), endtime.strftime('%H:%M:%S')])
    endtime = datetime.datetime.strptime(x, '%H:%M:%S')
    starttime = datetime.datetime.strptime(x, '%H:%M:%S')
  else:
    endtime = datetime.datetime.strptime(x, '%H:%M:%S')
active_time.append([starttime.strftime('%H:%M:%S'), endtime.strftime('%H:%M:%S')])
active_time = active_time[1:]

starttime = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
endtime = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
for x in normal_lst:
  if datetime.datetime.strptime(x, '%H:%M:%S') - endtime > datetime.timedelta(minutes = 60):
    normal_time.append([starttime.strftime('%H:%M:%S'), endtime.strftime('%H:%M:%S')])
    endtime = datetime.datetime.strptime(x, '%H:%M:%S')
    starttime = datetime.datetime.strptime(x, '%H:%M:%S')
  else:
    endtime = datetime.datetime.strptime(x, '%H:%M:%S')
normal_time.append([starttime.strftime('%H:%M:%S'), endtime.strftime('%H:%M:%S')])
normal_time = normal_time[1:]

starttime = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
endtime = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
for x in sleepy_lst:
  if datetime.datetime.strptime(x, '%H:%M:%S') - endtime > datetime.timedelta(hours = 2):
    sleepy_time.append([starttime.strftime('%H:%M:%S'), endtime.strftime('%H:%M:%S')])
    endtime = datetime.datetime.strptime(x, '%H:%M:%S')
    starttime = datetime.datetime.strptime(x, '%H:%M:%S')
  else:
    endtime = datetime.datetime.strptime(x, '%H:%M:%S')
sleepy_time.append([starttime.strftime('%H:%M:%S'), endtime.strftime('%H:%M:%S')])
sleepy_time = sleepy_time[1:]
  
#exercise = #hr more than 10 less than 20 over average

app = Flask(__name__)

@app.route("/")
def hello():
  return {'mood' : mood, 'avg_hr_hour' : avg_hour, 'avg_hr_day' : avg_day, 'ran_hr_hour': ran_hour, 'restless' : restless, 'active_time' : active_time, 'normal_time' : normal_time, 'sleepy_time' : sleepy_time}

if __name__ == "__main__":
  app.run()
