import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', '.env'))

# Environment variables
environment = os.getenv("ENV", "")
project_name = os.getenv("NAME", "")
memory_limit = os.getenv("MEMORY_LIMIT", "2")

# Collect DB
collect_db_host = os.getenv("COLLECT_DB_HOST", "")
collect_db_user = os.getenv("COLLECT_DB_USER", "")
collect_db_password = os.getenv("COLLECT_DB_PASSWORD", "")
collect_db_name = os.getenv("COLLECT_DB_NAME", "")

# Environment directories
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
storage_dir = os.path.join(app_dir, "storages")
log_dir = os.path.join(app_dir, "logs")
test_dir = os.path.join(app_dir, "tests")
class_dir = os.path.join(app_dir, "classes")
model_dir = os.path.join(app_dir, "models")

# Dates Collection
coll_date_from = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
coll_date_since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# Telegram Bot
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
telegram_topic_id = os.getenv("TELEGRAM_TOPIC_ID", "")
telegram_topic_reply_to_message_id = os.getenv("TELEGRAM_TOPIC_REPLY_TO_MESSAGE_ID", "")
telegram_send_general_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
telegram_send_topic_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"

# Excluded methods for domains
excluded_methods_for_domain = {
    "get_projects_statistics_problem_dates": [
      {
            ".io": ["get_statistics_with_zero_cpas"]
      },
    ],
}