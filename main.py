import sys
from helper.log import set_log
from helper.validate import set_memory_limit
from classes.projects import get_enabled_projects_ids

def main(reason = "all"):   
     try:
          

          sys.exit(0)
     except Exception as e:
          set_log(str(e), reason="Error", method="main")
          sys.exit(1)

if __name__ == "__main__":
     set_memory_limit() 
     main()
