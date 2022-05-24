import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


OWN_Endpoint = "hsttps://api.openweathermap.org/data/2.5/onecall?"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "ACabbf6aa64f5ed678744f82a13ebb8d6d"
auth_token = os.environ.get("AUTH_TOKEN")


weather_params = {
    "lat": 33.771257,
    "lon": 72.748766,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWN_Endpoint, params=weather_params)
response.raise_for_status()

weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
# print(weather_slice)

will_rain = False

for hour_data in weather_slice:
    # print(weather_data["hourly"][0]["weather"][0]["id"])
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    Client = Client(account_sid, auth_token, http_client=proxy_client)
    message = Client.messages .create(
        body="It's going to rain today. Remember to bring an Umbrella.",
        from_="+16053163407",
        to="+92 304 5678856"
    )
    print(message.status)