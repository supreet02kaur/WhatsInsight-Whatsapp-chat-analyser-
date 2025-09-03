import re
import pandas as pd


class Preprocessor: 
    def __init__(self):
        self.pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s[APM]{2})\s-\s([^:]+):\s(.+)'
    def preprocess(self , file_contents):
        # Regular expression to match date, time, and message
        # Convert file content into lines
        chat_data = file_contents.splitlines()

        # Extract data using regex
        messages = []
        for line in chat_data:
            match = re.match(self.pattern, line)
            if match:
                date, time, sender, message = match.groups()
                messages.append([f"{date}, {time}", date, sender, message])

        # Create DataFrame
        df = pd.DataFrame(messages, columns=["user_message", "date", "user", "message"])

        # Convert Date column to datetime format
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%y")

        # Extract year, month number, day, hour, and minute
        df["year"] = df["date"].dt.year
        df["month_num"] = df["date"].dt.month  # Month number
        df["month"] = df["date"].dt.strftime("%B")  # Full month name
        df["day"] = df["date"].dt.day
        df["day_name"] = df["date"].dt.strftime("%A")  # Full day name (Monday, Tuesday, etc.)

        # Convert time format and extract hour & minute
        df["hour"] = pd.to_datetime(df["user_message"].str.split(", ").str[1], format="%I:%M %p").dt.hour
        df["minute"] = pd.to_datetime(df["user_message"].str.split(", ").str[1], format="%I:%M %p").dt.minute
        period = []
        for hour in df[['day_name', 'hour']]['hour']:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))

        df['period'] = period

        # Final DataFrame
        df = df[["user_message", "date", "user", "message", "year", "month_num", "month", "day", "day_name", "hour", "minute", "period"]]

        return df
