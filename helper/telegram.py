import requests
from configs.globals import telegram_api_url, project_name

def set_telegram_message(message: str):
    try:
        telegram_url = f"{telegram_api_url}{message}"
        telegram_url = telegram_url.replace(" ", "%20")

        response = requests.get(telegram_url)

        if response.status_code != 200:
            error = f"Project: {project_name} | Error: status code {response.status_code}"
            raise Exception(error)

    except Exception as e:
        error = f"Project: {project_name} | Error: {str(e)}"
        raise Exception(error)