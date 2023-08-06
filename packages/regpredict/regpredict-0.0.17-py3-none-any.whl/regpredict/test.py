import pandas as pd
from regbot import signal, Regbot
#from regpredict.regbot import signal
df = pd.read_csv('../../../jupyter/regbot_v7.csv')

y_pred = []
def getSignal(open,close,utctime,dir):
    return signal(open,close,utctime,dir)

df['weekday'] = df['date'].apply(lambda x: Regbot.getWeekDay(x))


#df = df[df['enter_long'] == 1]
df = df[df['enter_short'] == 0]
print(df.head())


#df['enter_long_pred'] = df.apply(lambda row: getSignal(row['open'], row['close'], row['date'],'long'), axis=1)
df['enter_short_pred'] = df.apply(lambda row: getSignal(row['open'], row['close'], row['date'],'short'), axis=1)

print(df.tail(20))

#print(len(df[df['enter_long_pred'] == df['enter_long']]), len(df))
print(len(df[df['enter_short_pred'] == df['enter_short']]), len(df))