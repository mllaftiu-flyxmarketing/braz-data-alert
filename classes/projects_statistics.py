from helper.log import set_log
from configs.globals import excluded_methods_for_domain
from models.projects_statistics import (
    get_statistics_with_zero_bets_wins_dates_results,
    get_statistics_with_zero_payments_payouts_dates_results,
    get_statistics_with_missings_dates_results,
    get_projects_statistics_ids_by_dates,
    get_ids_for_statistics_zero_bets_wins_dates,
    get_ids_for_statistics_zero_payments_payouts_dates,
    get_statistics_with_zero_cpas_dates_results,
    get_ids_for_statistics_zero_cpas_dates,
)


def get_statistics_with_zero_bets_wins(project: dict) -> list:
    try:
        set_log("Collecting dates with zero amounts for bets and wins", reason="Info", method="get_statistics_with_zero_bets_wins")
        rows = get_statistics_with_zero_bets_wins_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        if len(out) > 0:
            ids_map = get_ids_for_statistics_zero_bets_wins_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_statistics_with_zero_bets_wins")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_statistics_with_zero_bets_wins")
        return []


def get_statistics_with_zero_cpas(project: dict) -> list:
    try:
        set_log("Collecting dates with zero amounts for CPAs", reason="Info", method="get_statistics_with_zero_cpas")
        rows = get_statistics_with_zero_cpas_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        if len(out) > 0:
            ids_map = get_ids_for_statistics_zero_cpas_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_statistics_with_zero_cpas")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_statistics_with_zero_cpas")
        return []


def get_statistics_with_zero_payments_payouts(project: dict) -> list:
    try:
        set_log("Collecting dates with zero amounts for payments and payouts", reason="Info", method="get_statistics_with_zero_payments_payouts")
        rows = get_statistics_with_zero_payments_payouts_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records with zero amounts for payments/payouts", reason="Info", method="get_zero_payments_payouts")
        if len(out) > 0:
            ids_map = get_ids_for_statistics_zero_payments_payouts_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_statistics_with_zero_payments_payouts")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_statistics_with_zero_payments_payouts")
        return []


def get_statistics_with_missings(project: dict) -> list:
    try:
        set_log("Collecting missing dates", reason="Info", method="get_missing")
        rows = get_statistics_with_missings_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records for missing dates", reason="Info", method="get_statistics_with_missings")
        if len(out) > 0:
            ids_map = get_projects_statistics_ids_by_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_statistics_with_missings")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_statistics_with_missings")
        return []


def get_projects_statistics_problem_dates(project: dict):
    try:
        set_log("Collecting projects_statistics problem dates", reason="Info", method="get_projects_statistics_problem_dates")
        domain = project.get("domain") if isinstance(project, dict) else None
        excluded = set()

        cfg_entry = excluded_methods_for_domain.get("get_projects_statistics_problem_dates", {})
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
            set_log("No exclusions matched; running all statistics checks", reason="Info", method="get_projects_statistics_problem_dates")

        methods_map = {
            "get_statistics_with_zero_bets_wins": get_statistics_with_zero_bets_wins,
            "get_statistics_with_zero_payments_payouts": get_statistics_with_zero_payments_payouts,
            "get_statistics_with_zero_cpas": get_statistics_with_zero_cpas,
            "get_statistics_with_missings": get_statistics_with_missings,
        }
        order = [
            "get_statistics_with_zero_bets_wins",
            "get_statistics_with_zero_payments_payouts",
            "get_statistics_with_zero_cpas",
            "get_statistics_with_missings",
        ]

        for name in order:
            if name in excluded:
                if domain:
                    set_log(f"Excluding {name} for {domain}", reason="Info", method="get_projects_statistics_problem_dates")
                continue
            methods_map[name](project)
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_statistics_problem_dates")
        return None

