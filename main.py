import sys
from configs import globals
from helper.log import set_log
from helper.validate import set_memory_limit
from classes.projects import get_enabled_projects
from classes.projects_statistics import get_projects_statistics_problem_dates

def main(reason = "all"):   
     projects = get_enabled_projects()

     try:
          for project in projects:
               globals.project_name = project["title"]
               
               if reason == "projects_statistics" or reason == "all":
                    get_projects_statistics_problem_dates(project)
          sys.exit(0)
     except Exception as e:
          set_log(str(e), reason="Error", method="main")
          sys.exit(1)

if __name__ == "__main__":
     set_memory_limit() 

     if len(sys.argv) > 1:
          if sys.argv[1] == "--projects_statistics":
               main("projects_statistics")
          else:
               set_log("Invalid argument", reason="Error", method="main")
               sys.exit(1)
     else:
          main()
