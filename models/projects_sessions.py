from helper.log import set_log
from typing import Dict, Any, cast
from datetime import datetime, date
from configs.globals import coll_date_from, coll_date_since
from helper.database import open_coll_connection, close_coll_connection

table_prefix = "projects"
table_suffix = "sessions"
projects_sessions_id = "id"
projects_sessions_date = "date"
projects_sessions_bets = "bets"
projects_sessions_wins = "wins"

def get_sessions_with_zero_bets_wins_dates_results(table_name: str) -> list:
    dates = []

    try:
        start = datetime.strptime(coll_date_from, "%Y-%m-%d").date()
        end = datetime.strptime(coll_date_since, "%Y-%m-%d").date()

        params = [start, end]
        query = (
            f"SELECT {projects_sessions_date} AS date "
            f"FROM {table_name} "
            f"WHERE {projects_sessions_date} BETWEEN %s AND %s "
        )
        query += (
            f"GROUP BY {projects_sessions_date} "
            f"HAVING COALESCE(SUM({projects_sessions_bets}), 0) = 0 "
            f"AND COALESCE(SUM({projects_sessions_wins}), 0) = 0"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        dates = cursor.fetchall()
        set_log(f"Fetched {len(dates)} dates with zero bets and wins", reason="Info", method="get_sessions_with_zero_bets_wins_dates_results")

        cursor.close()
        close_coll_connection(conn)

        return dates
    except Exception as e:
        set_log(str(e), reason="Error", method="get_sessions_with_zero_bets_wins_dates_results")
        return []


def get_ids_for_statistics_with_zero_bets_wins_dates(table_name: str, dates: list) -> dict:
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
            f"SELECT {projects_sessions_date} AS date, MIN({projects_sessions_id}) AS id "
            f"FROM {table_name} "
            f"WHERE {projects_sessions_date} IN ({placeholders}) "
            f"AND COALESCE({projects_sessions_bets}, 0) = 0 "
            f"AND COALESCE({projects_sessions_wins}, 0) = 0 "
            f"GROUP BY {projects_sessions_date} "
            f"ORDER BY {projects_sessions_date}"
        )

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, norm_dates)
        rows = cursor.fetchall()
        set_log(f"Fetched {len(rows)} IDs for zero bets/wins tracking", reason="Info", method="get_ids_for_statistics_zero_bets_wins_dates")

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
        set_log(str(e), reason="Error", method="get_ids_for_statistics_zero_bets_wins_dates")
        return {}