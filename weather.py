from datetime import datetime
import requests

def get_weather():
    now = datetime.now()
    query_link = str(now.strftime("%Y-%m-%d")+"T"+str(now.strftime("%H:%M:%S")))

    url = f'https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast/?date={query_link}'
    response = requests.get(url)

    weather_data = response.json()
    print()

    if response.status_code == 200:
        weather = weather_data['data']['items'][0]['forecasts'][0]['forecast']
        return {"weather": weather}
    else:
        return {"error": "Failed to fetch weather"}
    
