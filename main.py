# coding:utf-8
import sys
import calendar
from GoogleCalendar import GoogleCalendar
# from datetime import date
from datetime import *

def get_year_days(year, month):
  month_days = [i+1 for i in range(calendar.monthrange(year, month)[1])]
  days = list(map(lambda day: "{0:02d}/{1:02d}/{2:02d}".format(year, month, day), month_days))
  return days

def main(year):
  months = [i+1 for i in range(12)]
  year_days = list(map(lambda month: get_year_days(year, month), months))

  events = GoogleCalendar().getEvents(year)
  holiday_dict = dict(
        (event["start"]["date"].replace("-", "/"), event["summary"])
        for event in events
      )

  week = ["月", "火", "水", "木", "金", "土", "日"]

  for month in year_days:
    for day in month:
      week_str = week[datetime.strptime(day, '%Y/%m/%d').weekday()]
      if day in holiday_dict:
        print(day + " " + week_str.decode("utf_8") + " " + holiday_dict[day])
      else:
        print(day + " " + week_str.decode("utf_8"))


if __name__ == '__main__':
  main(2017)