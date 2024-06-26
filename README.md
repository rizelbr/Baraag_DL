# Baraag DL

A simple Baraag media downloader, made to be a simple way of downloading all images/videos in posts made by accounts you follow.

Inspired by [PixivUtil](https://github.com/Nandaka/PixivUtil2) and [FantiaDL](https://github.com/bitbybyte/fantiadl).

Many thanks to the folks at [Mastodon.py](https://github.com/halcy/Mastodon.py) for making this implementation much easier than expected.

# Installation

## Linux/MacOS
### Recommended
- Create an environment with:
```python3 -m venv baraag_dl```

- Activate the environment:
```source baraag_dl/bin/activate```

- Download [requirements.txt](https://github.com/rizelbr/Baraag_DL/blob/main/requirements.txt) and baraag_dl.py to your current folder.

- Install dependencies:
```python3 -m pip install -r requirements.txt```

- Alternatively, install the following packages using ```python3 -m pip install```:
```
colorama
Mastodon.py
requests
```
- Run Baraag_DL:
  ```python3 baraag_dl.py```

- After done running, either close the terminal or deactivate the environment with: ```deactivate```

#### Optional additional setup
- For added convenience, I recommend either creating a shell script to execute ```baraag_dl.py``` using the Python interpreter from the environment you created above, or modifying ```baraag_dl.py``` to point to the environment's Python interpreter when executing.

- For the former, if we suppose you created the ```baraag_dl``` environment in your home folder, create a file containing the following lines in the same folder as ```baraag_dl.py```:
```
#!/bin/bash

~/baraag_dl/bin/python3 baraag_dl.py
```

- Save the file with a name of your choice (let's call it ```run.sh``` for this example), and grant it execution permissions with ```chmod +x run.sh``` .

- From this point on, you should be able to execute Baraag DL by running ```run.sh``` , without the need to activate or deactivate environments.

- For the latter, modify the first line in ```baraag_dl.py``` to ```#!~/baraag_dl/bin/python3```

- From this point on, you should be able to execute ```baraag_dl.py``` directly, without the need for activating or deactivating an environment.

- Please be aware that if you choose the latter, you **will** need to redo this modification whenever you update Baraag DL.

### Alternative 1

- Skip the virtual environment and install the requirements to the base Python install using ```pip install``` to install the required packages listed above.

### Alternative 2

- Use Anaconda/miniconda/miniforge to create an environment, install the required packages, and run ```baraag_dl.py``` from within the environment.

## Windows
### Recommended
- Download the [prepackaged binaries](https://github.com/rizelbr/Baraag_DL/releases).

### Alternative
- Download and install Python if not already installed.

- Create an environment with:
```py -m venv baraag_dl```

- Activate the environment:
```baraag_dl\Scripts\activate```

- Download [requirements.txt](https://github.com/rizelbr/Baraag_DL/blob/main/requirements.txt) and baraag_dl.py to your current folder.

- Install dependencies:
```py -m pip install -r requirements.txt```

- Alternatively, install the following packages using ```py -m pip install```:
```
colorama
Mastodon.py
requests
```
- Run Baraag_DL:
  ```py baraag_dl.py```

- After done running, either close the terminal or deactivate the environment with: ```deactivate```

# Usage
## Logging in and authentication
### First run
- Baraag DL will register a client with the Mastodon API used by Baraag.
- This will generate a persistent authentication token, ```client_credentials``` in the same folder baraag_dl.py is run from.
- You will be prompted for a username (e-mail) and password to log into your Baraag account.
- Should the login be successful, Baraag DL will generate a persistent user token, ```user_credentials``` in the same folder baraag_dl.py is run from.

### Subsequent runs
- If ```client_credentials``` and ```user_credentials``` are still valid, authentication will happen without user input.
- Should either or both files become invalid or corrupted, Baraag DL will recreate the client and prompt you for username and password again.
 
## Execution
- You will then be shown a menu and asked how you'd like to proceed:
### 1. Download from all followed accounts
- Baraag DL will automatically:
    - Fetch all accounts you follow
    - Fetch all posts by accounts you follow that contain attachments
    - Download each attachment sequentially for all followed accounts
    
### 2. Search for a specific user
- Baraag DL will then prompt you for the name of the artist/account to search. 
- Should the search be successful, it will present you with a list of the accounts matching the name you input.
- You can then choose among the options of the list for the account from which all media will be downloaded.

## Downloading and Filenames
- Files are saved as ```{Date posted}_{Post ID}_{Attachment_ID}.extension``` in a folder for each account, named in the format ```{Account name}_{Account ID}```. Keep in mind that ```Account name``` is not the same as ```Display name```, so an account's public name and Baraag registration name may differ.
- Files already downloaded and saved to disk are skipped to save time, bandwidth, and not bombard the API with requests.

:warning: The Mastodon API is limited to 300 requests every 5 minutes. This means that Baraag DL will run considerably slower after some time as to prevent being cut off by the API.

# To-Do
- Implement dry run mode (debugging)
- Implement Pawoo compatibility.
- Install script for MacOS/Linux (?)
