import requests
from typing import Optional
from datetime import datetime
from configs.globals import (
    coll_date_from,
    coll_date_since,
)
from configs.globals import (
    telegram_send_general_message_url,
    telegram_send_topic_message_url,
    telegram_chat_id,
    telegram_topic_id,
    telegram_topic_reply_to_message_id,
    project_name,
)

MAX_TELEGRAM_MESSAGE_LENGTH = 3900


def _truncate_message(msg: str) -> str:
    if not isinstance(msg, str):
        msg = str(msg)
    if len(msg) <= MAX_TELEGRAM_MESSAGE_LENGTH:
        return msg
    keep = MAX_TELEGRAM_MESSAGE_LENGTH - 50
    suffix = f"... (truncated {len(msg) - keep} chars)"
    return msg[:keep] + suffix


def format_topic_message(message: str, reason: str, method: str) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    reasoning = method.replace("_", " ").title()
    reasoning = reasoning.replace("Get", "Found").title()
    message = message.replace("; ", "\n")
    
    header = (
        f"📅 **Date Range**\n{coll_date_from} - {coll_date_since}\n\n"
        f"🗄 **Project**\n{project_name}\n\n"
        f"⏱️ **Run at**\n{date_str}\n\n"
        f"📝 **Description**\n{reasoning}\n\n"
        f"🎯 **Method**\n{method}\n\n"
        f"📌 **{reason}**{message}"
    )
    return header


def set_telegram_general_message(message: str, chat_id: Optional[str] = None, thread_id: Optional[str] = None):
    try:
        target_chat_id = chat_id if chat_id else telegram_chat_id
        payload = {
            "chat_id": target_chat_id,
            "text": _truncate_message(message),
            "parse_mode": "HTML",
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
            "text": _truncate_message(message),
            "parse_mode": "HTML",
        }

        use_thread_id = thread_id if thread_id is not None else telegram_topic_id
        if use_thread_id and str(use_thread_id).strip() != "":
            payload["message_thread_id"] = str(use_thread_id)
        else:
            use_reply_id = reply_to_message_id if reply_to_message_id is not None else telegram_topic_reply_to_message_id
            if use_reply_id and str(use_reply_id).strip() != "":
                payload["reply_to_message_id"] = str(use_reply_id)

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
