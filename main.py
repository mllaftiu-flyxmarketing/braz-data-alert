import sys
from helper.log import set_log
from helper.validate import set_memory_limit
from classes.projects_statistics import get_projects_statistics_problem_dates

def main(reason = "all"):   
     try:
          if reason == "projects_statistics" or reason == "all":
               get_projects_statistics_problem_dates()
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
