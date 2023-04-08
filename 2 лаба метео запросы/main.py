import requests

city = 'Moscow,RU'
appid = '29d09b29d42f90dfe468c166e44d0fd1'
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print('Скорость ветра и видимость на сегодня:')
print('Видимость:      ', data['visibility'])
print('Скорость ветра: ', data['wind']['speed'], 'м/c')
res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print('\n')
print("Прогноз погоды на неделю:")
for i in data['list']:
    print('Дата', i['dt_txt'].split()[0], 'Время', i['dt_txt'].split()[1])
    print('Видимость:      ', i['visibility'])
    print('Скорость ветра: ', i['wind']['speed'], 'м/c', '\n')
