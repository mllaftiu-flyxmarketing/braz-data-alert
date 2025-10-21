from models.projects_statistics import (
    get_zero_bets_wins_dates_results,
    get_zero_payments_payouts_dates_results,
    get_missing_dates_results,
)
from helper.log import set_log


def get_zero_bets_wins_dates() -> list:
    try:
        set_log("Collecting dates with zero bets and wins", reason="Info", method="get_zero_bets_wins_dates")
        rows = get_zero_bets_wins_dates_results()
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
        return out
    except Exception as e:
        set_log(str(e), reason="Error", method="get_zero_bets_wins_dates")
        return []


def get_zero_payments_payouts_dates() -> list:
    try:
        set_log("Collecting dates with zero payments and payouts", reason="Info", method="get_zero_payments_payouts_dates")
        rows = get_zero_payments_payouts_dates_results()
        out = []
        for row in rows:
            d = row["date"]
            s = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            out.append(s)
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
        return result
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_statistics_problem_dates")
        return []

