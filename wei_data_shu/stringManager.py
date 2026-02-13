import base64
from datetime import date, time,datetime,timedelta
import time

import pandas as pd


class StringBaba:
    def __init__(self, input_string):
        self.input_string = input_string

    def format_string_sql(self):
        input_lines = self.input_string.strip()
        # 将输入字符串按换行符分割成列表
        lines = input_lines.split('\n')
        lines=[line.strip() for line in lines]
        # 使用 join 函数将列表元素连接成一个字符串，并在元素之间加上 ","
        formatted_output = '","'.join(lines)
        # 给整个字符串加上双引号
        formatted_output = f'"{formatted_output}"'
        return formatted_output

    def filter_string_list(self,filter_list):
        filtered_list = [s for s in self.input_string if any(keyword in s for keyword in filter_list)]
        return filtered_list

class DateFormat(object):
    def __init__(self, interval_day,timeclass='date'):
        self.interval_day = interval_day
        self.timeclass=timeclass #1日期 2时间戳 3时刻

    def get_timeparameter(self,Format='%Y%m%d'):
        if self.timeclass=='date':
            '返回日期'
            realtime = (date.today() - timedelta(days=self.interval_day)).strftime(Format)
        elif self.timeclass=='timestamp':
            '返回时间戳'
            realtime = time.localtime(time.time())
        elif self.timeclass=='time':
            ':return time'
            if Format=='%Y%m%d':
                Format = '%H%M'
            realtime = time.strftime(Format, time.localtime(time.time()))
        elif self.timeclass=='datetime':
            realtime= datetime.fromtimestamp(int(time.time()))
        else:
            raise TypeError("你输入的参数不合理!")
        return realtime

    def datetime_standar(self,df, colname, type=""):
        for index, row in df.iterrows():
            date_value = row[colname]

            # 检查日期值是否为None
            if date_value:
                # 在这里可以对非空日期值进行操作，比如转换日期格式等
                df.at[index, colname] = pd.to_datetime(date_value, format='mixed')
            else:
                # 对空日期值进行处理，可以跳过或执行其他操作
                pass
        return df

    def datetime_standar_lost(self,df, colname):
    #处理表格的列文本时间格式
        if self.timeclass == 'date':
            df[colname] = pd.to_datetime(df[colname]).dt.date
        elif self.timeclass == 'time':
            formats = ['%Y-%m-%d', '%H:%M:%S', '%Y-%m-%d %H:%M:%S']
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
        x = int(decoded_str[6]) + int(decoded_str[-1]) * 10
        # Use list comprehension for building the result list
        result = [decoded_str[i] for i in range(0, len(decoded_str), x)]
        result_str = ''.join(result)
        return result_str
    except Exception as e:
        print(f"Error during decryption: {e}")
        return None

class eFormat(object):
    def __init__(self, results):
        self.results = results

    def toTuple(self):
        try:
            results_sql = "(binary('".encode('utf-8')
            for i in range(len(self.results) - 1):
                results_sql = results_sql + (str(self.results[i][0]) + "'),binary('").encode("utf-8")
            results = results_sql + (str(self.results[len(self.results) - 1][0]) + "'))").encode('utf-8')
            return results
        except Exception as e:
            print(e)
            pass

