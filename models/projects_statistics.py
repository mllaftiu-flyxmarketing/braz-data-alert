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
projects_statistics_cpa_amount = "cpa_amount"


def get_projects_statistics_results() -> list:
    projects_statistics = []

    try:
        query = f"SELECT {projects_statistics_id}, {projects_statistics_date}, {projects_statistics_project_id}, {projects_statistics_customer_id}, {projects_statistics_partner_id}, {projects_statistics_promo_id}, {projects_statistics_payments}, {projects_statistics_payouts}, {projects_statistics_bets}, {projects_statistics_wins}, {projects_statistics_cpa_amount} FROM {table_name}"

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        projects_statistics = cursor.fetchall()
        set_log(f"Fetched {len(projects_statistics)} rows", reason="Info", method="get_projects_statistics_results")

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
        set_log(f"Fetched {len(dates)} dates with zero bets and wins", reason="Info", method="get_zero_bets_wins_dates_results")

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
        set_log(f"Fetched {len(dates)} dates with zero payments and payouts", reason="Info", method="get_zero_payments_payouts_dates_results")

        cursor.close()
        close_coll_connection(conn)

        return dates
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_payments_payouts_dates_results")
        return []


def get_zero_cpas_dates_results() -> list:
    dates = []

    try:
        start = datetime.strptime(coll_date_from, "%Y-%m-%d").date()
        end = datetime.strptime(coll_date_since, "%Y-%m-%d").date()

        query = (
            f"SELECT {projects_statistics_date} AS date "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} BETWEEN %s AND %s "
            f"GROUP BY {projects_statistics_date} "
            f"HAVING COALESCE(SUM({projects_statistics_cpa_amount}), 0) = 0"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (start, end))
        dates = cursor.fetchall()
        set_log(f"Fetched {len(dates)} dates with zero CPA amounts", reason="Info", method="get_zero_cpas_dates_results")

        cursor.close()
        close_coll_connection(conn)

        return dates
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_cpas_dates_results")
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
        set_log(f"Fetched {len(present_rows)} present dates in range", reason="Info", method="get_missing_dates_results")

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


def get_projects_statistics_ids_by_dates(dates: list) -> dict:
    ids_map: Dict[str, list] = {}
    try:
        if not dates:
            return ids_map

        norm_dates = []
        for d in dates:
            if isinstance(d, datetime):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            elif isinstance(d, date):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            else:
                norm_dates.append(str(d))

        placeholders = ",".join(["%s"] * len(norm_dates))
        query = (
            f"SELECT {projects_statistics_date} AS date, MIN({projects_statistics_id}) AS id "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} IN ({placeholders}) "
            f"GROUP BY {projects_statistics_date} "
            f"ORDER BY {projects_statistics_date}"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, norm_dates)
        rows = cursor.fetchall()
        set_log(f"Fetched {len(rows)} IDs for tracking", reason="Info", method="get_projects_statistics_ids_by_dates")

        cursor.close()
        close_coll_connection(conn)

        for raw in rows:
            row = cast(Dict[str, Any], raw)
            d = row["date"]
            if isinstance(d, datetime):
                key = d.strftime("%Y-%m-%d")
            elif isinstance(d, date):
                key = d.strftime("%Y-%m-%d")
            else:
                key = str(d)
            ids_map.setdefault(key, []).append(row["id"])

        return ids_map
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_statistics_ids_by_dates")
        return {}


def get_ids_for_zero_bets_wins_dates(dates: list) -> dict:
    ids_map: Dict[str, list] = {}
    try:
        if not dates:
            return ids_map

        norm_dates = []
        for d in dates:
            if isinstance(d, datetime):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            elif isinstance(d, date):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            else:
                norm_dates.append(str(d))

        placeholders = ",".join(["%s"] * len(norm_dates))
        query = (
            f"SELECT {projects_statistics_date} AS date, MIN({projects_statistics_id}) AS id "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} IN ({placeholders}) "
            f"AND COALESCE({projects_statistics_bets}, 0) = 0 "
            f"AND COALESCE({projects_statistics_wins}, 0) = 0 "
            f"GROUP BY {projects_statistics_date} "
            f"ORDER BY {projects_statistics_date}"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, norm_dates)
        rows = cursor.fetchall()
        set_log(f"Fetched {len(rows)} IDs for zero bets/wins tracking", reason="Info", method="get_ids_for_zero_bets_wins_dates")

        cursor.close()
        close_coll_connection(conn)

        for raw in rows:
            row = cast(Dict[str, Any], raw)
            d = row["date"]
            if isinstance(d, datetime):
                key = d.strftime("%Y-%m-%d")
            elif isinstance(d, date):
                key = d.strftime("%Y-%m-%d")
            else:
                key = str(d)
            ids_map.setdefault(key, []).append(row["id"])
        return ids_map
    except Exception as e:
        set_log(str(e), reason="Error", method="get_ids_for_zero_bets_wins_dates")
        return {}


def get_ids_for_zero_payments_payouts_dates(dates: list) -> dict:
    ids_map: Dict[str, list] = {}
    try:
        if not dates:
            return ids_map

        norm_dates = []
        for d in dates:
            if isinstance(d, datetime):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            elif isinstance(d, date):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            else:
                norm_dates.append(str(d))

        placeholders = ",".join(["%s"] * len(norm_dates))
        query = (
            f"SELECT {projects_statistics_date} AS date, MIN({projects_statistics_id}) AS id "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} IN ({placeholders}) "
            f"AND COALESCE({projects_statistics_payments}, 0) = 0 "
            f"AND COALESCE({projects_statistics_payouts}, 0) = 0 "
            f"GROUP BY {projects_statistics_date} "
            f"ORDER BY {projects_statistics_date}"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, norm_dates)
        rows = cursor.fetchall()
        set_log(f"Fetched {len(rows)} IDs for zero payments/payouts tracking", reason="Info", method="get_ids_for_zero_payments_payouts_dates")

        cursor.close()
        close_coll_connection(conn)

        for raw in rows:
            row = cast(Dict[str, Any], raw)
            d = row["date"]
            if isinstance(d, datetime):
                key = d.strftime("%Y-%m-%d")
            elif isinstance(d, date):
                key = d.strftime("%Y-%m-%d")
            else:
                key = str(d)
            ids_map.setdefault(key, []).append(row["id"])
        return ids_map
    except Exception as e:
        set_log(str(e), reason="Error", method="get_ids_for_zero_payments_payouts_dates")
        return {}


def get_ids_for_zero_cpas_dates(dates: list) -> dict:
    ids_map: Dict[str, list] = {}
    try:
        if not dates:
            return ids_map

        norm_dates = []
        for d in dates:
            if isinstance(d, datetime):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            elif isinstance(d, date):
                norm_dates.append(d.strftime("%Y-%m-%d"))
            else:
                norm_dates.append(str(d))

        placeholders = ",".join(["%s"] * len(norm_dates))
        query = (
            f"SELECT {projects_statistics_date} AS date, MIN({projects_statistics_id}) AS id "
            f"FROM {table_name} "
            f"WHERE {projects_statistics_date} IN ({placeholders}) "
            f"AND COALESCE({projects_statistics_cpa_amount}, 0) = 0 "
            f"GROUP BY {projects_statistics_date} "
            f"ORDER BY {projects_statistics_date}"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, norm_dates)
        rows = cursor.fetchall()
        set_log(f"Fetched {len(rows)} IDs for zero CPA tracking", reason="Info", method="get_ids_for_zero_cpas_dates")

        cursor.close()
        close_coll_connection(conn)

        for raw in rows:
            row = cast(Dict[str, Any], raw)
            d = row["date"]
            if isinstance(d, datetime):
                key = d.strftime("%Y-%m-%d")
            elif isinstance(d, date):
                key = d.strftime("%Y-%m-%d")
            else:
                key = str(d)
            ids_map.setdefault(key, []).append(row["id"])
        return ids_map
    except Exception as e:
        set_log(str(e), reason="Error", method="get_ids_for_zero_cpas_dates")
        return {}
