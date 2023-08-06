#!/usr/bin/env python3
import json

import boto3
import time
import sys
import argparse
import uuid
import os
from os import environ
import glob
from .enumeration import loadbalancer as loadbalancer
from .enumeration import rand_id_generator as rand_id_generator
from .enumeration import s3aclenum as s3aclenum
from .enumeration import ecrprivenum
from .enumeration import ecrpubenum
from .enumeration import snsenum
from . import settings
from botocore.config import Config
from pathlib import Path

config = Config(
    retries=dict(
        max_attempts=7
    )
)

# Define ANSI escape sequence colors
environ["PYTHONIOENCODING"] = "UTF-8"
orange = "\033[3;33m"
green = "\033[0;32m"
red = "\033[9=0;31m"
nocolor = "\033[0m"

# Create timestamp in preferred format for wordlist files
timestamp = time.strftime("%Y%m%d-%H%M%S")


# Requests user to provide required info to kick off scan
def words_type(input_args):
    # print(("\033[0;31m" + 'What type of scan do you want to attempt? ' + "\033[0m"))
    # print('1. accounts')
    # print('2. root account')
    # print('3. account footprint')
    # print('4. roles')
    # print('5. users')
    # print()
    # wordlist_type = input('Scan Type: ').lower()
    # print('')
    while True:
        print("In words_type Function")
        print(input_args.scan_type)

        if str(input_args.scan_type) == '1':
            return 'accounts', 'none'
        elif str(input_args.scan_type) == '2':
            return 'root account', 'none'
        elif str(input_args.scan_type) == 'roles':
            # account_no = input('Provide an Account ID to scan against: ')
            print('')
            return 'roles', str(input_args.account_no)
        elif str(input_args.scan_type) == '3':
            # account_no = input('Provide an Account ID to scan against: ')
            print('')
            return 'footprint', str(input_args.account_no)
        elif str(input_args.scan_type) == '4':
            # account_no = input('Provide an Account ID to scan against: ')
            print('')
            return 'roles', str(input_args.account_no)
        elif str(input_args.scan_type) == '5':
            # account_no = input('Provide an Account ID to scan against: ')
            print('')
            return 'users', str(input_args.account_no)
        # else:
        #     print('You did not enter a valid wordlist type.')
        #     print('')
        #     wordlist_type = input("\033[0;31m" + 'Enter a number between 1-5 ' + "\033[0m").lower()


# Creates final wordlist based on type of scanning to be performed.
def words(input_args):
    wordlist_type ,account_no = words_type(input_args)
    wordlist_path = 'wordlist-' + wordlist_type + '-' + timestamp + '.txt'
    wordlist = os.path.join(os.getcwd(), wordlist_path)
    print(wordlist)
    new_list = []
    while True:
        try:
            if wordlist_type == 'accounts':
                response = rand_id_generator.rand_id_generator(list_size= input_args.word_list)
                wordlist_file = response
            elif wordlist_type == 'footprint':
                wordlist_file = os.path.dirname(__file__) + '/wordlists/service-linked-roles.txt'
            else:
                wordlist_file = input_args.word_list_path
            print('')
            with open(wordlist_file) as file:
                my_list = [x.rstrip() for x in file]
                file.close()
                if wordlist_type == 'roles':
                    for item in my_list:
                        new_list.append('arn:aws:iam::' + account_no + ':role/' + item)
                    with open(wordlist, 'a+') as f:
                        for item in new_list:
                            f.write("%s\n" % item)
                    # Configure user-defined wordlist as roles for triggering via enumeration.loadbalancer.threader(getter())
                    results_file = loadbalancer.threader(loadbalancer.getter(thread =input_args.thread,wordlist=wordlist))
                    # print(results_file)
                    return results_file
                    break
                elif wordlist_type == 'footprint':
                    for item in my_list:
                        new_list.append('arn:aws:iam::' + account_no + ':role/' + item)
                    with open(wordlist, 'a+') as f:
                        for item in new_list:
                            f.write("%s\n" % item)
                    # Configure user-defined wordlist as roles for triggering via enumeration.loadbalancer.threader(getter())
                    results_file = loadbalancer.threader(loadbalancer.getter(thread =input_args.thread,wordlist=wordlist))
                    return results_file
                    break
                elif wordlist_type == 'users':
                    for item in my_list:
                        new_list.append('arn:aws:iam::' + account_no + ':user/' + item)
                    with open(wordlist, 'a+') as f:
                        for item in new_list:
                            f.write("%s\n" % item)
                    # Configure user-defined wordlist as users for triggering via enumeration.loadbalancer.threader(getter())
                    results_file = loadbalancer.threader(loadbalancer.getter(thread =input_args.thread,wordlist=wordlist))
                    return results_file
                    break
                # TODO: Separate root accounts and setup s3 ACL check for root e-mail. Determine if root e-mail is only enumerable using s3 ACL
                elif wordlist_type == 'accounts':
                    for item in my_list:
                        new_list.append(item)
                    with open(wordlist, 'a+') as f:
                        for item in new_list:
                            f.write("%s\n" % item)

                    # Configure user-defined wordlist as account IDs or root account e-mails for triggering via enumeration.loadbalancer.threader(getter())
                    results_file = loadbalancer.threader(loadbalancer.getter(thread =input_args.thread,wordlist=wordlist))
                    return results_file
                    break
                elif wordlist_type == 'root account':
                    valid_emails = []
                    print('Indentified Root Account E-mail Addresses:')
                    for i in my_list:
                        if s3aclenum.s3_acl_princ_checker(i) == 'Pass':
                            print(i)
                            valid_emails.append(i)
                        else:
                            pass
                    with open(os.path.dirname(__file__) + 'results/valid_scan_results.txt', 'a+') as f:
                        for i in valid_emails:
                            f.write("%s\n" % i)
                    break
                else:
                    print('Scan type provided is not valid.')
                    wordlist_type = input(
                        "\033[0;31m" + 'Wordlist is intended to be accounts, roles, users, groups, or root account? ' + "\033[0m").lower()

        except OSError as e:
            print('')
            print('Provided filename does not appear to exist.')
            print('Provided filename does not appear to exist.')
            print(e)
            continue

# def scan_inst():

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scan_type', type=int, default=1,
                        help="What type of scan do you want to attempt? Enter the type of scan for example 1.accounts,2.root account,3.account footprint,4.roles,5.users")

    parser.add_argument('--account_no', type=int, default=3.0,
                        help="Enter account number.")


    parser.add_argument('--thread', type=int, default=10,
                        help="This is number of thread ")

    parser.add_argument('--word_list', type=int, default=10,
                        help="How large of a list should we create?")

    parser.add_argument('--word_list_path', type=str, default="",
                        help="Path to the world list file which will be required for scan")

    parser.add_argument('--s3_bucket_name', type=str, default="",
                        help="Name of S3 bucket which will be later used for storing the scan results.")

    parser.add_argument('--profile_arn', type=str, default="",
                        help="Arn of aws profile for e.g arn:aws:iam::account_id:user/user.name or you can get these details by runing (aws sts get-caller-identity) this command in cli")

    input_args = parser.parse_args()

    print("Input arguments : " + str(input_args))





    # Deploy infrastructure for scanning
    print(green + f"""
    ________        .__        __    __________.__        __   
    \_____  \  __ __|__| _____/  |_  \______   \__| _____/  |_ 
     /  / \  \|  |  \  |/ __ \   __\  |       _/  |/  _ \   __/
    /   \_/.  \  |  /  \  ___/|  |    |    |   \  (  <_> )  |  
    \_____\ \_/____/|__|\___  >__|    |____|_  /__|\____/|__|  
           \__>             \/               \/                
    """ + nocolor)

    sts = boto3.client('sts')
    # Create clients required for Quiet Riot Enumeration Infrastructure
    iam = boto3.client('iam', config=config)
    s3 = boto3.client('s3', config=config)
    sns = boto3.client('sns', config=config)
    ecrprivate = boto3.client('ecr', config=config)
    ecrpublic = boto3.client('ecr-public', config=config)

    if str(input_args.s3_bucket_name) != "":

        buckets = s3.list_buckets()
        bucket_flag = 0

        for i in range(0, len(buckets['Buckets'])):
            if str(input_args.s3_bucket_name) in buckets['Buckets'][i]['Name']:
                bucket_flag = 1
                print("S3 bucket is already there with this name: " + input_args.s3_bucket_name)
                break
            else:
                bucket_flag = 0
                pass

        if bucket_flag == 0:

            print("Creating S3 bucket for uploading results: " + input_args.s3_bucket_name)
            s3_bucket = f'{str(input_args.s3_bucket_name)}'
            s3.create_bucket(
                Bucket=s3_bucket
            )
            time.sleep(4)
            response = s3.put_bucket_policy(
                Bucket=f'{str(input_args.s3_bucket_name)}',
                Policy=json.dumps({"Version":"2012-10-17",
                        "Statement":[
                            {
                                "Sid":"QuietRiot",
                                "Effect":"Allow",
                                "Principal":{
                                    "AWS": f'{str(input_args.profile_arn)}'
                                },
                                "Action":"*",
                                "Resource": [
                                    f'arn:aws:s3:::{str(input_args.s3_bucket_name)}/*' # Needs to be updated to be more generalized
                                ]
                            }
                        ]}))




    # Create s3 bucket to scan against for root account e-mail addresses.


    # global_bucket = 's3://quiet-riot-global-bucket/'

    # initialize
    #############################################################################
    ##                                                                         ##
    ##           Deployment of Enumeration Infra based on user preference      ##
    ##                                                                         ##
    #############################################################################

    # Create ECR Public Repository - Resource that has IAM policy attachment
    ecr_public_repo = f'quiet-riot-public-repo-{uuid.uuid4().hex}'
    ecrpublic.create_repository(
        repositoryName=ecr_public_repo
    )
    # Create ECR Private Repository - Resource that has IAM policy attachment
    ecr_private_repo = f'quiet-riot-private-repo-{uuid.uuid4().hex}'
    ecrprivate.create_repository(
        repositoryName=ecr_private_repo
    )
    # Create SNS Topic - Resource that has IAM policy attachment
    sns_topic = f'quiet-riot-sns-topic-{uuid.uuid4().hex}'
    sns.create_topic(
        Name=sns_topic
    )
    # Create s3 bucket to scan against for root account e-mail addresses.
    s3_bucket = f'quiet-riot-bucket-{uuid.uuid4().hex}'
    s3.create_bucket(
        Bucket=s3_bucket
    )

    canonical_id = s3.list_buckets()['Owner']['ID']
    # Generate list from created resource names
    settings.init()
    settings.scan_objects.append(ecr_public_repo)
    settings.scan_objects.append(ecr_private_repo)
    settings.scan_objects.append("arn:aws:sns:us-east-1:" + settings.account_no + ":" + sns_topic)
    settings.scan_objects.append(s3_bucket)
    settings.scan_objects.append(canonical_id)
    # print("Calling the words function-------")
    # Call initial workflow that takes a user wordlist and starts a scan.
    results_file = words(input_args)
    # print(results_file)

    if str(input_args.s3_bucket_name) != "":
        try:
            result_file_path = os.path.join(os.getcwd(), results_file)
            s3.put_object(
                Body=open(f'{result_file_path}', 'rb'),
                Bucket=f'{input_args.s3_bucket_name}',
                Key=f'{results_file}'
            )
        except Exception as result_exc:
            print(result_exc)
            print("There is some error in uploading file to S3 bucket")


        try:
            results_file1 = glob.glob("valid_scan_results-*")
            for filePath_results in results_file1:
                try:
                    # print(filePath)
                    results_file_path = os.path.join(os.getcwd(), filePath_results)
                    # print(results_file_path)
                    os.remove(results_file_path)
                except Exception as result_file_exc:
                    print(result_file_exc)
                    print("Error while deleting  file")


        except Exception as result_file_exc:
            print(result_file_exc)

    # Request whether user is finished with infrastructure

    while True:
        print('')
        time.sleep(1)
        prompt1 = 'yes'  # TODO: figure out why it can't take "no" - the threads never finish a second time through...think I need to clear the threads... #input('Finished Scanning? Answer "yes" to delete your infrastructure: ').lower()
        time.sleep(1)
        # If user is finished with infrastructure, delete the created infrastructure
        if prompt1 == 'yes':
            buckets = s3.list_buckets()
            # print(buckets)
            for i in range(0, len(buckets['Buckets'])):
                if len(buckets['Buckets']) != 0:
                    if 'quiet-riot-bucket' in buckets['Buckets'][i]['Name']:
                        print("Deleting Quiet Riot Infrastructure: " + buckets['Buckets'][i]['Name'])
                        s3.delete_bucket(Bucket=buckets['Buckets'][i]['Name'])
                    else:
                        pass
            # Delete ECR Public Repository - Resource that has IAM policy attachment
            public_repos = ecrpublic.describe_repositories()
            for i in range(0, len(public_repos['repositories'])):
                if len(public_repos['repositories']) != 0:
                    if 'quiet-riot-public-repo' in public_repos['repositories'][i]['repositoryName']:
                        print(
                            "Deleting Quiet Riot Infrastructure: " + public_repos['repositories'][i]['repositoryName'])
                        ecrpublic.delete_repository(repositoryName=public_repos['repositories'][i]['repositoryName'])
                    else:
                        pass
            # Delete ECR Private Repository - Resource that has IAM policy attachment
            private_repos = ecrprivate.describe_repositories()
            for i in range(0, len(private_repos['repositories'])):
                if len(private_repos['repositories']) != 0:
                    if 'quiet-riot-private-repo' in private_repos['repositories'][i]['repositoryName']:
                        print(
                            "Deleting Quiet Riot Infrastructure: " + private_repos['repositories'][i]['repositoryName'])
                        ecrprivate.delete_repository(repositoryName=private_repos['repositories'][i]['repositoryName'])
                    else:
                        pass
            # Delete SNS Topic - Resource that has IAM policy attachment
            sns_topics = sns.list_topics()
            for i in range(0, len(sns_topics['Topics'])):
                if len(sns_topics['Topics']) != 0:
                    if 'quiet-riot-sns-topic' in sns_topics['Topics'][i]['TopicArn']:
                        print("Deleting Quiet Riot Infrastructure: " + sns_topics['Topics'][i]['TopicArn'])
                        sns.delete_topic(TopicArn=sns_topics['Topics'][i]['TopicArn'])
                    else:
                        pass
                else:
                    print("There are no topics to delete.")
            print('')
            # Ask user if they want valid principals file downloaded
            print('')
            # TODO: Create control flow logic to ask user if willing to upload valid principals to global quiet-riot bucket maintained by Righteous Gambit Research
            try:
                fileList = glob.glob("wordlist-**")
                for filePath in fileList:
                    try:
                        # print(filePath)
                        wordlist_file_path = os.path.join(os.getcwd(), filePath)
                        # print(wordlist_file_path)
                        os.remove(wordlist_file_path)
                    except Exception as text_file:
                        print(text_file)
                        print("Error while deleting wordlist file: ", wordlist_file_path)

            except Exception as wordlist_file_exc:
                print(wordlist_file_exc)

            sys.exit()
        elif prompt1 == 'no':
            print('')
            print(
                "\033[0;32m" + f'If you have uploaded a wordlist, you can review your validated principals @ valid_principals.txt in your local directory.' + "\033[0m")
            print('')
            keep_going = input('Configure another wordlist? ').lower()
            print('')
            if keep_going == 'yes':
                words()
            elif keep_going == 'no':
                pass
            else:
                print('Provided response is not valid. Response must be "yes" or "no".')
                print('')
                keep_going = input('Configure another wordlist? ').lower()
        else:
            print('')
            print('Provided response is not valid. Response must be "yes" or "no".')
