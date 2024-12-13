#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baraag DL v0.02 -  A simple Baraag media downloader
"""

import argparse
from mastodon import Mastodon
from mastodon.Mastodon import MastodonError, MastodonMalformedEventError, MastodonNetworkError, MastodonReadTimeout, MastodonAPIError, MastodonUnauthorizedError

import sys
import os
import requests
import logging
import subprocess

from datetime import datetime

from colorama import Fore, Style, Back, init

from getpass import getpass

# Initializing colorama for Windows

if os.name != "posix":
    init(convert=True)

# Global variables

baraag_dl_version = "v0.02"
client_name = "baraag_dl"+baraag_dl_version

# Initial empty client

client = None

# Initializing logger

timestamp = datetime.now().strftime("%Y%m%d%H%M")
logfile = "baraag_dl_error_"+timestamp+".log"

logging.basicConfig(level = logging.INFO,
                    handlers=[logging.FileHandler(logfile, delay=True)])

# Core functions

def create_client():
    '''
    Utilizes create_app() from Mastodon.py to register the current script and
    obtain access credentials.
    
    It takes no arguments and returns nothing.
    
    Credentials are written to a file, "client_credentials" in the root folder 
    of the script.
    '''
    Mastodon.create_app(client_name,
                        api_base_url = 'https://baraag.net',
                        to_file = 'client_credentials')

def init_client(client_credentials = "client_credentials", user_credentials = None):
    '''
    Initializes a local Mastodon client using Mastodon.py, and utilizes the 
    credentials created by create_client() to interface with the Mastodon API. 
    Utilizes the 'pace' rate limiter to prevent the API from rejecting
    requests.

    It takes 2 arguments:
        
    client_credentials = str, file path of the file containing the
                        client credentials, generated by create_client()
                        Defaults to "client_credentials" (root folder of the 
                                                          script).
                       REQUIRED
                       
    user_credentials = str, file path of the file containing the
                       user credentials, generated by user_login()
                       Defaults to None.
                        
                       OPTIONAL
    
    In the absence of user_credentials, the client will initialize without
    authenticating an user, which will need to be done manually by user_login()

    Returns: a Mastodon object client

    ''' 
    if user_credentials == None:
        client = Mastodon(client_id = client_credentials,
                        api_base_url = 'https://baraag.net',
                        ratelimit_method='pace'
                        )
    else:
        client = Mastodon(client_id = client_credentials,
                        api_base_url = 'https://baraag.net',
                        ratelimit_method='pace',
                        access_token = user_credentials
                        )

    return client

def request_login():
    """
    A simple function to request login information from the user.
    
    Takes no arguments.
    
    Returns a pair of strings: user, password
    
    """
    user = input("Login (e-mail): ")
    password = getpass("Password (will not be echoed): ")
    
    return user, password

def user_login(client, user, password):
    """
    Logs in the user after initialization if there are no valid credentials.

    Takes 3 arguments: 
    
    client = Mastodon object client, generated by init_client().
             REQUIRED
    
    user = username (str), generated by request_login().
           REQUIRED
           
    password = password (str), generated by request_login().
              REQUIRED

    Returns nothing, but generates a file named user_credentials containing
    an authentication token that can be used by init_client().
    
    Please see initialize() to see how the authentication flow works currently.   
    """
    client.log_in(username = user,
                    password = password,
                    to_file = "user_credentials")

def mastodon_error_handler(exc):
    """
    Handles generic MastodonError type errors.
    Saves exception traceback to log, exits program.

    Takes 1 argument:
        
    exc = Exception caught during runtime.
          REQUIRED
          
    Returns nothing. Exits program.

    """
    logging.exception(str(exc))
    print()
    print(Fore.RED+"Baraag DL was unable to connect to the API. Please check error logs."+Fore.RESET)
    print()
    print("Exiting...")
    sys.exit()
    
def mastodon_network_error_handler(exc):
    """
    Handles network-related MastodonError type errors.
    Saves exception traceback to log, exits program.

    Takes 1 argument:
        
    exc = Exception caught during runtime.
          REQUIRED
          
    Returns nothing. Exits program.

    """
    logging.exception(str(exc))
    print()
    print(Fore.RED+"Baraag network error! Please check internet connection and/or try"\
          " again later."+Fore.RESET)
    print()
    print("Exiting...")
    sys.exit()

def cold_init():
    """
    Cold client initialization loop used to reinitialize and return a client
    when credentials either do not exist or have become invalid.

    It takes no arguments.

    Returns: a Mastodon object client

    """
    print("Registering Baraag client...")
    try: 
        create_client()
        client = init_client("client_credentials")
        print()
        print(Fore.GREEN+"Client registered."+Fore.RESET)
        print()
        print("Requesting user information...")
        print()
        user, password = request_login()
        print()   
        
    except MastodonNetworkError as exc:
        mastodon_network_error_handler(exc)
        
    except MastodonError as exc:
        mastodon_error_handler(exc)     

    try:
        user_login(client, user, password)
        print(Fore.GREEN+"Login successful!"+Fore.RESET)
        return client
    except Exception as exc:
        logging.exception(str(exc))
        print()
        print(Fore.RED+"Unable to login with details provided!"+Fore.RESET)
        print()
        print("Exiting...")
        sys.exit()

def initialize():
    """
    Creates an initialization loop that prepares the local client with the
    required credentials.
    
    It utilizes init_client(), request_login(), user_login() and cold_init()
    to generate and read credentials.
    
    It takes no arguments.

    Returns: a Mastodon object client

    """
    print("Initializing client...")
    print()
    try:
        if os.path.isfile("client_credentials") and os.path.isfile("user_credentials"):
            client_credentials = "client_credentials"
            user_credentials = "user_credentials"
            print("Client and user credentials found. Attempting authentication...")
            print()
            try:
                client = init_client(client_credentials, user_credentials)
                client.me()
                print(Fore.GREEN+"Authentication successful!"+Fore.RESET)
                return client
            
            except MastodonUnauthorizedError as exc:
                #logging.exception(str(exc))
                print(Fore.RED+"Credentials invalid!"+Fore.RESET)
                print()
                print("Reinitializing...")
                print()
                client = cold_init()
                return client
            
            except MastodonNetworkError as exc:
                mastodon_network_error_handler(exc)
                
            except MastodonError as exc:
                mastodon_error_handler(exc)
            
            except Exception as exc:
                #logging.exception(str(exc))
                print(Fore.RED+"Credentials invalid!"+Fore.RESET)
                print()
                print("Reinitializing...")
                print()
                client = cold_init()
                return client
                
        elif os.path.isfile("client_credentials"):
            client_credentials = "client_credentials"
            print("Client credentials found. Attempting authentication...")
            print()
            client = init_client(client_credentials)
            user, password = request_login()
            
            try:
                user_login(client, user, password)
                print()
                print(Fore.GREEN+"Login successful!"+Fore.RESET)
                return client
            
            except MastodonNetworkError as exc:
                mastodon_network_error_handler(exc)
                
            except MastodonError as exc:
                mastodon_error_handler(exc)
                   
            except Exception as exc:
                #logging.exception(str(exc))
                print(Fore.RED+"Unable to login with credentials provided!"+Fore.RESET)
                print()
                print("Attempting client reinitialization...")
                print()
                client = cold_init()
                return client
                
        else:
            print(Fore.RED+"Credentials not found!"+Fore.RESET)
            print()
            print("Reinitializing...")
            print()
            client = cold_init()
            return client
    
    except KeyboardInterrupt:
        print()
        print(Fore.YELLOW+"Interrupted by user. Exiting..."+Fore.RESET)
        sys.exit()
        
def get_following(user_id):
    """
    Returns a list of dictionaries containing all users a user with the
    provided ID follows.
    
    Unlike most functions, this queries the API directly instead of going
    through the client generated and managed by Mastodon.py.

    It takes 1 argument: 
        
    user_id = user ID on Baraag (int); mainly derived from logged in user,
              but may be obtained from search_user().
              REQUIRED

    Returns: a list of dictionaries.

    """
    url = "https://baraag.net/api/v1/accounts/"+str(user_id)+"/following"
    
    follow_list = []
    
    try:
        req_response = requests.get(url)
    except Exception as exc:
        logging.exception(str(exc))
        print()
        print(Fore.RED+"HTTP request failed. Please check error logs."+Fore.RESET)
        sys.exit()
        
    if not req_response:
        print()
        print(Fore.RED+"HTTP request returned an empty list."+Fore.RESET)
        print()
        print(Fore.YELLOW+"Please check if user exists and Baraag is up, and try again later."+Fore.RESET)
        print()
        print("Exiting...")
        sys.exit()
    
    else:       
        while 'next' in req_response.links.keys():
            follow_list.extend(req_response.json())
            url = req_response.links["next"]["url"]
            req_response = requests.get(url)
            
        else:
            follow_list.extend(req_response.json())         
        
        return follow_list

def parse_following(follow_list):
    """
    Returns a simple dictionary containing information of all accounts a given
    user ID follows.

    It takes 1 argument:
        
    follow_list = a list of dictionaries cointaining followed account
                  information, generated by get_following().
                  REQUIRED
    
    Returns: a dictionary containing followed account name and ID.

    """
    return {account['acct']: {'account': account['acct'], 'id': account['id']}\
            for account in follow_list}

def get_owner_info(client):
    """
    Returns a dictionary with basic information on the logged-in user 
    (ID and followed users).
        
    It takes 1 argument:
        
    client = Mastodon client object, generated/initialized by initialize()
             REQUIRED

    Returns: a dictionary {'id': owner_id(int), 
                           'following':{ account_name (str): {'account':(str),
                                                              'id':(int)}
                                        }}
    """
    try:
        owner_info = client.me()
    
    except MastodonNetworkError as exc:
        mastodon_network_error_handler(exc)
          
    except MastodonError as exc:
        mastodon_error_handler(exc)    
    
    owner_id = owner_info['id']
    following_info = get_following(owner_id)
    following_info = parse_following(following_info)
    
    return {'id': owner_id, 'following': following_info}
    
def get_page(client = client, user_id = None, newest_post = None):
    """
    Collects a user's posts containing attached media up to a specified
    post ID. Limited to 40 posts due to Mastodon API, so a "page" contains
    40 posts.
    
    Use within get_timeline() to iterate over all posts.
    
    Takes 3 arguments:
        
    client = Mastodon client object, generated/initialized by initialize()
             Defaults to client.
             REQUIRED
    
    user_id = user ID on Baraag (int); mainly derived from ['following']['id']
              in the dictionary generated by get_owner_info().
              Defaults to None
              REQUIRED
              
    newest_post = ID of the newest post in the page to fetch. Usually defined
                  by the pagination in get_timeline().
                  Defaults to None
                  OPTIONAL, but then it will only fetch the newest 40 posts.
                  
    Returns: an AttribAccessList Mastodon object with 40 AttribAccessDic Mastodon
             objects (i.e a page with 40 posts)
    """
    try:    
        page = client.account_statuses(id=user_id, 
                                    only_media = True,
                                    exclude_replies = True,
                                    limit =  40,
                                    max_id = newest_post)
    
    except MastodonNetworkError as exc:
        mastodon_network_error_handler(exc)
          
    except MastodonError as exc:
        mastodon_error_handler(exc) 
    
    return page


def get_timeline(client = client, user_id = None):
    """
    Constructs a timeline of a user with a given ID using the posts fetched
    by get_page(), iterating over the pages based on the last post ID of
    every page, and stopping once there are no more posts to fetch.
    
    Takes 3 arguments:
    
    client = Mastodon client object, generated/initialized by initialize()
             Defaults to client.
             REQUIRED
             
    user_id = user ID on Baraag (int); mainly derived from ['following']['id']
              in the dictionary generated by get_owner_info().
              Defaults to None
              REQUIRED

    Returns: a list containing all AttribAccessList Mastodon objects fetched
             by get_page().

    """
    timeline = []
    
    newest_post = None
    
    page = get_page(client, user_id, newest_post)
    
    counter = 0
    
    while len(page) != 0:
        timeline.append(page)
        newest_post = page[-1]['id']
        page = get_page(client, user_id, newest_post)
        counter +=1
        print("Fetching page "+str(counter)+"; Last post of page: "+str(newest_post))
    print()
    
    return timeline

def get_attachment_data(timeline):
    """
    Generates a dictionary of all post IDs, media attachment IDs and file URLs
    in a timeline generated by get_timeline(), and assigns each attachment a
    local filename for saving to disk.
    
    It takes 1 argument:
        
    timeline = a list containing all AttribAccessList Mastodon objects fetched
               by get_page(), generated by get_timeline().
               REQUIRED
               
    Returns: a dictionary containing all media attachments, segregated by post
             ID: { post_id: { 'media': 
                             { attachment_id : { 'id': (int), 
                                               'url': (str), 
                                               'filename':(str) }
                              }}}
    """
    attachment_dic = {}
    
    for page in timeline:
        for subpage in page:
            date = str(subpage['created_at']).split()[0]
            post_id = str(subpage['id'])
            
            attachment_dic[post_id] = {}
            attachment_dic[post_id]['id'] = post_id
            attachment_dic[post_id]['media'] = {}
            
            attachments = subpage['media_attachments']
            
            for attachment in attachments:
                attachment_id = str(attachment['id'])
                if "media_proxy" in attachment['url']:
                    attachment_url = attachment['remote_url'].split('?')[0]
                else:
                    attachment_url = attachment['url']
                
                extension = "." + attachment_url.split(".")[-1]
                
                if "com" in extension or "/" in extension:
                    print("Extension could not be inferred for attachment "+ \
                          attachment_id+" from post "+post_id+".")
                    print("Possible redirect url...")
                    print()
                    print("Temporarily fetching file to infer filetype...")
                    
                    try:
                        problem_file = requests.get(attachment_url)
                        file_header = problem_file.headers
                        extension = "."+file_header['Content-Disposition'].split(".")[-1].strip('\"')
                        print()
                        print("Extension inferred from HTTP response: "+extension[1:])
                        print()
                    
                    except Exception as exc:
                        logging.exception(str(exc))
                        print()
                        print(Fore.RED+"Failed to infer file type!"+Fore.RESET)
                        print()
                        print("Skipping...")
                        continue
                
                else:
                    pass
                
                filename = "_".join([date, post_id, attachment_id])+extension
                
                attachment_dic[post_id]['media'][attachment_id] = {}
                
                attachment_dic[post_id]['media'][attachment_id]['id'] = attachment_id
                
                attachment_dic[post_id]['media'][attachment_id]['url'] = attachment_url
                
                attachment_dic[post_id]['media'][attachment_id]['filename'] = filename
    
    return attachment_dic

def download_file(file, folder):
    """
    Downloads the specified file to the specified folder.
    
    Takes 2 arguments:
        
    file = an attachment in dictionary form {attachment_id: { 'id': (int), 
                                                              'url': (str), 
                                                              'filename':(str)
                                                              }} ,
            existing in the larger dictionary generated by 
            get_attachment_data().
            REQUIRED
    
    folder = the folder name where the attachment will be downloaded, usually 
             defined by process_following_user() at runtime.
             REQUIRED.
             
    Returns nothing, saves specified attachment to a file with the specified
    filename in the specified folder.
    """
    url = file['url']
    filename = file['filename']
    rel_path = folder+file['filename']
    file_id = file['id']
    
    if os.path.isfile(rel_path):
        print("File "+filename+" already exists in folder "+folder[:-1]+". Skipping...")
    else:
        with requests.get(url, stream = True) as request:
            try:
                with open(rel_path, 'wb') as output_file:
                    for chunk in request.iter_content(chunk_size=None):
                        output_file.write(chunk)
                print("Downloaded "+file_id+" to "+filename)
                
            except Exception as exc:
                logging.exception(str(exc))
                print()
                print(Fore.RED+"HTTP request failed. Please check error logs."+Fore.RESET)
                sys.exit()

def sanitize(string):
    """
    Sanitizes a given string to remove potentially problematic characters.
    Used mainly to sanitize account names so they can be used as part of folder
    names. 
    
    This is admittedly a horrible implementation and might be rewritten in 
    later releases.
    
    Takes 1 argument:
        
    string = a string to be sanitized, usually the account name of a followed
             account to process when saving files to disk.
             REQUIRED
             
    Returns: the input string with the offending characters replaced by an
             underscore.

    """
    bad_chars = ['^', '@', '%','$', '?', ':', '<', '>', '\\', '*', '|', '"'," "]
    sanitized_chars = []
    
    for char in string:
        if char in bad_chars:
            sanitized_chars.append("_")
        else:
            sanitized_chars.append(char)
            
    sanitized_string = "".join(sanitized_chars)

    return sanitized_string 

def process_following_user(client, settings, follow_dic):
    """
    Goes over every account followed by an user, collects all posts with 
    media attachments, and downloads them to disk in folders according to
    account name and user ID. Additionally, converts MP4 attachments if
    ffmpeg is enabled in the settings (from config.ini, passed as argument)
    
    Requires get_timeline(), get_attachment_data() and download_file() to
    operate.
    
    Takes 2 arguments:
        
    client = Mastodon client object, generated/initialized by initialize()
             Defaults to client.
             REQUIRED
             
    settings = dictionary of conversion settings, created by ffmpeg_validate()
    
    follow_dic = a dictionary of followed account names and IDs in the format
                 {account_name (str): {'account':(str),'id':(int)}.
                  
                  Obtained from the ['following'] key of the dictionary
                  returned by get_owner_info(), or alternatively from
                  search_user().

    Returns nothing, saves all media attachments to disk and converts them if
    conversion is enabled.
    """
    total_number = len(follow_dic.keys())
    
    current_number = 1
    
    for key in follow_dic.keys():
        account = follow_dic[key]
        account_name = account['account']
        account_id = account['id']
        account_folder_name = sanitize(account_name)+"_"+str(account_id)
              
        print("Processing user "+str(current_number)+"/"+str(total_number)+":")
        print("Account: "+account_name)
        print("ID: "+str(account_id)+"\n")
        print("Processing posts: \n")
        
        timeline = get_timeline(client, account_id)
        
        media = get_attachment_data(timeline)
             
        if os.name == "posix":
            folder_path = account_folder_name+"/"
        else:
            folder_path = account_folder_name+"\\"
              
        if not os.path.isdir(account_folder_name):
            os.makedirs(account_folder_name)
        else:
            pass
                
        for post in media.keys():
            post = media[post]['media']
            for file in post.keys():
                file = post[file]
                extension = file["filename"].split(".")[-1]
                download_file(file, folder_path)
                if extension == "mp4" and settings["use_ffmpeg"]:
                    video_convert(settings, file, folder_path)
                else:
                    pass
        
        current_number +=1
        
        print()

def search_user(client):
    """
    Searches Baraag for an account, defined by the user.

    Takes 1 arguments:
        
    client = Mastodon client object, generated/initialized by initialize()
             Defaults to client.
             REQUIRED
             
             
    Returns a dictionary with the info of the user from which media should be
    downloaded, in the format {account_name (str): {'account':(str),'id':(int)}.         
    """
    results = []
    while not results:
    
        try:
            username = input("Please type in username to search (Ctrl+C to exit): ")
            results = client.account_search(username)
            if not results:
                print(Fore.RED+"User not found!"+Fore.RESET+" Please try again!")
            
        except MastodonNetworkError as exc:
            mastodon_network_error_handler(exc)
              
        except MastodonError as exc:
            mastodon_error_handler(exc)         
        
        except KeyboardInterrupt:
            print()
            print(Fore.YELLOW+"Interrupted by user. Exiting..."+Fore.RESET)
            sys.exit()

    if len(results) > 1:
        print(str(len(results))+" users found: \n")
        for number, item in enumerate(results):
            print(str(number+1) +" "+item['display_name']\
                  +" URL: "+item['url']
                  +" ID: "+str(item['id'])+"\n")
              
        valid_choices = list(range(1, len(results) + 1))
        selection = ""
        
        while selection not in valid_choices:
            selection = ""
            while not selection.isdigit():
                selection = input("Please pick the user to be used from the list: ")
            else:
                selection = int(selection)                
            
        selection -=1
        result_dic = {results[selection]['acct']:\
                      {'account': results[selection]['acct'],\
                       'id': results[selection]['id']}}
        
    else:   
        result_dic = {results[0]['acct']:\
                      {'account': results[0]['acct'],\
                       'id': results[0]['id']}}
    
    return result_dic

def download_following(client, settings):
    """
    Routine loop that downloads media from all accounts the user follows.
    Segregated from main() since v0.014. Requires a setting dictionary as
    an argument as of v0.02.
    
    Takes 2 arguments:
        
    client = Mastodon client object, generated/initialized by initialize()
             Defaults to client.
             REQUIRED
    settings = dictionary of conversion settings, created by ffmpeg_validate()
               REQUIRED
             
    Returns nothing, saves files to disk, exits program when done.

    """
    # Getting user information
           
    owner_info = get_owner_info(client)
    
    # Get following list
    
    follow_list = owner_info['following']
    follow_number = len(follow_list)
    
    # Process followed accounts and start downloads
    print()
    print(Fore.YELLOW+"Processing all followed accounts ("+str(follow_number)+" users)"+Fore.RESET)
    print()
    process_following_user(client, settings, follow_list)
    print(Fore.GREEN+"All done!"+Fore.RESET)

def select_menu():
    """
    Basic selection menu.
    
    It takes no arguments.
    
    It returns a selection number (INT).
    """
    
    print("\nChoose an option:\n")
    print("1. Download media from all followed accounts")
    print("2. Search for user to download media from")
    print("3. Exit\n")
    
    valid_choices = [1,2,3]
    selection = ""
    
    try:
        while selection not in valid_choices:
            selection = ""
            while not selection.isdigit():
                selection = input("Please choose an option: ")

            else:
                selection = int(selection)  
        
    except KeyboardInterrupt:
        print()
        print(Fore.YELLOW+"Interrupted by user. Exiting..."+Fore.RESET)
        sys.exit()
        
    return selection

def write_ini():
    """
    Writes a basic ini file for ffmpeg settings in case it does not exist
    or has invalid contents.
    
    Defaults to setting "use_ffmpeg" to False.

    It takes no arguments and returns nothing.    
    """
    ini_settings =  "use_ffmpeg = False\n"\
                    "ffmpeg_path = System\n"\
                    "convert_gif = True\n"\
                    "convert_apng = True\n"\
                    "file_size_limit = 50.0"
    
    with open("config.ini", "w") as ini_file:
        ini_file.writelines(ini_settings)

def read_ini():
    """
    Reads a config.ini present in the base folder of the script.

    It takes no arguments and returns nothing.
    """
    with open("config.ini", "r") as ini_file:
        settings = ini_file.readlines()
    settings = [x.replace(" ", "").strip().split("=")for x in settings]
    
    settings = {x[0]:x[1] for x in settings}
    
    if settings["use_ffmpeg"] == "True":
        settings["use_ffmpeg"] = True
    else:
        settings["use_ffmpeg"] = False
        
    if settings["convert_gif"] == "True":
        settings["convert_gif"] = True
    else:
        settings["convert_gif"] = False
        
    if settings["convert_apng"] == "True":
        settings["convert_apng"] = True
    else:
        settings["convert_apng"] = False
    
    try:
        settings["file_size_limit"] = float(settings["file_size_limit"])
    except ValueError:
        print(Fore.RED+"Invalid filesize limit value!"+Fore.RESET +
              " Resetting to defaults...")
        print()
        settings["file_size_limit"] = 50.0
         
    return settings

def validate_ini(settings):
    """
    Runs a quick validation of the settings in the config.ini file.
    
    Returns a boolean of the validity of the file.
    """
    valid_options = ["use_ffmpeg", "ffmpeg_path", "convert_gif", "convert_apng",
                     "file_size_limit"]
    
    if sorted(valid_options) == sorted(list(settings.keys())):
        return True
    else:
        return False

def ffmpeg_init():
    """
    Runs an initialization loop for ffmpeg to enable it in case the user so
    requires and/or it is present in the system.
    
    In short, it:
        1- reads the config.ini file if present
        2- creates the file if not present/and or file is invalid
    
    Returns a dictionary with the data from the config.ini file
    """
    if os.path.isfile("config.ini"):
        print(Fore.GREEN+"Ffmpeg settings file found!"+Fore.RESET)
        print()
        print("Reading settings file...")
        print()
        try:
            settings = read_ini()
            if validate_ini(settings):
                return settings
            else:
                print(Fore.RED+"Settings invalid! Reinitializing settings file"\
                      "..."+Fore.RESET)
                print()
                write_ini()
                settings = read_ini()
                return settings
        except:
            print(Fore.RED+"Settings invalid! Reinitializing settings file..."
                  +Fore.RESET)
            print()
            print("Creating settings file...")
            print()
            write_ini()
            settings = read_ini()
            return settings
    else:
        print(Fore.RED+"Settings file not found!"+Fore.RESET)
        print()
        print("Creating settings file...")
        print()
        write_ini()
        settings = read_ini()
        return settings

def ffmpeg_validate(settings):
    """
    Validates the settings of the config.ini file based on OS and settings
    in the file.
    
    Takes the settings from ffmpeg_init() as a required parameter.
    
    Returns the settings dictionary as is if settings are valid, or with
    ffmpeg turned off (settings["use_ffmpeg"] = False) if settings are invalid
    or ffmpeg is not present.
    """
    current_os = sys.platform
    settings = settings
    
    if settings["ffmpeg_path"] == "System":
        if current_os == "linux":
            ffmpeg_path = "/usr/bin/"
            ffmpeg_exe = "ffmpeg"
            ffmpeg_full_path = ffmpeg_path + ffmpeg_exe
            settings["ffmpeg_path"] = ffmpeg_full_path
        
        elif current_os == "darwin":
            ffmpeg_path = ""
            ffmpeg_exe = "ffmpeg"
            ffmpeg_full_path = ffmpeg_path + ffmpeg_exe
            settings["ffmpeg_path"] = ffmpeg_full_path 
        
        else:
            ffmpeg_path = ""
            ffmpeg_exe = "ffmpeg.exe"
            ffmpeg_full_path = ffmpeg_path + ffmpeg_exe
            settings["ffmpeg_path"] = ffmpeg_full_path          
    else:
        pass
    
    try: 
        if os.path.isfile(settings["ffmpeg_path"]):
            print(Fore.GREEN+"Ffmpeg executable found!"+Fore.RESET)
            print()
            return settings
            
        else:
            print(Fore.RED+"Ffmpeg executable not found!"+Fore.RESET)
            print("Disabling Ffmpeg conversion...")
            print()
            settings["use_ffmpeg"] = False
            return settings
    except:
        print(Fore.RED+"Ffmpeg executable not found!"+Fore.RESET)
        print("Disabling Ffmpeg conversion...")
        print()
        settings["use_ffmpeg"] = False
        return settings

def video_convert(settings, file, folder):
    """
    Converts a given MP4 file to APNG and GIF depending on the contents of the
    settings dictionary (derived from config.ini)
    
    Usually run after download_file() to do on-the-fly conversion as needed.
    
    Keep in mind "file" here does not mean the actual file on disk, but rather
    its attachment "metadata" dictionary generated by get_attachment_data()
    
    Takes 3 arguments:
        settings = settings dictionary returned by ffmpeg_validate(); REQUIRED
        file = an attachment in dictionary form {attachment_id: { 'id': (int), 
                                                                  'url': (str), 
                                                                  'filename':(str)
                                                                  }} ,
                existing in the larger dictionary generated by 
                get_attachment_data().
                REQUIRED
        folder = the folder name where the attachment will be downloaded, usually 
                 defined by process_following_user() at runtime.
                 REQUIRED.
    
    Returns nothing, generates GIF and APNG files in the same folder as the MP4
    file.
    
    This is admiteddly a very rudimentary implementation, might revamp in future
    releases.
    """
    apng = settings["convert_apng"]
    gif = settings["convert_gif"]
    ffmpeg = settings["ffmpeg_path"]
    size_limit = settings["file_size_limit"]
    
    filename = file['filename']
    filename_stem = filename.split(".")[0]
    input_path = folder + filename
    
    # This size is in BYTES, so divide by 1048576 for MB
    file_size = os.path.getsize(input_path)/1048576
    
    if file_size <= size_limit:
        if apng:
            output = filename_stem + ".apng"
            input_path = folder + filename
            output_path = folder + output
            if os.path.isfile(output_path):
                print("File "+output+" already exists in folder "+folder[:-1]+". Skipping...")
            else:
                print("Converting to APNG...")
                arguments = [ffmpeg, "-i", input_path, output_path]
                try:
                    process = subprocess.run(arguments, stderr=subprocess.PIPE,
                                         stdout=subprocess.PIPE, text=True,
                                         check=True)
                    stdout = process.stdout
                    print("Conversion to APNG successful")
                except subprocess.CalledProcessError as exc:
                    logging.exception(str(exc))
                    print(Fore.RED+"Conversion to APNG failed. Please check error logs."+Fore.RESET)
                    print("Continue anyway...")

        if gif:
            output = filename_stem + ".gif"
            input_path = folder + filename
            output_path = folder + output
            if os.path.isfile(output_path):
                print("File "+output+" already exists in folder "+folder[:-1]+". Skipping...")
            else:
                print("Converting to GIF...")
                arguments = [ffmpeg, "-i", input_path, "-filter_complex",
                             '[0:v]split[a][b];[a]palettegen=stats_mode=diff[p];'\
                                 '[b][p]paletteuse=dither=bayer:bayer_scale=5:'\
                                     'diff_mode=rectangle', output_path]
                try:
                    process = subprocess.run(arguments, stderr=subprocess.PIPE,
                                             stdout=subprocess.PIPE, text=True,
                                             check=True)
                    stdout = process.stdout
                    print("Conversion to GIF successful")
                except subprocess.CalledProcessError as exc:
                    logging.exception(str(exc))
                    print(Fore.RED+"Conversion to GIF failed. Please check error logs."+Fore.RESET)
                    print("Continue anyway...")

    else:
        print("File over the filesize limit. Skipping...")
#%%
def main():
    try:
        print("------------------------------------------------------")
        print(Fore.LIGHTCYAN_EX+"Baraag DL version "+str(baraag_dl_version))
        print("by rizelbr"+Fore.RESET)
        print()
        print("Github: "+Fore.LIGHTBLUE_EX+"https://github.com/rizelbr/Baraag_DL"+Fore.RESET)
        print("------------------------------------------------------")
        print()
        
        # Program settings initialization
        
        settings = ffmpeg_init()

        # Initialize Ffmpeg
        settings = ffmpeg_validate(settings)
    
        if settings["use_ffmpeg"]:
            print(Fore.GREEN+"Ffmpeg conversion enabled."+Fore.RESET)
            print()
        else:
            print(Fore.YELLOW+"Ffmpeg conversion disabled"+Fore.RESET)
            print()

        # Client initialization
        
        client = initialize()
        
        # Main menu
        selection = select_menu()
        
        if selection == 1:
            # Downloading all followed accounts
            download_following(client, settings)
            
        elif selection == 2:
            # Downloading all media from a specific account
            user_to_download = search_user(client)
            print()
            process_following_user(client, settings, user_to_download)
            print(Fore.GREEN+"All done!"+Fore.RESET)
           
        else:
            print()
            print(Fore.YELLOW+"Exiting..."+Fore.RESET)
            sys.exit()
        
        if os.path.isfile(logfile):
            print(Fore.YELLOW+"There were errors during the execution "\
                  "of Baraag DL. Please check logs for details."+Fore.RESET)
        else:
            pass
        
    except KeyboardInterrupt:
        print()
        print(Fore.YELLOW+"Interrupted by user. Exiting..."+Fore.RESET)
        sys.exit()

if __name__ == "__main__": 
    main()
#%% DEBUG
