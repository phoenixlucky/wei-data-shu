"""Core text and date utilities."""

from __future__ import annotations

import base64
import time
from datetime import date, datetime, timedelta

class StringBaba:
    def __init__(self, input_string):
        self.input_string = input_string

    def format_string_sql(self):
        lines = [line.strip() for line in self.input_string.strip().split("\n")]
        return '"' + '","'.join(lines) + '"'

    def filter_string_list(self, filter_list):
        return [item for item in self.input_string if any(keyword in item for keyword in filter_list)]


class DateFormat:
    def __init__(self, interval_day, timeclass="date"):
        self.interval_day = interval_day
        self.timeclass = timeclass

    def get_timeparameter(self, Format="%Y%m%d"):
        if self.timeclass == "date":
            return (date.today() - timedelta(days=self.interval_day)).strftime(Format)
        if self.timeclass == "timestamp":
            return time.localtime(time.time())
        if self.timeclass == "time":
            if Format == "%Y%m%d":
                Format = "%H%M"
            return time.strftime(Format, time.localtime(time.time()))
        if self.timeclass == "datetime":
            return datetime.fromtimestamp(int(time.time()))
        raise TypeError("你输入的参数不合理!")

    def datetime_standar(self, df, colname, type=""):
        import pandas as pd

        for index, row in df.iterrows():
            date_value = row[colname]
            if date_value:
                df.at[index, colname] = pd.to_datetime(date_value, format="mixed")
        return df

    def datetime_standar_lost(self, df, colname):
        import pandas as pd

        if self.timeclass == "date":
            df[colname] = pd.to_datetime(df[colname]).dt.date
        elif self.timeclass == "time":
            formats = ["%Y-%m-%d", "%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
            for fmt in formats:
                try:
                    df[colname] = pd.to_datetime(df[colname], format=fmt)
                    break
                except ValueError:
                    continue
            else:
                print(f"Column {colname} cannot be parsed with the provided formats.")
        else:
            print("Invalid type. Choose either 'date' or 'time'.")
        return df


def decrypt(bs):
    try:
        decoded_bytes = base64.b64decode(bs)
        decoded_str = decoded_bytes.decode("utf-8")
        interval = int(decoded_str[6]) + int(decoded_str[-1]) * 10
        return "".join(decoded_str[index] for index in range(0, len(decoded_str), interval))
    except Exception as exc:
        print(f"Error during decryption: {exc}")
        return None


class eFormat:
    def __init__(self, results):
        self.results = results

    def toTuple(self):
        try:
            results_sql = "(binary('".encode("utf-8")
            for i in range(len(self.results) - 1):
                results_sql = results_sql + (str(self.results[i][0]) + "'),binary('").encode("utf-8")
            return results_sql + (str(self.results[len(self.results) - 1][0]) + "'))").encode("utf-8")
        except Exception as exc:
            print(exc)


__all__ = ["StringBaba", "DateFormat", "decrypt", "eFormat"]
