import os
import json
from decimal import Decimal
from helper.log import set_log
from configs.globals import storage_dir, environment
from helper.validate import create_file_if_not_exists, create_dir_if_not_exists


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)

def store_to_storage(content, file_name: str, file_format = ""):
     if environment == "local":
          if file_format:
               with open(storage_dir + "/" + file_name + "." + file_format, "w") as f:
                    f.write(content)
          else:
               with open(storage_dir + "/" + file_name + ".txt", "w") as f:
                    f.write(content)
     
def store_to_json(content, file_name: str):
    try:
        create_dir_if_not_exists(storage_dir)
        create_file_if_not_exists(storage_dir, file_name + ".json")

        file_path = os.path.join(storage_dir, f"{file_name}.json")
        
        with open(file_path, "w") as f:
            json.dump(content, f, indent=4, cls=DecimalEncoder)
        return True
    except Exception as e:
        set_log(f"Error storing JSON: {str(e)}", "Error", "store_to_json")
        return False