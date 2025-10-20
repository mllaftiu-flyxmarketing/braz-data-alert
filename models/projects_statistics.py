from helper.database import open_coll_connection, close_coll_connection
from helper.log import set_log

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

        close_coll_connection(conn)

        return projects_statistics
    except Exception as e:
        set_log(str(e), reason="Error", method="get_projects_statistics_results")
        return []
