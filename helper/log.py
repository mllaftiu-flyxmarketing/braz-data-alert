import os
from datetime import datetime
import configs.globals as cfg
from helper.validate import create_dir_if_not_exists, create_file_if_not_exists


def format_log(message: str, reason: str = "", method: str = ""):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{date_time} | Project: {cfg.project_name} | Method: {method} | {reason}: {message}"

def set_log(message: str, reason: str = "", method: str = "", send_telegram: bool = False):
    create_dir_if_not_exists(cfg.log_dir)
    create_file_if_not_exists(cfg.log_dir, "globals.log")

    log_file = os.path.join(cfg.log_dir, "globals.log")
    formatted_message = format_log(message, reason, method)

    if cfg.environment == "local":
        print(f"{formatted_message}")

    if method:
        with open(log_file, mode="a") as f:
            f.write(f"{formatted_message}\n")
    
    if send_telegram or reason in ("Error", "Warning"):
        from helper.telegram import set_telegram_topic_message, format_topic_message
        topic_text = format_topic_message(message, reason, method)
        set_telegram_topic_message(topic_text)