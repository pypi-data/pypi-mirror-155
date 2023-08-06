#######################################################################################################################################################
#  Description: This Python script is used to define the Pipeline Increment module that help to increment the PIPELINE_ID value in 
#               bulk_pipeline_trigger.json file.
#               
#  Author: Arjun Babu (arbnair97@gmail.com)
#  Created date: 03/06/2022
#  Python compatible version: 3.10.4
#  
#  Modifications:
#  1. 
#
#######################################################################################################################################################

from itertools import *
import json
from pathlib import Path




def increment_pipeline_version(eks_level_folders):
    '''
    Info: This Function is used to loop through all the EKS cluster level folders, parse the current 'PIPELINE_TRIGGER_ID' from the 'bulk-pipeline-trigger.json', append one digit and write back. Thus making a new change.
    '''
    try:

        # Will update the bulk-pipeline-trigger.json in the EKS cluster folders.
        for path in eks_level_folders:

                path_dir = f'{path}'+'/bulk-pipeline-trigger.json'

                # Will increment the current value for 'PIPELINE_TRIGGER_ID'.
                with open(path_dir, 'r') as FileRead:
                    data_dict_read = json.load(FileRead)
                    pipeline_version = data_dict_read["PIPELINE_TRIGGER_ID"]
                    pipeline_version = float(pipeline_version)
                    pipeline_version = pipeline_version + 1

                with open(path_dir, 'w') as FileWrite:
                    FileWrite.write('{ "PIPELINE_TRIGGER_ID":'+str(pipeline_version)+' }')
        
    except Exception as e:
        fatal_error(f'Exception caught while looping and appending *PIPELINE_TRIGGER_ID* in bulk-pipeline-trigger.json: {e}')
    print()


def fatal_error(message):
    print('\033[31mERROR: ' + message + '\033[0m')
    exit  

