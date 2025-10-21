from helper.log import set_log
from configs.globals import excluded_methods_for_domain
from models.projects_sessions import (
      table_prefix, 
      table_suffix, 
      get_sessions_with_zero_bets_wins_dates_results, 
      get_ids_for_statistics_with_zero_bets_wins_dates,
      get_sessions_missing_dates_results,
      get_sessions_ids_by_dates,
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

def get_projects_sessions_problem_dates(project: dict) -> list:
    try:
        set_log("Collecting projects_sessions problem dates", reason="Info", method="get_projects_sessions_problem_dates")
        domain = project.get("domain") if isinstance(project, dict) else None
        excluded = set()
        cfg_entry = excluded_methods_for_domain.get("get_projects_sessions_problem_dates", {})
        items = []
        if isinstance(cfg_entry, dict):
            items = list(cfg_entry.items())
        elif isinstance(cfg_entry, list):
            for entry in cfg_entry:
                if isinstance(entry, dict):
                    items.extend(entry.items())

        if domain and items:
            for key, methods in items:
                if domain == key or domain.endswith(key):
                    excluded.update(methods if isinstance(methods, list) else [])
        if not excluded:
            set_log("No exclusions matched; running all session checks", reason="Info", method="get_projects_sessions_problem_dates")

        methods_map = {
            "get_sessions_with_zero_bets_wins": get_sessions_with_zero_bets_wins,
            "get_sessions_with_missings": get_sessions_with_missings,
        }
        order = [
            "get_sessions_with_zero_bets_wins",
            "get_sessions_with_missings",
        ]

        for name in order:
            if name in excluded:
                if domain:
                    set_log(f"Excluding {name} for {domain}", reason="Info", method="get_projects_sessions_problem_dates")
                continue
            methods_map[name](project)
        return []
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_sessions_problem_dates")
        return []


def get_sessions_with_missings(project: dict) -> list:
    table_name = f"{table_prefix}_{project['id']}_{table_suffix}"
    try:
        set_log("Collecting missing dates", reason="Info", method="get_sessions_with_missings")
        rows = get_sessions_missing_dates_results(table_name)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records for missing dates", reason="Info", method="get_sessions_with_missings")
        if len(out) > 0:
            ids_map = get_sessions_ids_by_dates(table_name, out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_sessions_with_missings")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_sessions_with_missings")
        return []


def get_sessions_with_missing_dates(project: dict) -> list:
    table_name = f"{table_prefix}_{project['id']}_{table_suffix}"
    try:
        set_log("Collecting missing dates", reason="Info", method="get_sessions_with_missing_dates")
        rows = get_sessions_missing_dates_results(table_name)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records for missing dates", reason="Info", method="get_sessions_with_missing_dates")
        if len(out) > 0:
            ids_map = get_sessions_ids_by_dates(table_name, out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with missing dates found at\n{'; '.join(parts)}", reason="Error", method="get_sessions_with_missing_dates")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_sessions_with_missing_dates")
        return []