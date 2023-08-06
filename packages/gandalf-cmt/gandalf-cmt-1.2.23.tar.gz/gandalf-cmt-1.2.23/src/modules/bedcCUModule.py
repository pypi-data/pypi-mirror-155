#######################################################################################################################################################
#  Description: This Python script is used to define the mav_bedc_cu_module module that make changes to the 
#               delete flag, redeploy flag, sanity_check flag, validation floag, change cnfNetworkFunction value, helm chart key on a mass scale 
#               and any new addition to values.yaml files.
#               
#  Author: Arjun Babu (arbnair97@gmail.com)
#  Created date: 03/06/2022
#
#  Python compatible version: 3.10.4
#  
#  Modifications:
#  1. 
#
#######################################################################################################################################################

from itertools import *
import json
from pathlib import Path
import numpy as np




def mav_bedc_cu_module(delete_flag, redeploy_flag, sanity_check_flag, validation_check_flag, chart_version, cnf_package_version, eks_level_folders ):
    '''
    Info: This Function is used to loop through all the EKS cluster level folders, parse the current values of delete flag, redeploy flag, sanity_check flag, validation flag, updates the new cnfPackageVersion and chart key value.
    '''
    try:

        # Creation of empty lists for processing.
        unfiltered_chart_key_list = []
        unfiltered_cnf_nw_fn_list = []

        # This code block is used to grep the value of chart_key and cnfPackageVersionFile in application_config.json and config.json across all the EKS cluster folders, append to a list and create a filtered list with unique values.
        for repo_path in eks_level_folders:

            application_config_path = f'{repo_path}'+'/application_config.json'
            config_json_path = f'{repo_path}'+'/config.json'

            # Opens application_config.json, grep the value of chart_key and put it in the unfiltered_chart_key_list list.
            with open(application_config_path, 'r') as applicatipon_json_FileRead:
                app_data = json.load(applicatipon_json_FileRead) 
                chart_key_counter = (str((app_data['profiles']['mav_bedc']['charts'])).count('chart_key'))

                for iteration in range(0, chart_key_counter):
                    chart_keys = (app_data['profiles']['mav_bedc']['charts'][iteration]['chart_key'])
                    unfiltered_chart_key_list.append(str(chart_keys))
            

            # Opens config.json, grep the value of cnfPackageVersionFile and put it in the unfiltered_cnf_nw_fn_list list.
            with open(config_json_path, 'r') as config_jsonFileRead:
                config_data = json.load(config_jsonFileRead) 

                cnf_nw_fn = (config_data['cnfPackageVersionFile'])
                unfiltered_cnf_nw_fn_list.append(str(cnf_nw_fn))


        # filters unfiltered_chart_key_list and create chart_key_list with unique chart values. (Filter process)
        numpy_array = np.array(unfiltered_chart_key_list)
        chart_key_list = np.unique(numpy_array)

        # filters unfiltered_cnf_nw_fn_list and cnf_nw_fn_list with unique cnfPackageVersionFile. (Filter process)
        numpy_array = np.array(unfiltered_cnf_nw_fn_list)
        cnf_nw_fn_list = np.unique(numpy_array)


        # The below code block replaces the values in application_config.json and config.json.     
        for path in eks_level_folders:

                # Setting up the path for both files.
                application_config_path = f'{path}'+'/application_config.json'
                config_json_path = f'{path}'+'/config.json'

                # Replace condition and functionality for delete flag.
                if delete_flag == 'false':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"delete": "true"', '"delete": "false"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)
                elif delete_flag == 'true':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"delete": "false"', '"delete": "true"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)
                
                # Replace condition and functionality for redeploy flag.
                if redeploy_flag == 'false':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"redeploy": "true"', '"redeploy": "false"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)
                elif redeploy_flag == 'true':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"redeploy": "false"', '"redeploy": "true"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)

                # Replace condition and functionality for sanity_check flag.
                if sanity_check_flag == 'disabled':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"sanity_check": "enabled"', '"sanity_check": "disabled"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)
                elif sanity_check_flag == 'enabled':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"sanity_check": "disabled"', '"sanity_check": "enabled"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)
                
                # Replace condition and functionality for validation_check flag.
                if validation_check_flag == 'disabled':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"validation_check": "enabled"', '"validation_check": "disabled"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)
                elif validation_check_flag == 'enabled':
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()
                        data = data.replace('"validation_check": "disabled"', '"validation_check": "enabled"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)

                # Replace condition and functionality for chart_key value. Doesn't run if the value in input.py is not provided.
                if chart_version != None:

                    # Opens application_config.json, replaces the values in chart_key_list(will loop all values) if they are in the file with the new value. 
                    with open(application_config_path, 'r') as FileRead:
                        data = FileRead.read()

                        for app_list_iterate in chart_key_list:
                            data = data.replace(f'"chart_key": "{app_list_iterate}"', f'"chart_key": "{chart_version}"')
                    with open(application_config_path, 'w') as FileWrite:
                        FileWrite.write(data)
                
                # Replace condition and functionality for cnfPackageVersionFile value. Doesn't run if the value in input.py is not provided.
                if cnf_package_version != None:
                    # Opens config.json, replaces the values in cnf_nw_fn_list(will loop all values) if they are in the file with the new value. 
                    with open(config_json_path, 'r') as FileRead:
                        data = FileRead.read()

                        for config_list_iterate in cnf_nw_fn_list:
                            data = data.replace(f'"cnfPackageVersionFile": "{config_list_iterate}"', f'"cnfPackageVersionFile": "{cnf_package_version}"')
                    with open(config_json_path, 'w') as FileWrite:
                        FileWrite.write(data)
                
    except Exception as e:
        fatal_error(f'Exception caught while traversing through the EKS level folders and replacing values: {e}')
    print()



def mav_bedc_cu_values_yaml_files(change, drop_version, line_number, required, eks_level_folders):
    '''
    Info: This Function is used to loop through all the EKS cluster level folders, go to the drop versions and modify the values.yaml files with new line additions.
    '''
    try:

        # Functionality will only run if the value for 'required' is set to 'yes' in the yaml_change dictionary in input.py file.
        if required == "true":
            
            # Performs the functionality for the prefered EKS cluster level folder(s).
            for path in eks_level_folders:
                for eks_folders in Path(f'{path}/').iterdir():
                    
                    # Condition to find if the drop version folder is there in the EKS cluster level folder. If not, no point in continuing and skip to next EKS folder. 
                    if f'{path}\{drop_version}' == str(eks_folders):
                        for drop_path in Path(f'{path}/{drop_version}').iterdir():
                            if drop_path.is_dir():
                                # After traversing through the drop version folder, will loop through all the sub folders and update the values.yaml files.
                                values_yaml_file = f'{drop_path}/values.yaml'

                                # Opens the values.yaml file and insert the line of code into the prefered line number.
                                with open(values_yaml_file, 'r') as FileRead:
                                    yaml_data = FileRead.readlines()
                                    yaml_data.insert(line_number - 1, change)    
                                with open(values_yaml_file, 'w') as FileWrite:
                                    FileWrite.writelines(yaml_data)
        
    except Exception as e:
        fatal_error(f'Exception caught while looping and modifying the values.yaml files with new line additions: {e}')
    print()


def fatal_error(message):
    print('\033[31mERROR: ' + message + '\033[0m')
    exit  
