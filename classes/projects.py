from models.projects import get_enabled_projects_results, project_id
from helper.log import set_log


def get_enabled_projects_ids() -> list:
    try:
        set_log("Collecting enabled projects ids", reason="Info", method="get_enabled_projects_ids")
        projects = get_enabled_projects_results()
        return [project[project_id] for project in projects]
    except Exception as e:
        set_log(str(e), reason="Error", method="get_enabled_projects_ids")
        return []


def get_enabled_projects() -> list:
    try:
        set_log("Collecting enabled projects", reason="Info", method="get_enabled_projects")
        return get_enabled_projects_results()
    except Exception as e:
        set_log(str(e), reason="Error", method="get_enabled_projects")
        return []
