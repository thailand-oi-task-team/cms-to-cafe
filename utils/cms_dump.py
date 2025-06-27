import json

class CMS_Dump:
  def __init__(self, contest_file):
    print(f"Loaded CMS contest data from {contest_file}.")
    json_raw = open(contest_file, "r")
    self.data = json.load(json_raw)
    
  
  def get_contest_ids(self):
    contest_ids = list()
    
    for id in self.data:
      if id.startswith("_"):
        continue
      if self.data[id]["_class"] == "Contest":
        contest_ids.append(id)
    
    return contest_ids
  
  def get_task_ids(self, contest_id):
    task_ids = list()
    
    for id in self.data[contest_id]["tasks"]:
      task_ids.append(id)
    
    return task_ids
  
  def get_task_name(self, task_id):
    return self.data[task_id]["name"]
  
  def get_active_dataset_id(self, task_id):
    return self.data[task_id]["active_dataset"]
  
  def get_testcase_ids(self, active_dataset_id):
    testcase_ids = list()
    
    for testcase_name in self.data[active_dataset_id]["testcases"]:
      testcase_ids.append(self.data[active_dataset_id]["testcases"][testcase_name])
    
    return testcase_ids
  
  def get_test_file(self, testcase_id):
    input_file = self.data[testcase_id]["input"]
    output_file = self.data[testcase_id]["output"]
    
    return input_file, output_file
  
  def get_manager_file_ids(self, active_dataset_id):
    if self.data[active_dataset_id]["managers"] == {}:
      return []
    
    manager_file_ids = list()
    for file_name in self.data[active_dataset_id]["managers"]:
      manager_file_ids.append(self.data[active_dataset_id]["managers"][file_name])
    
    return manager_file_ids
  
  def get_file(self, file_id):
    file_path = self.data[file_id]["digest"]
    file_name = self.data[file_id]["filename"]
    return file_path, file_name
  
  def get_groups(self, active_dataset_id):
    if self.data[active_dataset_id]["score_type"] == "GroupMin":
      return self.data[active_dataset_id]["score_type_parameters"]
    if self.data[active_dataset_id]["score_type"] == "GroupMinPrereq":
      return self.data[active_dataset_id]["score_type_parameters"][1:]
    raise ValueError("Unsupported score type. Only GroupMin and GroupMinPreReq are supported.")

  def get_task_title(self, task_id):
    return self.data[task_id]["title"]
  
  def get_task_limits(self, active_dataset_id):
    time_limit = self.data[active_dataset_id]["time_limit"]
    memory_limit = self.data[active_dataset_id]["memory_limit"]
    memory_limit = int(memory_limit) // 1024 // 1024
    return time_limit, memory_limit

  def get_attachment_file_ids(self, task_id):
    if "attachments" not in self.data[task_id]:
      return []
    
    attachment_file_ids = list()
    for file_name in self.data[task_id]["attachments"]:
      attachment_file_ids.append(self.data[task_id]["attachments"][file_name])
    
    return attachment_file_ids
  
  def get_task_statement_id(self, task_id):
    primary_statement_name = self.data[task_id]["primary_statements"][0]
    primary_statment_id = self.data[task_id]["statements"][primary_statement_name]
    return primary_statment_id
  
  def get_statement(self, statement_id):
    return self.data[statement_id]["digest"]