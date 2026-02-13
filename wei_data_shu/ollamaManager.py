#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import requests
import json
import toml

class ChatBot:
    def __init__(self, api_url, model='llama3.2', messages_file='messages.toml', history_file='chat_history.toml'):
        self.api_url = api_url
        self.model = model
        self.messages_file = messages_file
        self.history_file = history_file
        self.messages = self.load_initial_messages()
        self.initialize_history_file()

    # 读取初始消息
    def load_initial_messages(self):
        if os.path.exists(self.messages_file):
            data = toml.load(self.messages_file)
            return data['messages']
        else:
            print(f"文件 '{self.messages_file}' 不存在，加载默认初始消息。")
            return [{'role': 'system', 'content': '你是一个帮助用户的助手。请'}]
        
    # 初始化聊天记录文件
    def initialize_history_file(self):
        if not os.path.exists(self.history_file):
            # 如果聊天记录文件不存在，则创建一个空的聊天记录文件
            with open(self.history_file, 'w', encoding='utf-8') as f:
                toml.dump({'messages': []}, f)
            print(f"聊天记录文件 '{self.history_file}' 已创建，路径: {os.path.abspath(self.history_file)}")
        else:
            print(f"聊天记录文件路径: {os.path.abspath(self.history_file)}")

    # 记录聊天过程
    def record_chat_history(self):
        chat_data = {'messages': self.messages}
        with open(self.history_file, 'w', encoding='utf-8') as f:
            toml.dump(chat_data, f)

    # 发送消息到聊天API
    def send_message(self, user_input, stream=True):
        # 添加用户消息到聊天历史
        self.messages.append({'role': 'user', 'content': user_input})

        # 创建请求数据
        data_chat = {
            'model': self.model,
            'messages': self.messages,
            'stream': stream
        }

        try:
            # 发送 POST 请求
            response_chat = requests.post(self.api_url, json=data_chat, headers={'Content-Type': 'application/json'}, stream=stream)

            # 检查响应状态
            if response_chat.status_code == 200:
                if stream:
                    return self.handle_stream_response(response_chat)
                else:
                    return self.handle_non_stream_response(response_chat)
            else:
                print("请求失败，状态码:", response_chat.status_code)
                return None

        except requests.exceptions.RequestException as e:
            print("请求过程中发生错误:", e)
            return None

    # 处理流式响应
    def handle_stream_response(self, response_chat):
        content_output = ""
        for line in response_chat.iter_lines():
            if line:
                response_data = json.loads(line.decode('utf-8', errors='replace'))
                content = response_data.get('message', {}).get('content', '')
                print(content, end="")  # 实时输出响应
                content_output += content
        print("", end="\n")  # 结束行
        # 将助手的消息添加到聊天历史
        self.messages.append({'role': 'assistant', 'content': content_output})
        self.record_chat_history()
        return content_output

    # 处理非流式响应
    def handle_non_stream_response(self, response_chat):
        response_data = response_chat.json()
        content_output = response_data.get('message', {}).get('content', '')
        print(content_output)  # 输出响应
        self.messages.append({'role': 'assistant', 'content': content_output})
        self.record_chat_history()
        return content_output

    # 开始新聊天
    def start_new_chat(self):
        self.messages = self.load_initial_messages()
        print("新聊天会话已开始。")

# 使用示例
if __name__ == "__main__":
    bot = ChatBot(api_url='http://localhost:11434/api/chat')

    print("开始聊天（输入 'exit' 退出，输入 'new' 新建聊天）")
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'new':
            bot.start_new_chat()
            continue

        # 默认使用流式响应，可以根据需要选择非流式响应
        bot.send_message(user_input, stream=True)

    print("聊天结束。")