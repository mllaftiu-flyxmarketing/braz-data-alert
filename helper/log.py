import os
import sys
from datetime import datetime
from configs.globals import environment, log_dir, project_name
from helper.validate import create_dir_if_not_exists, create_file_if_not_exists


def format_log(message: str, reason: str = "", method: str = ""):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{date_time} | Project: {project_name} | Method: {method} | {reason}: {message}"

def set_log(message: str, reason: str = "", method: str = "", send_telegram: bool = False):
    create_dir_if_not_exists(log_dir)
    create_file_if_not_exists(log_dir, "globals.log")

    log_file = os.path.join(log_dir, "globals.log")
    formatted_message = format_log(message, reason, method)

    if environment == "local":
        print(f"{formatted_message}")

    if method:
        with open(log_file, mode="a") as f:
            f.write(f"{formatted_message}\n")
    
    if send_telegram or reason in ("Error", "Warning"):
        from helper.telegram import set_telegram_message
        set_telegram_message(formatted_message)