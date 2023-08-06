"""This module provides the RP To-Do database functionality."""
# rptodo/database.py

import configparser
import json
import archieml
import pandas
from pathlib import Path

from trk import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

template = """:skip
################ Time Tracker #########################

------------- Template -------------


description: 
start_time:
end_time:
project:
task:
client:
billable: no
[.tags]
[]
---

--------------------------------------
:endskip

[entries]   
  
        """

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.aml"
)

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text(template)  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    

    def read_task_text(self):
        try:


            with open(self._db_path) as fp:
                self.db_trk_lines =  fp.readlines()
                
            
            
            return(self.db_trk_lines)
           
        except OSError:
            print("ERROR Happened")

    def read_task_df(self):


            pass


    def write_task_text(self, lines) :
        try:
            with open(self._db_path, "w") as fp:
                fp.writelines(lines)             
           
           
        except OSError:  # Catch file IO problems
            return DB_WRITE_ERROR