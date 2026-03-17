"""MySQL database integration."""

from __future__ import annotations

from collections import deque

import mysql.connector


class MySQLDatabase:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("Connected to MySQL database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("MySQL connection closed")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                if isinstance(params, list):
                    cursor.executemany(query, params)
                else:
                    cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def execute_many(self, query, params_list):
        cursor = self.connection.cursor()
        try:
            cursor.executemany(query, params_list)
            self.connection.commit()
            print("Batch query executed successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def fetch_query(self, query, params=None, dictionary=False):
        cursor = self.connection.cursor(dictionary=dictionary)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def call_procedure(self, proc_name, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.callproc(proc_name, params if isinstance(params, (list, tuple)) else (params,))
            else:
                cursor.callproc(proc_name)
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            self.connection.commit()
            return results if results else None
        except mysql.connector.Error as err:
            print(f"存储过程调用错误: {err}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def run_ai_chatbot(self, chat_history_size=5, system_msg="System: You are a helpful AI assistant."):
        try:
            from mysql.ai.genai import MyLLM
        except Exception as exc:
            print(f"AI模块加载失败: {exc}")
            return
        my_llm = MyLLM(self.connection)
        chat_history = deque(maxlen=chat_history_size)
        while True:
            user_input = input("\nUser: ")
            if user_input.lower() in ("exit", "quit"):
                break
            history = [system_msg] + list(chat_history) + [f"User: {user_input}"]
            prompt = "\n".join(history)
            try:
                response = my_llm.invoke(prompt)
            except Exception as err:
                print(f"AI调用错误: {err}")
                continue
            print(f"Bot: {response}")
            chat_history.append(f"User: {user_input}")
            chat_history.append(f"Bot: {response}")


__all__ = ["MySQLDatabase"]
