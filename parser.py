#!/bin/python3

import argparse
import os
import shutil

from utils.cms_dump import CMS_Dump

cms_dump = None
file_dir = None
only_parse_task = None

def parse_task(task_id):
  global cms_dump
  global only_parse_task
  
  task_name = cms_dump.get_task_name(task_id)
  active_dataset_id = cms_dump.get_active_dataset_id(task_id)
  
  if only_parse_task is not None and only_parse_task != task_name:
    print(f"Skipping task {task_name} as it is not in the specified tasks to parse.")
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
  
  found_checker = False
  manager_file_ids = cms_dump.get_manager_file_ids(active_dataset_id)
  for file_id in manager_file_ids:
    file_path, file_name = cms_dump.get_file(file_id)
    
    os.system(f"cp {os.path.join(file_dir, 'files', file_path)} contest_data/{task_name}/managers/{file_name}")
    
    if file_name == 'checker':
      found_checker = True
      os.system(f"mv contest_data/{task_name}/managers/{file_name} contest_data/{task_name}/checker/checker")
  
  groups = cms_dump.get_groups(active_dataset_id)
  
  attachment_file_ids = cms_dump.get_attachment_file_ids(task_id)
  for file_id in attachment_file_ids:
    file_path, file_name = cms_dump.get_file(file_id)
    
    os.system(f"cp {os.path.join(file_dir, 'files', file_path)} contest_data/{task_name}/attachment/{file_name}")
  
  statement_id = cms_dump.get_task_statement_id(task_id)
  statement = cms_dump.get_statement(statement_id)
  os.system(f"cp {os.path.join(file_dir, 'files', statement)} contest_data/{task_name}/statement.pdf")
  
  with open(f"contest_data/{task_name}/config.yml", "w") as config_file:
    config_file.write("---\n")
    config_file.write('testcases_pattern: "*"\n')
    config_file.write("testcases_dir: testcases\n")
    config_file.write("testcases:\n")
    test_index = 1
    group_num = 1
    for group_val in groups:
      score = group_val[0]
      num_tests = group_val[1]
      for i in range(num_tests):
        config_file.write(f"  '{test_index}':\n")
        
        config_file.write(f"    group: {group_num}\n")
        config_file.write(f"    group_name: '{test_index}'\n")
        config_file.write(f"    weight: 1\n")
        
        test_index += 1
      group_num += 1
    
    task_title = cms_dump.get_task_title(task_id)
    time_limit, memory_limit = cms_dump.get_task_limits(active_dataset_id)
    
    if found_checker:
      config_file.write("checker: checker\n")
      config_file.write("checker_dir: checker\n")
    config_file.write(f"name: {task_name}\n")
    config_file.write(f"full_name: {task_title}\n")
    config_file.write("task_type: batch\n")
    config_file.write("compilation_type: with_managers\n")
    config_file.write(f"time_limit: {time_limit}\n")
    config_file.write(f"memory_limit: {memory_limit}\n")
    config_file.write("score_type: group_min\n")
    config_file.write("evaluation_type: custom_cafe\n")
    config_file.write("ds_name: Dataset 1\n")
    config_file.write("managers_dir: managers\n")
    config_file.write("solutions_dir: model_solutions\n")
    config_file.write("initializers_dir: initializers\n")
        
      

def main():
  parser = argparse.ArgumentParser(description="Parse CMS contest data.")
  parser.add_argument("--dir", type=str, help="Path to the CMS contest directory", required=True)
  parser.add_argument("--only", type=str, help="Only parse the specified task", default=None)
  args = parser.parse_args()
  
  global cms_dump
  global file_dir
  global only_parse_task
  
  file_dir = args.dir
  cms_dump = CMS_Dump(os.path.join(file_dir, "contest.json"))
  only_parse_task = args.only.strip() if args.only else None

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