from helper.database import open_coll_connection, close_coll_connection
from helper.log import set_log
from configs.globals import coll_date_from, coll_date_since
from datetime import datetime, timedelta, date
from typing import cast, Dict, Any

table_name = "projects_statistics"
projects_statistics_id = "id"
projects_statistics_date = "date"
projects_statistics_project_id = "project_id"
projects_statistics_customer_id = "customer_id"
projects_statistics_partner_id = "partner_id"
projects_statistics_promo_id = "promo_id"
projects_statistics_payments = "payments"
projects_statistics_payouts = "payouts"
projects_statistics_bets = "bets"
projects_statistics_wins = "wins"


def get_projects_statistics_results() -> list:
    projects_statistics = []

    try:
        query = f"SELECT {projects_statistics_id}, {projects_statistics_date}, {projects_statistics_project_id}, {projects_statistics_customer_id}, {projects_statistics_partner_id}, {projects_statistics_promo_id}, {projects_statistics_payments}, {projects_statistics_payouts}, {projects_statistics_bets}, {projects_statistics_wins} FROM {table_name}"

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        projects_statistics = cursor.fetchall()

        cursor.close()
        close_coll_connection(conn)

        return projects_statistics
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_statistics_results")
        return []


def get_zero_bets_wins_dates_results() -> list:
    dates = []

    try:
        start = datetime.strptime(coll_date_from, "%Y-%m-%d").date()
        end = datetime.strptime(coll_date_since, "%Y-%m-%d").date()

        query = (
            f"SELECT {projects_statistics_date} AS date "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} BETWEEN %s AND %s "
            f"GROUP BY {projects_statistics_date} "
            f"HAVING COALESCE(SUM({projects_statistics_bets}), 0) = 0 "
            f"AND COALESCE(SUM({projects_statistics_wins}), 0) = 0"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (start, end))
        dates = cursor.fetchall()

        cursor.close()
        close_coll_connection(conn)

        return dates
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_bets_wins_dates_results")
        return []


def get_zero_payments_payouts_dates_results() -> list:
    dates = []

    try:
        start = datetime.strptime(coll_date_from, "%Y-%m-%d").date()
        end = datetime.strptime(coll_date_since, "%Y-%m-%d").date()

        query = (
            f"SELECT {projects_statistics_date} AS date "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} BETWEEN %s AND %s "
            f"GROUP BY {projects_statistics_date} "
            f"HAVING COALESCE(SUM({projects_statistics_payments}), 0) = 0 "
            f"AND COALESCE(SUM({projects_statistics_payouts}), 0) = 0"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (start, end))
        dates = cursor.fetchall()

        cursor.close()
        close_coll_connection(conn)

        return dates
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_payments_payouts_dates_results")
        return []


def get_missing_dates_results() -> list:
    dates = []

    try:
        start = datetime.strptime(coll_date_from, "%Y-%m-%d").date()
        end = datetime.strptime(coll_date_since, "%Y-%m-%d").date()

        query = (
            f"SELECT DISTINCT {projects_statistics_date} AS date "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} BETWEEN %s AND %s "
            f"ORDER BY {projects_statistics_date}"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (start, end))
        present_rows = cursor.fetchall()

        cursor.close()
        close_coll_connection(conn)

        present_dates = set()
        for raw in present_rows:
            row = cast(Dict[str, Any], raw)
            d = row["date"]
            if isinstance(d, datetime):
                present_dates.add(d.date())
            elif isinstance(d, date):
                present_dates.add(d)
            elif isinstance(d, str):
                present_dates.add(datetime.strptime(d, "%Y-%m-%d").date())

        total_days = (end - start).days + 1
        full_range = {start + timedelta(days=i) for i in range(total_days)}
        missing = sorted(full_range - present_dates)

        dates = [{"date": m} for m in missing]
        return dates
    except Exception as e:
        set_log(str(e), reason="Error", method="get_missing_dates_results")
        return []
