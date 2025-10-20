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

# Store DB
store_db_host = os.getenv("STORE_DB_HOST", "")
store_db_user = os.getenv("STORE_DB_USER", "")
store_db_password = os.getenv("STORE_DB_PASSWORD", "")
store_db_name = os.getenv("STORE_DB_NAME", "")
store_daily_table = os.getenv("STORE_DAILY_TABLE", "")
store_monthly_table = os.getenv("STORE_MONTHLY_TABLE", "")

# Environment directories
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
storage_dir = os.path.join(app_dir, "storages")
log_dir = os.path.join(app_dir, "logs")
test_dir = os.path.join(app_dir, "tests")
class_dir = os.path.join(app_dir, "classes")
model_dir = os.path.join(app_dir, "models")

# Dates Collection
coll_date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
coll_date_since = datetime.now().strftime("%Y-%m-%d")

# Telegram Bot
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
telegram_api_url = (
    os.getenv("TELEGRAM_API_URL", "")
    + telegram_bot_token
    + "/sendMessage?chat_id="
    + telegram_chat_id   
    + "&text="
)
