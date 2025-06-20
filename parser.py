#!/bin/python3

import argparse
import os
import shutil

from utils.cms_dump import CMS_Dump

cms_dump = None
file_dir = None

def parse_task(task_id):
  global cms_dump
  
  task_name = cms_dump.get_task_name(task_id)
  active_dataset_id = cms_dump.get_active_dataset_id(task_id)
  
  if task_name != 'd1_dining_car':
    return 
  
  os.mkdir(f"contest_data/{task_name}")
  os.mkdir(f"contest_data/{task_name}/attachment")
  os.mkdir(f"contest_data/{task_name}/checker")
  os.mkdir(f"contest_data/{task_name}/initializers")
  os.mkdir(f"contest_data/{task_name}/managers")
  os.mkdir(f"contest_data/{task_name}/model_solutions")
  os.mkdir(f"contest_data/{task_name}/testcases")
  
  testcase_ids = cms_dump.get_testcase_ids(active_dataset_id)
  test_index = 1
  for testcase_id in testcase_ids:
    input_file, solution_file = cms_dump.get_test_file(testcase_id)
    os.system(f"cp {os.path.join(file_dir, 'files', input_file)} contest_data/{task_name}/testcases/{test_index}.in")
    os.system(f"cp {os.path.join(file_dir, 'files', solution_file)} contest_data/{task_name}/testcases/{test_index}.sol")
    
    test_index += 1
  
  manager_file_ids = cms_dump.get_manager_file_ids(active_dataset_id)
  for file_id in manager_file_ids:
    file_path, file_name = cms_dump.get_file(file_id)
    
    os.system(f"cp {os.path.join(file_dir, 'files', file_path)} contest_data/{task_name}/managers/{file_name}")
    
    if file_name == 'checker':
      os.system(f"mv contest_data/{task_name}/managers/{file_name} contest_data/{task_name}/checker/checker")
  
  groups = cms_dump.get_groups(t)
  
  # TODO: write config file
  with open(f"contest_data/{task_name}/config.yml", "w") as config_file:
    config_file.write("---\n")
    config_file.write("testcases_dir: testcases\n")
    config_file.write("testcases:\n")
    for i in range(1, test_index):
      config_file.write(f"\t '{i}'" )

def main():
  parser = argparse.ArgumentParser(description="Parse CMS contest data.")
  parser.add_argument("--dir", type=str, help="Path to the CMS contest directory", required=True)
  args = parser.parse_args()
  
  global cms_dump
  global file_dir
  
  file_dir = args.dir
  cms_dump = CMS_Dump(os.path.join(file_dir, "contest.json"))

  contest_ids = cms_dump.get_contest_ids()
  
  if os.path.exists("contest_data"):
    shutil.rmtree("contest_data")
  os.mkdir("contest_data")
  
  for contest_id in contest_ids:
    print(f"Contest ID: {contest_id}")
    
    task_ids = cms_dump.get_task_ids(contest_id)
    for task_id in task_ids:
      parse_task(task_id)
  
if __name__ == "__main__":
  main()