from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import archieml
import pandas as pd
from datetime import datetime
from dateutil import parser

from trk import DB_READ_ERROR
from trk.database import DatabaseHandler

class Tracker:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path) # DatabaseHandler component to facilitate direct communication with the to-do database

    def _get_time(self,x = None):        
        if x is None:
            date_time = datetime.now()            
            return date_time
        else:
            date_time = parser.parse(x) 
                      
            return date_time
    def _date_to_string(self,date_time):
        str_date = datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S" )
        return(str_date)

    def _get_task_value(self, string):
        value = string.strip().split(":")[1]
        return(value)


    def _is_value_empty(self,string):
        if ":" in string:
            value = self._get_task_value(string)
            # value = string.strip().split(":")[1]
            if not value:
                return(0)
            else:
                return(1)
        else:
            return(0)

    def _get_information(self,lines): 
        positions = {}
        positions["tasks"] = []
        section = {}
        tracker_start = False
        section_start = False

        for i, line in enumerate(lines): 
            
            
            if line.strip() == "[entries]":
                positions["start"] = i+1
                tracker_start = True
            
            if tracker_start == True:
                
                if "description:" in line.strip():
                    section_start = True
                
                if section_start == True:
                    if "description:" in line.strip():
                        section["description"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "start_time:" in line.strip():
                        section["start_time"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "end_time:" in line.strip():
                        section["end_time"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "project:" in line.strip():
                        section["project"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "task:" in line.strip():
                        section["task"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "client:" in line.strip():
                        section["client"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "billable:" in line.strip():
                        section["billable"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "[.tags]" in line.strip():
                        section["tag_start"] = {"position": i, "value": self._is_value_empty(line.strip())}
                    if "[]" in line.strip():
                        section["tag_end"] = {"position": i, "value": self._is_value_empty(line.strip())}
                        section_start = False

                if section_start == False and len(section) != 0 :
                    
                    positions["tasks"].append(section)
                    section = {}
        return(positions)

    def _parse_active_information(self,positions, lines):
        """
        assumes tat there is only one active task
        """

        ls_tasks = positions["tasks"]
                
        for i in ls_tasks:
            if i["end_time"]["value"] == 0:
                active_task = i
                break
        
        
        description = self._get_task_value(lines[active_task["description"]["position"]].strip())
        start_time = lines[active_task["start_time"]["position"]].split('start_time:')[1].strip()
        project = self._get_task_value(lines[active_task["project"]["position"]].strip())
        task = self._get_task_value(lines[active_task["task"]["position"]].strip())
        client = self._get_task_value(lines[active_task["task"]["position"]].strip())
        billable = self._get_task_value(lines[active_task["billable"]["position"]].strip())

        return (description, start_time, task, project, client, billable  )




    def _check_active_tasks(self,position_dictionary):
        status_result  = {}
        active_tasks = 0
        ls_active_task_positions = []
        for i in position_dictionary["tasks"]:
            status = i["end_time"]["value"]
            position = i["end_time"]["position"]     
            if status == 0:
                active_tasks = active_tasks +1
                ls_active_task_positions.append(position)
        status_result["active_task_count"] = active_tasks
        status_result["active_task_index"] = ls_active_task_positions
                
        return(status_result)


    def _parse_time(self, time):
        if (time is None):
            time = self._get_time()                
            time = self._date_to_string(time)
        else:
            time =  self._get_time(time)
            time = self._date_to_string(time)
        return(time)

    
    def start(self, description, start_time, project, task, client, billable, tags):
        """Add a new event to the database."""
        lines = self._db_handler.read_task_text()    
        end_time = ""         
           
        start_time = self._parse_time(start_time)
            

        positions = self._get_information(lines)
         
        status = self._check_active_tasks(positions)

        if  status["active_task_count"] == 1:
            error = "Error: End task still in progress before starting new task"
            return(start_time,error)
        

        elif status["active_task_count"] > 1:
            error = "Error: Multiple Tasks Open"
            return(start_time,error)
        else:
            entry = f"{chr(10)}{chr(10)}description:{description}{chr(10)}start_time:{start_time}{chr(10)}end_time:{end_time}{chr(10)}project:{project}{chr(10)}task:{task}{chr(10)}client:{client}{chr(10)}billable:{billable}{chr(10)}[.tags]{chr(10)}[]{chr(10)}---{chr(10)}"
            error = None
            index = positions["start"] 
            lines[index] = entry
            self._db_handler.write_task_text(lines)
            return(start_time, error)   

    def _calculate_minutes(self, start_time, end_time):

        start_time = self._get_time(start_time) 
        end_time = self._get_time(end_time) 
        c = end_time - start_time
        minutes = c.total_seconds()/60
        minutes = str(round(minutes, 3))
        return(minutes)
        

    
    def stop(self, end_time):
        lines = self._db_handler.read_task_text()       

        end_time = self._parse_time(end_time)
            

        positions = self._get_information(lines)    
        status = self._check_active_tasks(positions)

        

        if  status["active_task_count"] > 1:
            error = "Error: Multiple Tasks Open"
            return(end_time,error)  
        elif status["active_task_count"] == 0:
            error = "Error: No Tasks Open"
            return(end_time,error) 
        else:            
            error = None
            description, start_time, task, project, client, billable  = self._parse_active_information(positions, lines)
            entry = f"{end_time}{chr(10)}"
            index = status["active_task_index"][0]
            lines[index] = f"end_time: {entry}"
            self._db_handler.write_task_text(lines)
            minutes = self._calculate_minutes(start_time, end_time)
            
            return(description, start_time, end_time, minutes,  task, project, client, billable,  error)





