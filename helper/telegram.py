import requests
from typing import Optional
from configs.globals import (
    telegram_send_general_message_url,
    telegram_send_topic_message_url,
    telegram_chat_id,
    telegram_topic_id,
    telegram_topic_reply_to_message_id,
    project_name,
)

def set_telegram_general_message(message: str, chat_id: Optional[str] = None, thread_id: Optional[str] = None):
    try:
        target_chat_id = chat_id if chat_id else telegram_chat_id
        payload = {
            "chat_id": target_chat_id,
            "text": message,
        }

        response = requests.post(telegram_send_general_message_url, data=payload, timeout=15)

        if response.status_code != 200:
            body = response.text
            error = f"Project: {project_name} | Error: status code {response.status_code} | Body: {body}"
            raise Exception(error)

        data = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else None
        if not data or not data.get("ok", False):
            desc = data.get("description") if isinstance(data, dict) else response.text
            error = f"Project: {project_name} | Error: {desc}"
            raise Exception(error)

    except Exception as e:
        error = f"Project: {project_name} | Error: {str(e)}"
        raise Exception(error)

def set_telegram_topic_message(
    message: str,
    chat_id: Optional[str] = None,
    thread_id: Optional[str] = None,
    reply_to_message_id: Optional[str] = None,
):
    try:
        target_chat_id = chat_id if chat_id else telegram_chat_id
        payload = {
            "chat_id": target_chat_id,
            "text": message,
        }

        # Prefer reply_to_message_id (reply to the topic root message) if provided
        use_reply_id = reply_to_message_id if reply_to_message_id is not None else telegram_topic_reply_to_message_id
        if use_reply_id and str(use_reply_id).strip() != "":
            payload["reply_to_message_id"] = str(use_reply_id)
        else:
            # Fallback to message_thread_id when no reply id is provided
            use_thread_id = thread_id if thread_id is not None else telegram_topic_id
            if use_thread_id and str(use_thread_id).strip() != "":
                payload["message_thread_id"] = str(use_thread_id)

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            telegram_send_topic_message_url,
            json=payload,
            headers=headers,
            timeout=15,
        )

        if response.status_code != 200:
            body = response.text
            error = f"Project: {project_name} | Error: status code {response.status_code} | Body: {body}"
            raise Exception(error)

        data = response.json() if response.headers.get("Content-Type", "").startswith("application/json") else None
        if not data or not data.get("ok", False):
            desc = data.get("description") if isinstance(data, dict) else response.text
            error = f"Project: {project_name} | Error: {desc}"
            raise Exception(error)

    except Exception as e:
        error = f"Project: {project_name} | Error: {str(e)}"
        raise Exception(error)
