import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import re

yesterday = datetime.now() - timedelta(1)
yesterday_date = datetime.strftime(yesterday, '%Y-%m-%d')

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_APIKEY = "Your data here"
NEWS_APIKEY = "Your data here"
TWILIO_ACCOUNT_SID = "Your data here"
TWILIO_AUTH_TOKEN = "Your data here"
PHONE_NUMBER = "Your data here"
TWILIO_PHONE_NUMBER = "Your data here"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_APIKEY,
}
r = requests.get(STOCK_ENDPOINT, params = params)
stock_data = r.json()["Time Series (Daily)"]

data_list = [value for (key, value) in stock_data.items()]

yesterday_data = data_list[0]
yesterday_close_data = float(yesterday_data["4. close"])

# print(yesterday_close_data)


day_before_yesterday = data_list[1]
day_before_yesterday_close_data = float(day_before_yesterday["4. close"])
# print(day_before_yesterday_close_data)


difference = yesterday_close_data-day_before_yesterday_close_data
positive_difference = round(abs((difference)), 2)
# print(positive_difference)


average_difference = ((yesterday_close_data+day_before_yesterday_close_data)/2)
percentage_difference = int((positive_difference/average_difference)*100)

# print(percentage_difference)

news_params = {
    "apiKey": NEWS_APIKEY,
    "q": COMPANY_NAME,
    "language": "en",
    "from": datetime.now() - timedelta(4),
    "to": datetime.now()
}
t = requests.get(NEWS_ENDPOINT, params=news_params)
news_data = t.json()["articles"][:3]

def get_news():
    global news_title
    global news_description
    news_title = []
    news_report = []
    news_description = []
    for report in news_data:
        news_report.append(report)
    for i in range(0, len(news_report)):
        news_title.append(news_report[i]["title"])
    for i in range(0, len(news_report)):
        s = (news_report[i]["description"])
        t = re.sub("<a.*?</a>", "", s)
        news_description.append(t)
    # print(news_description)

if percentage_difference > 5:
    get_news()
    gain = True

if gain:
    if difference > 0:
        emoji = "🔺"
    else:
        emoji = "🔻"
    for news in range(0, len(news_title)):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages \
                .create(
                body=(f"{STOCK_NAME}: {percentage_difference}%{emoji}\nHeadline: {news_title[news]}\nBrief: {news_description[news]}"),
                from_ = TWILIO_PHONE_NUMBER,
                to = PHONE_NUMBER,
            )   
