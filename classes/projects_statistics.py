from models.projects_statistics import (
    get_zero_bets_wins_dates_results,
    get_zero_payments_payouts_dates_results,
    get_missing_dates_results,
    get_projects_statistics_ids_by_dates,
    get_ids_for_zero_bets_wins_dates,
    get_ids_for_zero_payments_payouts_dates,
)
from helper.log import set_log


def get_zero_bets_wins_dates() -> list:
    try:
        set_log("Collecting dates with zero amounts for bets and wins", reason="Info", method="get_zero_bets_wins_dates")
        rows = get_zero_bets_wins_dates_results()
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
            set_log(f"\n 0 amounts found at {'; '.join(parts)}", reason="Error", method="get_zero_bets_wins_dates")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_bets_wins_dates")
        return []


def get_zero_payments_payouts_dates() -> list:
    try:
        set_log("Collecting dates with zero amounts for payments and payouts", reason="Info", method="get_zero_payments_payouts_dates")
        rows = get_zero_payments_payouts_dates_results()
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records with zero amounts for payments/payouts", reason="Info", method="get_zero_payments_payouts_dates")
        if len(out) > 0:
            ids_map = get_ids_for_zero_payments_payouts_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\n 0 amounts found at {'; '.join(parts)}", reason="Error", method="get_zero_payments_payouts_dates")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_payments_payouts_dates")
        return []


def get_missing_dates() -> list:
    try:
        set_log("Collecting missing dates", reason="Info", method="get_missing_dates")
        rows = get_missing_dates_results()
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        set_log(f"Collected {len(out)} records for missing dates", reason="Info", method="get_missing_dates")
        if len(out) > 0:
            ids_map = get_projects_statistics_ids_by_dates(out)
            parts = []
            for d in out:
                ids = ids_map.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\n 0 amounts found at {'; '.join(parts)}", reason="Error", method="get_missing_dates")
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_missing_dates")
        return []


def get_projects_statistics_problem_dates() -> list:
    try:
        set_log("Collecting projects_statistics problem dates", reason="Info", method="get_projects_statistics_problem_dates")
        zero_bw = set(get_zero_bets_wins_dates())
        zero_pp = set(get_zero_payments_payouts_dates())
        missing = set(get_missing_dates())

        all_dates = sorted(zero_bw.union(zero_pp).union(missing))
        result = []
        for d in all_dates:
            issues = []
            if d in zero_bw:
                issues.append("bets_wins_zero")
            if d in zero_pp:
                issues.append("payments_payouts_zero")
            if d in missing:
                issues.append("missing_date")
            result.append({"date": d, "issues": issues})
        set_log(f"Collected {len(result)} records with problem dates", reason="Info", method="get_projects_statistics_problem_dates")
        if len(result) > 0:
            # Build IDs per-date only for dates with actual issues using condition-specific helpers
            ids_bw = get_ids_for_zero_bets_wins_dates(sorted(zero_bw))
            ids_pp = get_ids_for_zero_payments_payouts_dates(sorted(zero_pp))
            merged: dict[str, list] = {}
            for d, arr in ids_bw.items():
                merged.setdefault(d, []).extend(arr)
            for d, arr in ids_pp.items():
                merged.setdefault(d, []).extend(arr)
            parts = []
            for d in all_dates:
                ids = merged.get(d, [])
                if ids:
                    parts.append(f"date {d} & id(s) {', '.join(str(i) for i in sorted(set(ids)))}")
                else:
                    parts.append(f"date {d}")
            set_log(f"\n 0 amounts found at {'; '.join(parts)}", reason="Error", method="get_projects_statistics_problem_dates")
        return result
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_statistics_problem_dates")
        return []

