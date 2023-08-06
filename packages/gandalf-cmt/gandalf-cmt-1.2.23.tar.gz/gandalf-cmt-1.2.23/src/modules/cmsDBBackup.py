#######################################################################################################################################################
#  Description: This Python script is used to take automatic backup of mCMS SQL dump file, yang files and application.properties
#               
#  Author: Arjun Babu (arjun.babu@ust.com)
#  Created date: 0906/2022
#
#  Python compatible version: 3.10.4
#  
#  Modifications:
#  1. 
#
#######################################################################################################################################################


import os
import datetime
import subprocess



def mav_ndc_cms_backup(cms_namespace, release_name, path):
    '''
    Info: This Function is used to parse the mCMS namespace and apply within the Python operation.
    '''
    try:
        
        # To calculate current time of execution for creating timestamp
        current_time = str(datetime.datetime.now())
        current_time = str(current_time[0:19])
        current_time = current_time.replace(" ", "-")

        # To parse mCMS pod namespace that's being passed from installApp.sh


        if release_name == "cms1":
            # Creates a temporary dump folder for CMS1 in order to store the DB dump files
            subprocess.run(f'mkdir {path}/cms1_dump_files', shell=True)
        elif release_name == "cms2":
            # Creates a temporary dump folder for CMS2 in order to store the DB dump files
            subprocess.run(f'mkdir {path}/cms2_dump_files', shell=True)


        # Invoking other functions in the Python script
        cms_db_backup_zipping(cms_namespace, release_name)
        cms_db_backup_copy(cms_namespace, current_time, release_name)
        cms_db_backup_s3_upload(cms_namespace, current_time, release_name)
        cleanup(cms_namespace, release_name)

    except Exception as e:
        fatal_error(f'Exception caught while Parsing the mCMS namespace: {e}')
    print()


def cms_db_backup_zipping(cms_namespace, release_name):
    '''
    Info: This Function is used to log into the mCMS K8s pod, create the DB dump SQL file, Tar the .yang file and keep them within the mCMS K8s container.
    '''
    try:
        # Creates a shell script and inputs the command that's used to generate the mCMS DB dump file.
        subprocess.run(f'touch db_dump_shell_1.sh', shell=True)
        subprocess.run(f'chmod +x db_dump_shell_1.sh', shell=True)
        with open('db_dump_shell_1.sh', 'w') as FileWrite:
            FileWrite.write('''#!/bin/bash
            mysqldump -udbadmin -pPh03nix5parr0w! --add-drop-database --routines --databases cms > '''+release_name+'''dump.sql;
            ''')
        # Copies the shell script to the mCMS pod and executes it inside the pod.
        subprocess.run(f'kubectl cp db_dump_shell_1.sh -n {cms_namespace} {release_name}-0:/root/', shell=True)
        subprocess.run(f'kubectl exec -it -n {cms_namespace} {release_name}-0 /root/db_dump_shell_1.sh', shell=True)

        # Creates a second shell script and inputs the command that's used tar the .yang files from /data/redun/yang
        subprocess.run(f'touch db_dump_shell_2.sh', shell=True)
        subprocess.run(f'chmod +x db_dump_shell_2.sh', shell=True)
        with open('db_dump_shell_2.sh', 'w') as FileWrite:
            FileWrite.write('''#!/bin/bash
            tar -cvf /root/yang.tgz /data/redun/yang
            ''')
        # Copies the second shell script to the mCMS pod and executes it inside the pod.
        subprocess.run(f'kubectl cp db_dump_shell_2.sh -n {cms_namespace} {release_name}-0:/root/', shell=True)
        subprocess.run(f'kubectl exec -it -n {cms_namespace} {release_name}-0 /root/db_dump_shell_2.sh', shell=True)

    except Exception as e:
        fatal_error(f'Exception caught while creating the DB dump SQL file and Taring/zipping the .yang file in the {release_name} K8s pod: {e}')
    print()


def cms_db_backup_copy(cms_namespace, current_time, release_name):
    '''
    Info: This Function is used to copy the created DB dump SQL file, zipped .yang files and the application.properties file from the mCMS K8s pod to the CodePipeline runner.
    '''
    try:
        # Variable to generate the DB dump file with timestamp.
        db_dump_file_name = cms_namespace+release_name+'db_dump'+current_time+'.sql'

        # Copies the mCMS DB dump file from the pod to the CodePipeline runner.
        subprocess.run(f'kubectl cp -n {cms_namespace} {release_name}-0:/root/{release_name}dump.sql {release_name}_dump_files/{release_name}dump.sql', shell=True)
        os.rename(f'{release_name}_dump_files/{release_name}dump.sql', release_name+'_dump_files/'+db_dump_file_name)

        # Copies the tarred/zipped .yang files from the pod to the CodePipeline runner.
        subprocess.run(f'kubectl cp -n {cms_namespace} {release_name}-0:/root/yang.tgz {release_name}_dump_files/yang.tgz', shell=True)

        # Copies the application.properties file from the pod (/opt/dist/WebController/conf/) to the CodePipeline runner.
        subprocess.run(f'kubectl cp -n {cms_namespace} {release_name}-0:/opt/dist/WebController/conf/application.properties {release_name}_dump_files/application.properties', shell=True)

    except Exception as e:
        fatal_error(f'Exception caught while copying the created DB dump SQL file, zipped .yang files and the application.properties file from the {release_name} K8s pod: {e}')
    print()

def cms_db_backup_s3_upload(cms_namespace, current_time, release_name):
    '''
    Info: This Function is used to upload the DB files over to the `mtcil-prod` AWS S3 Bucket in the NDC Account.
    '''
    try:
        # Uploads all the files retrieved from the mCMS pod to the AWS S3 bucket 'mtcil-prod' in the AWS NDC Account.
        #subprocess.run(f'aws s3 cp dump_files/ s3://mv-releases-prod-us-west-2-01/releases/nmgt/{release_name}-backups/{cms_namespace}/{current_time}/ --recursive', shell=True)
        subprocess.run(f'aws s3 cp {release_name}_dump_files/ s3://mtcil-prod/mCMS-DB-Backup/{release_name}-backups/{cms_namespace}/{current_time}/ --recursive', shell=True)

    except Exception as e:
        fatal_error(f'Exception caught while uploading the DB files to the AWS S3 Bucket: {e}')
    print()


def cleanup(cms_namespace, release_name):
    '''
    Info: This Function is used to clean-up all the unwanted files from the mCMS K8s pod as well as the CodePipeline runner.
    '''
    try:
        # Cleans up all the unwanted files from the mCMS K8s pod as well as the CodePipeline runner
        subprocess.run(f'rm db_dump_shell_1.sh', shell=True)
        subprocess.run(f'rm db_dump_shell_2.sh', shell=True)
        subprocess.run(f"kubectl exec -n {cms_namespace} {release_name}-0 -- sh -c 'rm -rf /root/{release_name}dump.sql'", shell=True)
        subprocess.run(f"kubectl exec -n {cms_namespace} {release_name}-0 -- sh -c 'rm -rf /root/yang.tgz'", shell=True)
        subprocess.run(f"kubectl exec -n {cms_namespace} {release_name}-0 -- sh -c 'rm -rf /root/application.properties'", shell=True)
        subprocess.run(f"kubectl exec -n {cms_namespace} {release_name}-0 -- sh -c 'rm -rf /root/db_dump_shell_1.sh'", shell=True)
        subprocess.run(f"kubectl exec -n {cms_namespace} {release_name}-0 -- sh -c 'rm -rf /root/db_dump_shell_2.sh'", shell=True)
    except Exception as e:
        fatal_error(f'Exception caught while performing file clean-up: {e}')
    print()


def fatal_error(message):
    print('\033[31mERROR: ' + message + '\033[0m')
    exit 


