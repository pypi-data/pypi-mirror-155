#######################################################################################################################################################
#  Description: This Python script is used to define the mav_bedc_mgmt_module module that make changes to the 
#               delete flag, redeploy flag, validation floag, change cnfNetworkFunction value, helm chart key on a mass scale 
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




def mav_bedc_mgmt_module(release_name, delete_flag, redeploy_flag, validation_check_flag, chart_version, cnf_package_version, eks_level_folders):
    '''
    Info: This Function is used to loop through all the EKS cluster level folders, parse the current values of delete flag, redeploy flag, validation flag, updates the new cnfPackageVersion and chart key value.
    '''
    try:

        # The below code block replaces the values in application_config.json and config.json.     
        for path in eks_level_folders:

                # Setting up the path for both files.
                application_config_path = f'{path}'+'/application_config.json'
                config_json_path = f'{path}'+'/config.json'

                # Opens application_config.json, grep the value of chart_key and put it in the unfiltered_chart_key_list list.
                with open(application_config_path, 'r') as applicatipon_json_FileRead:
                    app_data = json.load(applicatipon_json_FileRead) 
                
                # Opens config.json, grep the value of cnfPackageVersionFile and put it in the unfiltered_cnf_nw_fn_list list.
                with open(config_json_path, 'r') as config_jsonFileRead:
                    config_data = json.load(config_jsonFileRead) 

                # setting up an integer with the total number of release in the application_config.json
                chart_counter = (str((app_data['profiles']['mav_bedc']['charts'])).count('release_name'))
                # Setting up an index value so that the correct release index is accessed.
                for chart_iteration in range(0, chart_counter):
                    release_value_json = (app_data['profiles']['mav_bedc']['charts'][chart_iteration]['release_name'])
                    if release_name == f'"{release_value_json}"':
                        index_value = chart_iteration
 
                # Replace condition and functionality for delete flag.
                if delete_flag == 'false':
                    if 'delete' in app_data['profiles']['mav_bedc']['charts'][index_value]:
                        app_data['profiles']['mav_bedc']['charts'][index_value]['delete'] = "false"
                        with open(application_config_path, 'w') as FileWrite:
                            json.dump(app_data, FileWrite, indent=2)
                elif delete_flag == 'true':
                    if 'delete' in app_data['profiles']['mav_bedc']['charts'][index_value]:
                        app_data['profiles']['mav_bedc']['charts'][index_value]['delete'] = "true"
                        with open(application_config_path, 'w') as FileWrite:
                            json.dump(app_data, FileWrite, indent=2)        

                # Replace condition and functionality for redeploy flag.
                if redeploy_flag == 'false':
                    if 'redeploy' in app_data['profiles']['mav_bedc']['charts'][index_value]:
                        app_data['profiles']['mav_bedc']['charts'][index_value]['redeploy'] = "false"
                        with open(application_config_path, 'w') as FileWrite:
                            json.dump(app_data, FileWrite, indent=2)
                elif redeploy_flag == 'true':
                    if 'redeploy' in app_data['profiles']['mav_bedc']['charts'][index_value]:
                        app_data['profiles']['mav_bedc']['charts'][index_value]['redeploy'] = "true"
                        with open(application_config_path, 'w') as FileWrite:
                            json.dump(app_data, FileWrite, indent=2)     

                # Replace condition and functionality for validation_check flag.
                if validation_check_flag == 'disabled':
                    if 'validation_check' in app_data['profiles']['mav_bedc']['charts'][index_value]:
                        app_data['profiles']['mav_bedc']['charts'][index_value]['validation_check'] = "disabled"
                        with open(application_config_path, 'w') as FileWrite:
                            json.dump(app_data, FileWrite, indent=2)
                elif validation_check_flag == 'enabled':
                    if 'validation_check' in app_data['profiles']['mav_bedc']['charts'][index_value]:
                        app_data['profiles']['mav_bedc']['charts'][index_value]['validation_check'] = "enabled"
                        with open(application_config_path, 'w') as FileWrite:
                            json.dump(app_data, FileWrite, indent=2)  

                # Condition to validate whether chart_key value needs to be replaced.
                if chart_version != None:
                    # Replace condition and functionality for chart_key value.
                    app_data['profiles']['mav_bedc']['charts'][index_value]['chart_key'] = chart_version
                    with open(application_config_path, 'w') as FileWrite:
                        json.dump(app_data, FileWrite, indent=2)  

                # Condition to validate whether cnf_package_version value needs to be replaced.
                if cnf_package_version != None:
                    # Replace condition and functionality for chart_key value.
                    config_data['cnfPackageVersionFile'] = cnf_package_version
                    with open(config_json_path, 'w') as FileWrite:
                        json.dump(config_data, FileWrite, indent=2) 
            
    except Exception as e:
        fatal_error(f'Exception caught while traversing through the EKS level folders and replacing values: {e}')
    print()




def mav_bedc_mgmt_values_yaml_files(change, drop_version, line_number, required, eks_level_folders, nf_type):
    '''
    Info: This Function is used to loop through all the EKS cluster level folders, go to the drop versions and modify the values.yaml files with new line additions.
    '''
    try:

        # Functionality will only run if the value for 'required' is set to 'yes' in the yaml_change dictionary in input.py file.
        if required == "true":
            
            # Performs the functionality for the prefered EKS cluster level folder(s).
            for path in eks_level_folders:
                for eks_folders in Path(f'{path}/gv').iterdir():
                    
                    # Condition to find if the drop version folder is there in the EKS cluster level folder. If not, no point in continuing and skip to next EKS folder. 
                    if f'{path}\gv\{drop_version}' == str(eks_folders):

                        # After traversing through the drop version folder, will loop through all the sub folders and update the values.yaml files.
                        values_yaml_file = f'{path}\gv\{drop_version}\{nf_type}/values.yaml'
                        
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
