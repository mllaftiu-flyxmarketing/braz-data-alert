from helper.database import open_coll_connection, close_coll_connection
from helper.log import set_log

table_name = "projects"
project_id = "id"
project_title = "title"
project_slug = "slug"
project_domain = "domain"
project_status = "is_enabled"
project_visibility = "is_visible"


def get_enabled_projects_results() -> list:
    projects = []

    try:
        query = f"SELECT {project_id}, {project_title}, {project_slug}, {project_domain} FROM {table_name} WHERE is_enabled = 1 AND is_visible = 1"

        conn = open_coll_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        projects = cursor.fetchall()
        cursor.close()
        close_coll_connection(conn)

        return projects
    except Exception as e:
        set_log(str(e), reason="Error", method="get_enabled_projects_results")
        return []
