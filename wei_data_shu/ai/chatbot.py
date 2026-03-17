"""Ollama chatbot implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

try:  # pragma: no cover
    import toml
except ModuleNotFoundError:  # pragma: no cover
    toml = None


def _load_toml(path: Path) -> dict[str, Any]:
    if tomllib is not None:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    if toml is not None:
        return toml.load(path)
    raise ModuleNotFoundError("toml")


def _dump_messages(path: Path, messages: list[dict[str, str]]) -> None:
    if toml is not None:
        with path.open("w", encoding="utf-8") as handle:
            toml.dump({"messages": messages}, handle)
        return

    lines = ["messages = []", ""]
    for message in messages:
        lines.append("[[messages]]")
        lines.append(f"role = {json.dumps(message['role'], ensure_ascii=False)}")
        lines.append(f"content = {json.dumps(message['content'], ensure_ascii=False)}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


class ChatBot:
    def __init__(
        self,
        api_url: str,
        model: str = "llama3.2",
        messages_file: str = "messages.toml",
        history_file: str = "chat_history.toml",
    ) -> None:
        self.api_url = api_url
        self.model = model
        self.messages_file = Path(messages_file)
        self.history_file = Path(history_file)
        self.messages = self.load_initial_messages()
        self.initialize_history_file()

    def load_initial_messages(self) -> list[dict[str, str]]:
        if self.messages_file.exists():
            data = _load_toml(self.messages_file)
            return data["messages"]
        print(f"文件 '{self.messages_file}' 不存在，加载默认初始消息。")
        return [{"role": "system", "content": "你是一个帮助用户的助手。请"}]

    def initialize_history_file(self) -> None:
        if not self.history_file.exists():
            _dump_messages(self.history_file, [])
            print(f"聊天记录文件 '{self.history_file}' 已创建，路径: {self.history_file.resolve()}")
            return
        print(f"聊天记录文件路径: {self.history_file.resolve()}")

    def record_chat_history(self) -> None:
        _dump_messages(self.history_file, self.messages)

    def send_message(self, user_input: str, stream: bool = True) -> str | None:
        self.messages.append({"role": "user", "content": user_input})
        data_chat = {"model": self.model, "messages": self.messages, "stream": stream}

        try:
            response_chat = requests.post(
                self.api_url,
                json=data_chat,
                headers={"Content-Type": "application/json"},
                stream=stream,
            )
            if response_chat.status_code != 200:
                print("请求失败，状态码:", response_chat.status_code)
                return None
            if stream:
                return self.handle_stream_response(response_chat)
            return self.handle_non_stream_response(response_chat)
        except requests.exceptions.RequestException as exc:
            print("请求过程中发生错误:", exc)
            return None

    def handle_stream_response(self, response_chat: requests.Response) -> str:
        content_output = ""
        for line in response_chat.iter_lines():
            if not line:
                continue
            response_data = json.loads(line.decode("utf-8", errors="replace"))
            content = response_data.get("message", {}).get("content", "")
            print(content, end="")
            content_output += content
        print("", end="\n")
        self.messages.append({"role": "assistant", "content": content_output})
        self.record_chat_history()
        return content_output

    def handle_non_stream_response(self, response_chat: requests.Response) -> str:
        response_data = response_chat.json()
        content_output = response_data.get("message", {}).get("content", "")
        print(content_output)
        self.messages.append({"role": "assistant", "content": content_output})
        self.record_chat_history()
        return content_output

    def start_new_chat(self) -> None:
        self.messages = self.load_initial_messages()
        print("新聊天会话已开始。")


__all__ = ["ChatBot"]
