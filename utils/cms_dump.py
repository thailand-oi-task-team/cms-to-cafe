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
  
  def get_file_path(self, testcase_id):
    input_file = self.data[testcase_id]["input"]
    output_file = self.data[testcase_id]["output"]
    
    return input_file, output_file