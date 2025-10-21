from helper.log import set_log
from models.projects_statistics import (
    get_zero_bets_wins_dates_results,
    get_zero_payments_payouts_dates_results,
    get_missing_dates_results,
    get_projects_statistics_ids_by_dates,
    get_ids_for_zero_bets_wins_dates,
    get_ids_for_zero_payments_payouts_dates,
    get_zero_cpas_dates_results,
    get_ids_for_zero_cpas_dates,
)


def get_zero_bets_wins(project: dict | None = None) -> list:
    try:
        set_log("Collecting dates with zero amounts for bets and wins", reason="Info", method="get_zero_bets_wins")
        rows = get_zero_bets_wins_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        if len(out) > 0:
            ids_map = get_ids_for_zero_bets_wins_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_zero_bets_wins")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_bets_wins")
        return []


def get_zero_cpas(project: dict | None = None) -> list:
    try:
        set_log("Collecting dates with zero amounts for CPAs", reason="Info", method="get_zero_cpas")
        rows = get_zero_cpas_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        if len(out) > 0:
            ids_map = get_ids_for_zero_cpas_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_zero_cpas")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_cpas")
        return []


def get_zero_payments_payouts(project: dict | None = None) -> list:
    try:
        set_log("Collecting dates with zero amounts for payments and payouts", reason="Info", method="get_zero_payments_payouts")
        rows = get_zero_payments_payouts_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records with zero amounts for payments/payouts", reason="Info", method="get_zero_payments_payouts")
        if len(out) > 0:
            ids_map = get_ids_for_zero_payments_payouts_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_zero_payments_payouts")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_payments_payouts")
        return []


def get_missing(project: dict | None = None) -> list:
    try:
        set_log("Collecting missing dates", reason="Info", method="get_missing")
        rows = get_missing_dates_results(project)
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records for missing dates", reason="Info", method="get_missing")
        if len(out) > 0:
            ids_map = get_projects_statistics_ids_by_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\nRecords with 0 amounts found at\n{'; '.join(parts)}", reason="Error", method="get_missing")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_missing")
        return []


def get_projects_statistics_problem_dates(project: dict | None = None):
    try:
        set_log("Collecting projects_statistics problem dates", reason="Info", method="get_projects_statistics_problem_dates")
        get_zero_bets_wins(project)
        get_zero_payments_payouts(project)
        get_zero_cpas(project)
        get_missing(project)
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_statistics_problem_dates")
        return None

