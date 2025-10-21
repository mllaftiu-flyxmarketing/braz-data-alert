from helper.log import set_log
from models.projects_sessions import (
      table_prefix, 
      table_suffix, 
      get_sessions_with_zero_bets_wins_dates_results, 
      get_ids_for_statistics_with_zero_bets_wins_dates
)


def get_sessions_with_zero_bets_wins(project: dict) -> list:
    table_name = f"{table_prefix}_{project['id']}_{table_suffix}"

    try:
        set_log("Collecting dates with zero amounts for bets and wins", reason="Info", method="get_sessions_with_zero_bets_wins")
        rows = get_sessions_with_zero_bets_wins_dates_results(table_name)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        if len(out) > 0:
            ids_map = get_ids_for_statistics_with_zero_bets_wins_dates(table_name, out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_sessions_with_zero_bets_wins")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_sessions_with_zero_bets_wins")
        return []