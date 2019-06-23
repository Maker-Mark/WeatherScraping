import pandas as pd
import requests
from bs4 import BeautifulSoup
page = requests.get(
    "https://forecast.weather.gov/MapClick.php?lat=40.6925&lon=-73.9904#.XQ93SJNKi34")
soup = BeautifulSoup(page.content, 'html.parser')

# Grab the seven day forcast
seven_day = soup.find(
    id="seven-day-forecast")


# Get the days
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
print(periods)


# Get the descriptions
short_descs = [sd.get_text()
               for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
print(short_descs)
print(temps)
print(descs)

# Use pandas to put the gathered data into a DataFrame
weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc": descs
})
print(weather)

# Getting the mean of the past 7 days
temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
temp_nums
print(temp_nums)
print(weather["temp_num"].mean())
